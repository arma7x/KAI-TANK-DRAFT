import asyncio
import json
import random
from dataclasses import dataclass

import websockets

PLAYERS = dict()

@dataclass
class Position:
    x: float = 100
    y: float = 100

@dataclass
class Player:
    pos: Position = Position()
    hp: float = 100

    async def to_dict(self):
        return dict(hp=self.hp, x=self.pos.x, y=self.pos.y)

async def generate_id():
    id_ = random.randint(1_000_000_000, 2_000_000_000)
    if id_ in PLAYERS:
        return generate_id()
    return id_

async def init():
    id_ = await generate_id()
    PLAYERS[id_] = Player()
    return id_

async def move(id_, movement):
    PLAYERS[id_].pos.x += movement[0]
    PLAYERS[id_].pos.y += movement[1]

async def accept(ws, path):
    global PLAYERS

    id_ = await init()
    async for message in ws:
        await ws.send(json.dumps({
            "id": id_,
            "others": [(await PLAYERS[pl_id].to_dict() if pl_id != id_ else None) for pl_id in PLAYERS]
        }))
        message = json.loads(message)
        movement = message.get("move")
        if movement:
            await move(id_, movement)
            
    print("CONNECTION CLOSED:", ws)

asyncio.get_event_loop().run_until_complete(websockets.serve(accept, "0.0.0.0", 65000))
asyncio.get_event_loop().run_forever()

