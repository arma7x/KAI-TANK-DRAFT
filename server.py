from flask import Flask, g
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

def update_tank_pos(tank_id, move=(0,0)):
    positions = getattr(g, "_positions", {})
    tank_pos = positions.get(tank_id, (100, 100))
    tank_pos[0] += move[0]
    tank_pos[1] += move[1]
    positions.set(tank_id, tank_pos)
    setattr(g, "_positions", positions)
    return positions[tank_id]

def get_tanks_pos(radius=10000):
    return getattr(g, "_positions", {})

@socketio.on("move")
def move_tank(message):
    tank_id = message["id"]
    move = message.get("move", (0, 0))
    emit("pos", {"data": update_tank_pos(tank_id, move)})
    emit("others_pos", {"data": get_tanks_pos()}, broadcast=True)

@socketio.on("connect")
def connect():
    emit("pos", {"data": update_tank_pos(tank_id, move)})
    emit("others_pos", {"data": get_tanks_pos()}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=65000, debug=True)
