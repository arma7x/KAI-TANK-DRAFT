const BULLET_SIZE = 4;
const WIDTH = 400, HEIGHT = 400;

var myId = null;
var currentPlayer = null;
var othersPlayer = {};
var socket = null;
var pb_root = null;

// TODO regarding encode and decode functions:
// maybe use hashtable/dictionary instead of if/else?

function encodeMessage(type, msg) {
  // TODO: verify `msg` here with .verify()
  let encodedBinary = null;
  if (type === "0") {
    if (msg.dir && ![0,1,2,3].includes(msg.dir))
      throw new Error("Invalid direction");
    encodedBinary = pb_root.Movement.encode(msg).finish();
  } else if (type === "1") {
    encodedBinary = pb_root.Voice.encode(msg).finish();
  } else if (type === "2") {
    encodedBinary = pb_root.NickSelection.encode(msg).finish();
  }
  if (encodedBinary === null) {
    throw new Error("Invalid type for encoding");
  } else {
    return type + protobuf.util.base64.encode(encodedBinary, 0, encodedBinary.length);
  }
}

function decodeMessage(s) {
  let type = s[0];
  let content = s.slice(1, s.length);
  const bufferLength = protobuf.util.base64.length(content);
  let buffer = new Uint8Array(bufferLength);
  let message = null;
  protobuf.util.base64.decode(content, buffer, 0);
  if (type === "0") {
    message = pb_root.InfoBroadcast.decode(buffer);
  } else if (type === "1") {
    message = pb_root.Voice.decode(buffer);
  } else if (type === "3") {
    message = pb_root.Disconnect.decode(buffer);
  } else if (type === "2") {
    message = pb_root.Init.decode(buffer);
  } else if (type === "4") {
    message = pb_root.ErrorMessage.decode(buffer);
  }
  if (message === null) {
    throw new Error("Invalid type for decoding");
  } else {
    message._type = type;
    return message;
  }
}

var game = {
  resources: [
    { name: "greentank", type: "image", "src": "tank-green.png",  }
  ],
  loaded: function() {
    me.game.world.resize(WIDTH, HEIGHT);
    me.pool.register("greentank", game.Tank);
    me.pool.register("bullet", game.Bullet);
    this.playScreen = new game.PlayScreen();
    me.state.set(me.state.PLAY, this.playScreen);
    me.state.change(me.state.PLAY);

    let host = "shangul.de1.hashbang.sh"
    if (document.location.host != host)
      host = "ws://0.0.0.0:3000"
    else
      host = "wss://shangul.de1.hashbang.sh/server"
    socket = new WebSocket(host);
    socket.onmessage = evt => {
      let dataP = decodeMessage(evt.data);
      if (dataP._type === "2") {
        myId = dataP.id
        currentPlayer = me.game.world.addChild(me.pool.pull("greentank"));
        currentPlayer.pos.x = me.Math.clamp(dataP.move.pos.x, currentPlayer.minX, currentPlayer.maxX);
        currentPlayer.pos.y = me.Math.clamp(dataP.move.pos.y, currentPlayer.minY, currentPlayer.maxY);
        const dir = pb_root.Direction.__proto__[dataP.move.dir].toLowerCase();
        if (currentPlayer.__DIRECTION__ !== dir) {
          rotateTank(currentPlayer, dir);
        }
        follow(currentPlayer, currentPlayer.pos.x, currentPlayer.pos.y)
        console.log(JSON.stringify(dataP));
      } else if (dataP._type === "0") {
        console.log(dataP);
      }
      // below is old implemention
      try {
        let data = JSON.parse(evt.data);
        if (data.init) {
          myId = data.init
          currentPlayer = me.game.world.addChild(me.pool.pull("greentank"));
          currentPlayer.pos.x = me.Math.clamp(data.position.x, currentPlayer.minX, currentPlayer.maxX);
          currentPlayer.pos.y = me.Math.clamp(data.position.y, currentPlayer.minY, currentPlayer.maxY);
          if (currentPlayer.__DIRECTION__ !== data.position.direction) {
            rotateTank(currentPlayer, data.position.direction);
          }
          follow(currentPlayer, currentPlayer.pos.x, currentPlayer.pos.y)
          socket.send(JSON.stringify({move: [currentPlayer.pos.x, currentPlayer.pos.y, currentPlayer.__DIRECTION__]}));
        }
        if (data.positions) {
          //if (data.positions[myId]) {
            //var position = data.positions[myId];
            //currentPlayer.pos.x = me.Math.clamp(position.x, currentPlayer.minX, currentPlayer.maxX);
            //currentPlayer.pos.y = me.Math.clamp(position.y, currentPlayer.minY, currentPlayer.maxY);
            //if (currentPlayer.__DIRECTION__ !== position.direction) {
              //rotateTank(currentPlayer, position.direction);
            //}
          //}
          for (var p in data.positions) {
            p = parseInt(p)
            var position = data.positions[p];
            if (othersPlayer[p] == null && p !== myId) {
              othersPlayer[p] = me.game.world.addChild(me.pool.pull("greentank"));
              othersPlayer[p].pos.x = me.Math.clamp(position.x, othersPlayer[p].minX, othersPlayer[p].maxX);
              othersPlayer[p].pos.y = me.Math.clamp(position.y, othersPlayer[p].minY, othersPlayer[p].maxY);
            } else if (othersPlayer[p] && p !== myId) {
              if (othersPlayer[p].__DIRECTION__ !== position.direction) {
                rotateTank(othersPlayer[p], position.direction);
              }
              othersPlayer[p].pos.x = me.Math.clamp(position.x, othersPlayer[p].minX, othersPlayer[p].maxX);
              othersPlayer[p].pos.y = me.Math.clamp(position.y, othersPlayer[p].minY, othersPlayer[p].maxY);
            }
          }
        }
        if (data.dc) {
          if (othersPlayer[data.dc]) {
            me.game.world.removeChild(othersPlayer[data.dc]);
            delete othersPlayer[data.dc];
          }
        }
      } catch (e) {
        // console.log(e);
      }
    };
    socket.onopen = () => {
      socket.send(JSON.stringify({ping: true}));
    }
  },
  onload: function () {
    pb_root = new protobuf.Root();
    var _this = this;
    pb_root.load("tank.proto").then(function(rt) {
      if (!me.video.init(240, 320, {parent: document.body, scale: "auto", renderer: me.video.CANVAS})) {
        alert("Your browser does not support HTML5 Canvas :(");
        return;
      }

      me.audio.init("ogg");
      me.loader.preload(game.resources, _this.loaded.bind(_this));
    });
  },
};


