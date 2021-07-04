import asyncio
import random
import sys
import re
import json
import math
from base64 import b64encode, b64decode
from enum import Enum
from dataclasses import dataclass

import websockets
import tank_pb2

MAP_WIDTH = 240
MAP_HEIGHT = 320
BULLET_SIZE = 4
BULLET_VELOCITY = 150
TANK_WIDTH = 16
TANK_HEIGHT = 16
# 1000/60FPS
TICKING = 1000/60


PLAYERS = dict()
BULLETS = dict()

class Direction(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

@dataclass
class Position:
    x: float = 100
    y: float = 100


@dataclass
class Player:
    socket: websockets.WebSocketServerProtocol
    pos: Position
    hp: float = 100
    nick: str = ""
    dir_: Direction = Direction.UP

    def to_pb(self, you=None):
        pos = tank_pb2.Position(x=self.pos.x, y=self.pos.y)
        pl = tank_pb2.Player(hp=self.hp, pos=pos, nick=self.nick, dir=self.dir_.value)
        if you:
            pl.nick = "YOU"
        return pl


async def generate_id():
    id_ = random.randint(1_000_000_000, 2_000_000_000)
    if id_ in PLAYERS:
        return generate_id()
    return id_


async def get_positions(pl_id=None):
    global PLAYERS
    positions = dict()
    for key, value in PLAYERS.items():
      positions[key] = value.to_pb()
    # if pl_id:
    #    positions[pl_id].nick = "YOU"
    return positions


async def init(nick, ws):
    id_ = await generate_id()
    if nick is None:
        nick = f"p{str(id_)[:5]}"
    PLAYERS[id_] = Player(nick=nick, pos=Position(x=random.randint(10, (MAP_WIDTH - 10)), y=random.randint(10, (MAP_HEIGHT - 10))), socket=ws)
    # PLAYERS[id_] = Player(nick=nick, pos=Position(x=271, y=297), socket=ws)
    # PLAYERS[id_] = Player(nick=nick, pos=Position(x=100, y=100), socket=ws)
    return id_


async def pos(id_, move):
    # TODO: validate move here
    PLAYERS[id_].pos.x = move.pos.x
    PLAYERS[id_].pos.y = move.pos.y
    # TODO: Check and see if it's a valid dir
    # if move.dir not in {"UP", "DOWN", "RIGHT", "LEFT"}:
        # raise ValueError(f"Invalid direction: {move.dir}")
    
    PLAYERS[id_].dir_ = getattr(Direction, Direction(move.dir).name)

# Refer to PROTOCOL.md for message_type

async def encode_message(message_type, message):
    return message_type + b64encode(message.SerializeToString()).decode("utf-8") 

async def decode_message(s):
    message_type = s[0]
    content = s[1:]

    if message_type == "0":
        return "0", tank_pb2.Movement.FromString(b64decode(content))
    if message_type == "1":
        return "1", tank_pb2.Voice.FromString(b64decode(content))
    if message_type == "2":
        return "2", tank_pb2.NickSelection.FromString(b64decode(content))
    if message_type == "3":
        return "3", tank_pb2.Bullet.FromString(b64decode(content))

    # raise ValueError(f"Invalid message type: {message_type}")

async def broadcastPlayer(id_):
    info_message = tank_pb2.InfoBroadcast(players=await get_positions(id_))
    for _, player in PLAYERS.items():
        await player.socket.send(await encode_message("0", info_message))

async def broadcastBullet():
    global BULLETS
    bullets = dict()
    for key, value in BULLETS.items():
        bullets[key] = value
    info_message = tank_pb2.BulletBroadcast(bullets=bullets)
    for _, player in PLAYERS.items():
        await player.socket.send(await encode_message("1", info_message))

async def periodic():
    # calculate bullet movement
    # x = -1 or y = -1 if bullet position is overmap area or hitted any tank
    global BULLETS
    while True:
        off_bullets = dict()
        for key, value in BULLETS.items():
            expired = False

            # https://www.khanacademy.org/math/geometry/hs-geo-analytic-geometry/hs-geo-distance-and-midpoints/v/distance-formula
            for plyr_id, plyr in PLAYERS.items():
                if (value.shooter != plyr_id):
                    v = math.sqrt(math.pow((value.pos.x - plyr.pos.x), 2) + math.pow((value.pos.y - plyr.pos.y), 2))
                    if (v <= 10.0):
                        value.pos.x = -1
                        value.pos.y = -1
                        expired = True
                        off_bullets[key] = value
                        break

            if (expired == False):
                if (value.dir == Direction.DOWN.value):
                  value.pos.y += BULLET_VELOCITY * TICKING / 1000
                  if (value.pos.y + BULLET_SIZE >= MAP_HEIGHT):
                      value.pos.y = -1
                      off_bullets[key] = value
                      expired = True
                elif (value.dir == Direction.UP.value):
                  value.pos.y -= BULLET_VELOCITY * TICKING / 1000
                  if (value.pos.y - BULLET_SIZE <= 0):
                      value.pos.y = -1
                      off_bullets[key] = value
                      expired = True
                elif (value.dir == Direction.RIGHT.value):
                  value.pos.x += BULLET_VELOCITY * TICKING / 1000
                  if (value.pos.x + BULLET_SIZE >= MAP_WIDTH):
                      value.pos.x = -1
                      off_bullets[key] = value
                      expired = True
                elif (value.dir == Direction.LEFT.value):
                  value.pos.x -= BULLET_VELOCITY * TICKING / 1000
                  if (value.pos.x - BULLET_SIZE <= 0):
                      value.pos.x = -1
                      off_bullets[key] = value
                      expired = True

        if (len(off_bullets) > 0):
            for key, _ in off_bullets.items():
                if (key in BULLETS.keys()):
                    BULLETS.pop(key)
            info_message = tank_pb2.BulletBroadcast(bullets=off_bullets)
            for _, player in PLAYERS.items():
                await player.socket.send(await encode_message("1", info_message))
        await asyncio.sleep(TICKING / 1000)

async def accept(ws, path):
    nick_check = re.compile("[A-Za-z0-9]+").match
    nick = None
    message = await decode_message(await ws.recv())
    if type(message) == tank_pb2.NickSelection:
        nick = message.nick
    if nick and not nick_check(nick):
        err = tank_pb2.ErrorMessage("Nick may contain only alphanumeric characters")
        await ws.send(await encode_message("5", err))
        return
    if nick and len(nick) > 12:
        err = tank_pb2.ErrorMessage("Nick must be 12 characters or less")
        await ws.send(await encode_message("5", err))
        return

    id_ = await init(nick, ws)
    init_message = tank_pb2.Init(id=id_)
    init_message.move.pos.x = PLAYERS[id_].pos.x
    init_message.move.pos.y = PLAYERS[id_].pos.y
    init_message.move.dir = PLAYERS[id_].dir_.value
    await ws.send(await encode_message("2", init_message))
    await broadcastPlayer(id_)
    await broadcastBullet()
    # hit race-condition
    try:
      async for message in ws:
          t, message = await decode_message(await ws.recv())
          if t == "0":
              await pos(id_, message)
              await broadcastPlayer(id_)
          if t == "3":
              bX: float = 0
              bY: float = 0
              message.id = await generate_id()
              message.shooter = id_

              if (PLAYERS[id_].dir_ == Direction.UP or PLAYERS[id_].dir_ == Direction.DOWN):
                  if (PLAYERS[id_].dir_ == Direction.DOWN):
                      bX = PLAYERS[id_].pos.x - (BULLET_SIZE / 2)
                      bY = PLAYERS[id_].pos.y + (TANK_HEIGHT / 2)
                  else:
                      bX = PLAYERS[id_].pos.x - (BULLET_SIZE / 2)
                      bY = PLAYERS[id_].pos.y - (TANK_HEIGHT / 2) - (BULLET_SIZE / 2)
              else:
                  if (PLAYERS[id_].dir_ == Direction.RIGHT):
                      bX = PLAYERS[id_].pos.x + (TANK_WIDTH / 2)
                      bY = PLAYERS[id_].pos.y - (BULLET_SIZE / 2)
                  else:
                      bX = PLAYERS[id_].pos.x - (TANK_WIDTH / 2) - (BULLET_SIZE / 2)
                      bY = PLAYERS[id_].pos.y - (BULLET_SIZE / 2)
              message.pos.x = bX
              message.pos.y = bY
              message.dir = PLAYERS[id_].dir_.value
              BULLETS[message.id] = message
              await broadcastBullet()
    except:
      pass

    PLAYERS.pop(id_)
    for player in PLAYERS.values():
      await player.socket.send(await encode_message("4", tank_pb2.Disconnect(id=id_)))
        
if __name__ == "__main__":
    if len(sys.argv) not in (1, 2):
        print("Invalid number of command line arguments", file=sys.stderr)
        sys.exit(1)

    bind_addr = "/home/shangul/.tank.sock"
    if len(sys.argv) == 2:
        bind_addr = sys.argv[1]

    if bind_addr.startswith("/"):
        asyncio.get_event_loop().run_until_complete(
            websockets.unix_serve(accept, bind_addr)
        )
    else:
        bind_addr = bind_addr.split(":")
        ip = bind_addr[0] or "0.0.0.0"
        port = int(bind_addr[1])
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(accept, ip, port)
        )
    asyncio.get_event_loop().run_until_complete(asyncio.get_event_loop().create_task(periodic()))
    asyncio.get_event_loop().run_forever()
