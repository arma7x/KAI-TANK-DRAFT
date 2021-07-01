import asyncio
import random
import sys
import re
import json
from base64 import b64encode, b64decode
from enum import Enum
from dataclasses import dataclass

import websockets
import tank_pb2


PLAYERS = dict()

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
    if pl_id:
        positions[pl_id].nick = "YOU"
    return positions


async def init(nick, ws):
    id_ = await generate_id()
    if nick is None:
        nick = f"p{str(id_)[:5]}"
    PLAYERS[id_] = Player(nick=nick, pos=Position(x=100, y=100), socket=ws)
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

    # raise ValueError(f"Invalid message type: {message_type}")

async def broadcast(id_):
    info_message = tank_pb2.InfoBroadcast(players=await get_positions(id_))
    for _, player in PLAYERS.items():
        await player.socket.send(await encode_message("0", info_message))

async def accept(ws, path):
    nick_check = re.compile("[A-Za-z0-9]+").match
    nick = None
    message = await decode_message(await ws.recv())
    if type(message) == tank_pb2.NickSelection:
        nick = message.nick
    if nick and not nick_check(nick):
        err = tank_pb2.ErrorMessage("Nick may contain only alphanumeric characters")
        await ws.send(await encode_message("4", err))
        return
    if nick and len(nick) > 12:
        err = tank_pb2.ErrorMessage("Nick must be 12 characters or less")
        await ws.send(await encode_message("4", err))
        return

    id_ = await init(nick, ws)
    init_message = tank_pb2.Init(id=id_)
    init_message.move.pos.x = PLAYERS[id_].pos.x
    init_message.move.pos.y = PLAYERS[id_].pos.y
    init_message.move.dir = PLAYERS[id_].dir_.value
    await ws.send(await encode_message("2", init_message))
    await broadcast(id_)
    async for message in ws:
        # hit race-condition
        try:
            t, message = await decode_message(await ws.recv())
            if t == "0":
                await pos(id_, message)
                await broadcast(id_)
        except:
          pass

    PLAYERS.pop(id_)
    for player in PLAYERS.values():
      await player.socket.send(await encode_message("3", tank_pb2.Disconnect(id=id_)))
        
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
    asyncio.get_event_loop().run_forever()