game.PlayScreen = me.Stage.extend({
  onResetEvent: function() {
    me.game.world.addChild(new me.ColorLayer("background", "#A00"), 0);
    me.input.bindKey(me.input.KEY.LEFT, "left");
    me.input.bindKey(me.input.KEY.RIGHT, "right");
    me.input.bindKey(me.input.KEY.UP, "up");
    me.input.bindKey(me.input.KEY.DOWN, "down");
  },
  onDestroyEvent: function() {
    me.input.unbindKey(me.input.KEY.LEFT);
    me.input.unbindKey(me.input.KEY.RIGHT);
    me.input.unbindKey(me.input.KEY.UP);
    me.input.unbindKey(me.input.KEY.DOWN);
  }
});

me.event.subscribe(me.event.KEYDOWN, function (action, keyCode, edge) {
  const time = 30;
  const yAxis = ['up', 'down'];
  if (keyCode === 32) {
    var bX, bY, bD;
    if (yAxis.indexOf(currentPlayer.__DIRECTION__) > -1) {
      if (currentPlayer.__DIRECTION__ === 'down')
        bX = currentPlayer.pos.x - (BULLET_SIZE/2), bY = currentPlayer.pos.y + (currentPlayer.height / 2), bD = 'down';
      else
        bX = currentPlayer.pos.x - (BULLET_SIZE/2), bY = currentPlayer.pos.y - (currentPlayer.height / 2) - (BULLET_SIZE/2), bD = 'up';
    } else {
      if (currentPlayer.__DIRECTION__ === 'right')
        bX = currentPlayer.pos.x + (currentPlayer.width / 2), bY = currentPlayer.pos.y - (BULLET_SIZE/2), bD = 'right';
      else
        bX = currentPlayer.pos.x + (currentPlayer.width / 2) - (BULLET_SIZE/2) - currentPlayer.width, bY = currentPlayer.pos.y - (BULLET_SIZE/2), bD = 'left';
    }
    const b = me.game.world.addChild(me.pool.pull("bullet", bX, bY))
    b.__DIRECTION__ = bD;
  }

});

