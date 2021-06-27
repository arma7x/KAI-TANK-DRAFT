import asyncio
import json
import random
import sys
from dataclasses import dataclass

import websockets

PLAYERS = dict()


@dataclass
class Position:
    x: float = 100
    y: float = 100


@dataclass
class Player:
    pos: Position
    hp: float = 100
    nick: str = ""

    def to_dict(self, you=None):
        if you:
            return dict(hp=self.hp, x=self.pos.x, y=self.pos.y, nick="YOU")
        else:
            return dict(hp=self.hp, x=self.pos.x, y=self.pos.y, nick=self.nick)


async def generate_id():
    id_ = random.randint(1_000_000_000, 2_000_000_000)
    if id_ in PLAYERS:
        return generate_id()
    return id_


async def get_others(id_=None):
    global PLAYERS
    if id_ is None:
        return [PLAYERS[pl_id].to_dict() for pl_id in PLAYERS]
    else:
        return [
            PLAYERS[pl_id].to_dict(True)
            if pl_id == id_
            else PLAYERS[pl_id].to_dict()
            for pl_id in PLAYERS
        ]


async def init(nick):
    id_ = await generate_id()
    if nick is None:
        nick = f"p{str(id_)[:5]}"
    PLAYERS[id_] = Player(nick=nick, pos=Position(x=100, y=100))
    return id_


async def pos(id_, new_pos):
    # TODO: validate move here
    PLAYERS[id_].pos.x = new_pos[0]
    PLAYERS[id_].pos.y = new_pos[1]


async def accept(ws, path):
    nick_check = re.compile("[A-Za-z0-9]+").match
    nick = json.loads(await ws.recv()).get("nick")
    if not nick_check(nick):
        await ws.send('{"error": "Invalid nick"}')
        return
    id_ = await init(nick)
    async for message in ws:
        await ws.send(json.dumps({"id": id_, "others": await get_others(id_)}))
        message = json.loads(message)
        if message.get("bye") == "BYE":
            break

        new_pos = message.get("pos")
        if new_pos:
            await pos(id_, new_pos)

    PLAYERS.pop(id_)


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
        ip = bind_addr[0] or "127.0.0.1"
        port = int(bind_addr[1])
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(accept, ip, port)
        )
    asyncio.get_event_loop().run_forever()
