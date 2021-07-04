const BULLET_SIZE = 4;
const WIDTH = 240, HEIGHT = 320;
const TILES = 20;
const DEBUG = true;

var myId = null;
var currentPlayer = null;
var shadowPlayer = null;
var othersPlayer = {};
var bullets = {};
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
  } else if (type === "3") {
    encodedBinary = pb_root.Bullet.encode(msg).finish();
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
    message = pb_root.BulletBroadcast.decode(buffer);
  } else if (type === "2") {
    message = pb_root.Init.decode(buffer);
  } else if (type === "3") {
    message = pb_root.Voice.decode(buffer);
  } else if (type === "4") {
    message = pb_root.Disconnect.decode(buffer);
  } else if (type === "5") {
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
    { name: "map", type: "image", "src": "/map.png", },
    { name: "greentank", type: "image", "src": "/tanks/tile000.png", },
    { name: "grass_1", type: "image", "src": "/tiles/tile000.png", },
    { name: "grass_2", type: "image", "src": "/tiles/tile001.png", },
    { name: "grass_3", type: "image", "src": "/tiles/tile002.png", },
    { name: "grass_4", type: "image", "src": "/tiles/tile003.png", },
    { name: "grass_5", type: "image", "src": "/tiles/tile004.png", },
  ],
  loaded: function() {
    me.game.world.resize(WIDTH, HEIGHT);
    me.pool.register("greentank", game.Tank);
    me.pool.register("grass", game.Tank);
    me.pool.register("grass", game.GrassTile);
    me.pool.register("bullet", game.Bullet);
    me.pool.register("map", game.Map);
    this.playScreen = new game.PlayScreen();
    me.state.set(me.state.PLAY, this.playScreen);
    me.state.change(me.state.PLAY);

    let host = "shangul.de1.hashbang.sh"
    if (document.location.host != host)
      host = `ws://${document.location.host.split(':')[0]}:3000`
    else
      host = "wss://shangul.de1.hashbang.sh/server"
    socket = new WebSocket(host);
    socket.onmessage = evt => {
      let dataP = decodeMessage(evt.data);
      if (dataP._type === "0") {
        for (let p in dataP.players) {
          p = parseInt(p)
          const move = dataP.players[p];
          if (p !== myId) {
            const dir = pb_root.Direction.__proto__[move.dir].toLowerCase();
            if (othersPlayer[p] == null) {
              othersPlayer[p] = me.game.world.addChild(me.pool.pull("greentank"));
              othersPlayer[p].__ID__ = p
            }
            if (othersPlayer[p]) {
              if (othersPlayer[p].__DIRECTION__ !== dir) {
                rotateTank(othersPlayer[p], dir);
              }
              othersPlayer[p].pos.x = me.Math.clamp(move.pos.x, othersPlayer[p].minX, othersPlayer[p].maxX);
              othersPlayer[p].pos.y = me.Math.clamp(move.pos.y, othersPlayer[p].minY, othersPlayer[p].maxY);
            }
          } else if (DEBUG && shadowPlayer && p === myId) {
            //setTimeout(() => {
              const dir = pb_root.Direction.__proto__[move.dir].toLowerCase();
              if (shadowPlayer.__DIRECTION__ !== dir) {
                rotateTank(shadowPlayer, dir);
              }
              shadowPlayer.pos.x = me.Math.clamp(move.pos.x, shadowPlayer.minX, shadowPlayer.maxX);
              shadowPlayer.pos.y = me.Math.clamp(move.pos.y, shadowPlayer.minY, shadowPlayer.maxY);
            //}, 65); // stimulate lag
          }
        }
      }
      if (dataP._type === "1") {
        // bullets
        for (var x in dataP.bullets) {
          const bullet = dataP.bullets[x];
          if (bullets[bullet.id] == null) {
            const dir = pb_root.Direction.__proto__[bullet.dir].toLowerCase();
            const b = me.game.world.addChild(me.pool.pull("bullet", bullet.pos.x, bullet.pos.y))
            b.__HITTER__ = bullet.shooter;
            b.__DIRECTION__ = dir;
            bullets[bullet.id] = b;
            // console.log("Add", bullet.id);
          } else if (bullet.pos.x === -1 || bullet.pos.y === -1) {
            // console.log("Remove", bullet.id);
            me.game.world.removeChild(bullets[bullet.id]);
            delete bullets[bullet.id];
          }
        }
      }
      if (dataP._type === "2") {
        myId = dataP.id
        currentPlayer = me.game.world.addChild(me.pool.pull("greentank"));
        currentPlayer.__ID__ = myId
        currentPlayer.pos.x = me.Math.clamp(dataP.move.pos.x, currentPlayer.minX, currentPlayer.maxX);
        currentPlayer.pos.y = me.Math.clamp(dataP.move.pos.y, currentPlayer.minY, currentPlayer.maxY);
        const dir = pb_root.Direction.__proto__[dataP.move.dir].toLowerCase();
        if (currentPlayer.__DIRECTION__ !== dir) {
          rotateTank(currentPlayer, dir);
        }
        follow(currentPlayer)
        if (DEBUG) {
          shadowPlayer = me.game.world.addChild(me.pool.pull("greentank"));
          shadowPlayer.body.collisionType = me.collision.types.NO_OBJECT;
          shadowPlayer.__ID__ = 'DEBUG'
          shadowPlayer.pos.x = me.Math.clamp(dataP.move.pos.x, shadowPlayer.minX, shadowPlayer.maxX);
          shadowPlayer.pos.y = me.Math.clamp(dataP.move.pos.y, shadowPlayer.minY, shadowPlayer.maxY);
          const dir = pb_root.Direction.__proto__[dataP.move.dir].toLowerCase();
          if (shadowPlayer.__DIRECTION__ !== dir) {
            rotateTank(shadowPlayer, dir);
          }
          follow(shadowPlayer)
        }
      }
      if (dataP._type === "4") {
        if (othersPlayer[dataP.id]) {
          me.game.world.removeChild(othersPlayer[dataP.id]);
          delete othersPlayer[dataP.id];
        }
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
    //for (var y=(TILES/2);y<=HEIGHT;y=y+TILES) {
      //for (var x=(TILES/2);x<=WIDTH;x=x+TILES) {
        //me.game.world.addChild(me.pool.pull("grass", x, y))
      //}
    //}
    // less memory
    me.game.world.addChild(me.pool.pull("map", WIDTH/2, HEIGHT/2))
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

var reloading = false;
me.event.subscribe(me.event.KEYDOWN, function (action, keyCode, edge) {
  const yAxis = ['up', 'down'];
  if (keyCode === 32 && !reloading) {
    reloading = true;
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(encodeMessage("3", {}));
    }
    setTimeout(() => {
      reloading = false
    }, 100);
  }

});

game.Map = me.Sprite.extend({
  init: function(x, y) {
    this._super(me.Sprite, "init", [
      x,
      y,
      {
        image: me.loader.getImage('map'),
      }
    ]);
  }
});

game.GrassTile = me.Sprite.extend({
  init: function(x = (TILES/2), y = (TILES/2)) {
    const n = Math.floor(Math.random() * 5) + 1;
    this._super(me.Sprite, "init", [
      x,
      y,
      {
        image: me.loader.getImage(`grass_${n}`),
      }
    ]);
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
    this.vel = 65;
    this.minX = (this.width / 2);
    this.maxX = WIDTH - (this.height / 2);
    this.minY = (this.height / 2);
    this.maxY = HEIGHT - (this.height / 2);

    this.body = new me.Body(this);
    // add a default collision shape
    this.body.addShape(new me.Rect(0, 0, this.width, this.height));
    // configure max speed and friction
    this.body.setFriction(0.4, 0);
    // enable physic collision (off by default for basic me.Renderable)
    this.isKinematic = false;
    this.body.setVelocity(0, 0);
    this.body.setMaxVelocity(0, 0);
    this.body.collisionType = me.collision.types.ENEMY_OBJECT;
  },
  onCollision: function (res, other) {
    if (other.body.collisionType === me.collision.types.ENEMY_OBJECT) {
      return true;
    }
  },
  __onHitted__: function(hitter) {
    // console.log(this.__ID__, 'hitted by', hitter);
  },
  update: function(time) {
    this._super(me.Sprite, "update", [time]);

    if (this.__ID__ === myId) {
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
        if (!me.collision.check(this))
          follow(this);
      }
    }
    return true;
  }
});

game.Bullet = me.Entity.extend({
    init : function (x, y) {
        this._super(me.Entity, "init", [x, y, { width: BULLET_SIZE, height: BULLET_SIZE }]);
        this.vel = 150;
        this.body.collisionType = me.collision.types.NO_OBJECT;
        this.renderable = new (me.Renderable.extend({
            init : function () {
                this._super(me.Renderable, "init", [0, 0, BULLET_SIZE, BULLET_SIZE]);
            },
            destroy : function () {},
            draw : function (renderer) {
                var color = renderer.getColor();
                renderer.setColor('#FF8200');
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
        } else if (this.__DIRECTION__ === 'up') {
          this.pos.y -= this.vel * time / 1000;
        } else if (this.__DIRECTION__ === 'right') {
          this.pos.x += this.vel * time / 1000;
        } else if (this.__DIRECTION__ === 'left') {
          this.pos.x -= this.vel * time / 1000;
        }
      }
      // SERVER-SIDE
       https://www.khanacademy.org/math/geometry/hs-geo-analytic-geometry/hs-geo-distance-and-midpoints/v/distance-formula
      for (var t in othersPlayer) {
        const v = Math.sqrt(Math.pow((this.pos.x - othersPlayer[t].pos.x), 2) + Math.pow((this.pos.y - othersPlayer[t].pos.y), 2));
        if (v <= 10) {
          console.log(v);
          //othersPlayer[t].__onHitted__(this.__HITTER__);
          //me.game.world.removeChild(othersPlayer[t]);
          //me.game.world.removeChild(this);
          //delete othersPlayer[othersPlayer[t].__ID__];
        }
      }
      return true;
    }
});

function follow(plyr) {

  var mX = plyr.pos.x - (240 / 2);
  mX = mX <= (240 / 2) ? mX - 1 : mX;
  mX = mX <= 0 ? 0 : mX;
  if ((WIDTH - plyr.pos.x) <= (240 / 2)) {
    mX = WIDTH - 240
  }

  var mY = plyr.pos.y - (320 / 2);
  mY = mY <= (320 / 2) ? mY - 1 : mY;
  mY = mY <= 0 ? 0 : mY;
  if ((HEIGHT - plyr.pos.y) <= (320 / 2)) {
    mY = HEIGHT - 320
  }

  me.game.viewport.moveTo(mX, mY)
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