game.Tank = me.Sprite.extend({
  init: function() {
    this._super(me.Sprite, "init", [
      me.game.viewport.width / 2,
      me.game.viewport.height / 2,
      {
        image: me.loader.getImage("greentank"),
      }
    ]);
    this.__DIRECTION__ = 'down';
    this.scale(0.7, 0.7);
    this.vel = 65;
    this.minX = (this.width / 2);
    this.maxX = WIDTH - (this.height / 2);
    this.minY = (this.height / 2);
    this.maxY = HEIGHT - (this.height / 2);
  },
  update: function(time) {
    this._super(me.Sprite, "update", [time]);

    var newX = this.pos.x, newY = this.pos.y, newDirection = this.__DIRECTION__;
    const oldX = this.pos.x, oldY = this.pos.y, oldDirection = this.__DIRECTION__;
    if (me.input.isKeyPressed("left")) {
      if (this.__DIRECTION__ !== 'left') {
        newDirection = rotateTank(this, 'left');
      } else
        newX -= this.vel * time / 1000;
    } else if (me.input.isKeyPressed("right")) {
      if (this.__DIRECTION__ !== 'right') {
        newDirection = rotateTank(this, 'right');
      } else
        newX += this.vel * time / 1000;
    } else if (me.input.isKeyPressed("up")) {
      if (this.__DIRECTION__ !== 'up') {
        newDirection = rotateTank(this, 'up');
      } else
        newY -= this.vel * time / 1000;
    } else if (me.input.isKeyPressed("down")) {
      if (this.__DIRECTION__ !== 'down') {
        newDirection = rotateTank(this, 'down');
      } else
        newY += this.vel * time / 1000;
    }
    if (newX !== oldX || newY !== oldY || oldDirection !== newDirection) {
      this.pos.x = me.Math.clamp(newX, this.minX, this.maxX);
      this.pos.y = me.Math.clamp(newY, this.minY, this.maxY);
      var payload = {
        pos: {
          x: this.pos.x,
          y: this.pos.y
        },
        dir: pb_root.Direction[newDirection.toUpperCase()]
      }
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(encodeMessage("0", payload));
      }
      follow(this, oldX, oldY);
    }

    return true;
  }
});

game.Bullet = me.Entity.extend({
    init : function (x, y) {
        this._super(me.Entity, "init", [x, y, { width: BULLET_SIZE, height: BULLET_SIZE }]);
        this.vel = 250;
        this.body.collisionType = me.collision.types.PROJECTILE_OBJECT;
        this.renderable = new (me.Renderable.extend({
            init : function () {
                this._super(me.Renderable, "init", [0, 0, BULLET_SIZE, BULLET_SIZE]);
            },
            destroy : function () {},
            draw : function (renderer) {
                var color = renderer.getColor();
                renderer.setColor('#000');
                renderer.fillRect(0, 0, this.width, this.height);
                renderer.setColor(color);
            }
        }));
        this.alwaysUpdate = true;
    },

    update : function (time) {
      if (this.__DIRECTION__) {
        if (this.__DIRECTION__ === 'down') {
          this.pos.y += this.vel * time / 1000;
          if (this.pos.y + this.height >= HEIGHT) {
              me.game.world.removeChild(this);
          }
        } else if (this.__DIRECTION__ === 'up') {
          this.pos.y -= this.vel * time / 1000;
          if (this.pos.y - this.height <= 0) {
              me.game.world.removeChild(this);
          }
        } else if (this.__DIRECTION__ === 'right') {
          this.pos.x += this.vel * time / 1000;
          if (this.pos.x + this.width >= WIDTH) {
              me.game.world.removeChild(this);
          }
        } else if (this.__DIRECTION__ === 'left') {
          this.pos.x -= this.vel * time / 1000;
          if (this.pos.x - this.width <= 0) {
              me.game.world.removeChild(this);
          }
        }
      }
      me.collision.check(this);
      return true;
    }
});

function follow(plyr, oldX, oldY) {
  const diffX = plyr.pos.x - oldX;
  if (plyr.pos.x > 120 && plyr.pos.x >= oldX && plyr.pos.x < (WIDTH - 120)) {
    me.game.viewport.move(diffX, 0);
  } else if (plyr.pos.x > 120 && plyr.pos.x <= oldX && plyr.pos.x < (WIDTH - 120)) {
    if (me.game.viewport.left > 0) {
      me.game.viewport.move(diffX, 0);
    }
  }
  const diffY = plyr.pos.y - oldY;
  if (plyr.pos.y > 160 && plyr.pos.y >= oldY && plyr.pos.y < (HEIGHT - 160)) {
    me.game.viewport.move(0, diffY);
  } else if (plyr.pos.y > 160 && plyr.pos.y <= oldY && plyr.pos.y < (HEIGHT - 160)) {
    if (me.game.viewport.top > 0) {
      me.game.viewport.move(0, diffY);
    }
  }
  // console.log('CAM x', me.game.viewport.left, 'CAM y', me.game.viewport.top);
}

function rotateTank(tank, to) {
  const dirAngle = {up: 0, right: 90, down: 180, left: 270};
  const x = dirAngle[to] - dirAngle[tank.__DIRECTION__];
  tank.__DIRECTION__ = to;
  tank.rotate(x * Math.PI / 180);
  return to;
}

me.device.onReady(function onReady() {
  game.onload();
});
