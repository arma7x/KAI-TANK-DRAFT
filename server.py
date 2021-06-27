import asyncio
import json
import random
import sys
import re
from dataclasses import dataclass

import websockets

from websockets import WebSocketServerProtocol

PLAYERS = dict()

WSCONS = set() # emit to all

@dataclass
class Position:
    x: float = 100
    y: float = 100
    direction: str = "down"


@dataclass
class Player:
    ws: WebSocketServerProtocol # send data to self conn
    pos: Position
    hp: float = 100
    nick: str = ""

    def to_dict(self, you=None):
        if you:
            return dict(hp=self.hp, x=self.pos.x, y=self.pos.y, direction=self.pos.direction, nick="YOU")
        else:
            return dict(hp=self.hp, x=self.pos.x, y=self.pos.y, direction=self.pos.direction, nick=self.nick)


async def generate_id():
    id_ = random.randint(1_000_000_000, 2_000_000_000)
    if id_ in PLAYERS:
        return generate_id()
    return id_


async def get_positions():
    global PLAYERS
    positions = dict()
    for pl_id, val in PLAYERS.items():
      positions[pl_id] = val.to_dict()
    return positions


async def init(nick, ws):
    WSCONS.add(ws)
    id_ = await generate_id()
    if nick is None:
        nick = f"p{str(id_)[:5]}"
    PLAYERS[id_] = Player(nick=nick, pos=Position(x=100, y=100, direction="down"), ws=ws)
    return id_


async def pos(id_, new_pos):
    # TODO: validate move here
    PLAYERS[id_].pos.x = new_pos[0]
    PLAYERS[id_].pos.y = new_pos[1]
    PLAYERS[id_].pos.direction = new_pos[2]


async def accept(ws, path):
    nick_check = re.compile("[A-Za-z0-9]+").match
    nick = json.loads(await ws.recv()).get("nick")
    if nick and not nick_check(nick):
        await ws.send('{"error": "Invalid nick"}')
        return
    id_ = await init(nick, ws)
    await ws.send(json.dumps({"init": id_, "position": PLAYERS[id_].to_dict()}))
    async for message in ws:
        # await ws.send(json.dumps({"id": id_, "positions": await get_positions()}))
        message = json.loads(message)
        if message.get("bye") == "BYE":
            break

        new_pos = message.get("move")
        if new_pos:
            await pos(id_, new_pos)
            for con in WSCONS:
              await con.send(json.dumps({"positions": await get_positions()}))

    PLAYERS.pop(id_)
    WSCONS.remove(ws)
    for con in WSCONS:
      await con.send(json.dumps({"dc": id_}))


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
