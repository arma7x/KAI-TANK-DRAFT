const BULLET_SIZE = 4;
var myId = null;
var currentPlayer = null;
var othersPlayer = {};
var socket = null;


var game = {
  resources: [
    { name: "greentank", type: "image", "src": "tank-green.png",  }
  ],
  loaded: function() {
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
      let data = JSON.parse(evt.data);
      if (data.init) {
        myId = data.init
        currentPlayer = me.game.world.addChild(me.pool.pull("greentank"));
        currentPlayer.pos.x = me.Math.clamp(data.position.x, currentPlayer.minX, currentPlayer.maxX);
        currentPlayer.pos.y = me.Math.clamp(data.position.y, currentPlayer.minY, currentPlayer.maxY);
        if (currentPlayer.__DIRECTION__ !== data.position.direction) {
          rotateTank(currentPlayer, data.position.direction);
        }
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
    };
    socket.onopen = () => {
      socket.send(JSON.stringify({ping: true}));
    }
  },
  onload: function () {
    if (!me.video.init(240, 320, {parent: document.body, scale: "auto", renderer: me.video.CANVAS})) {
      alert("Your browser does not support HTML5 Canvas :(");
      return;
    }

    me.audio.init("ogg");
    me.loader.preload(game.resources, this.loaded.bind(this));
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

  if (action === "left") {
    if (currentPlayer.__DIRECTION__ !== 'left') {
      rotateTank(currentPlayer, 'left');
    } else
      currentPlayer.pos.x -= currentPlayer.vel * time / 1000;
  } else if (action === "right"){
    if (currentPlayer.__DIRECTION__ !== 'right') {
      rotateTank(currentPlayer, 'right');
    } else
      currentPlayer.pos.x += currentPlayer.vel * time / 1000;
  } else if (action === "up") {
    if (currentPlayer.__DIRECTION__ !== 'up') {
      rotateTank(currentPlayer, 'up');
    } else
      currentPlayer.pos.y -= currentPlayer.vel * time / 1000;
  } else if (action === "down") {
    if (currentPlayer.__DIRECTION__ !== 'down') {
      rotateTank(currentPlayer, 'down');
    } else
      currentPlayer.pos.y += currentPlayer.vel * time / 1000;
  }

  me.Math.clamp(currentPlayer.pos.y, currentPlayer.minY, currentPlayer.maxY);
  me.Math.clamp(currentPlayer.pos.x, currentPlayer.minX, currentPlayer.maxX);

  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({move: [currentPlayer.pos.x, currentPlayer.pos.y, currentPlayer.__DIRECTION__]}));
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
    this.scale(0.75, 0.75);
    this.vel = 65;
    this.minX = (this.width / 2);
    this.maxX = me.game.viewport.width - (this.height / 2);
    this.minY = (this.height / 2);
    this.maxY = me.game.viewport.height - (this.height / 2);
  },
  update: function(time) {
    this._super(me.Sprite, "update", [time]);
    return true;
  }
});

game.Bullet = me.Entity.extend({
    init: function (x, y) {
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

    update: function (time) {
      if (this.__DIRECTION__) {
        if (this.__DIRECTION__ === 'down') {
          this.pos.y += this.vel * time / 1000;
          if (this.pos.y + this.height >= me.game.viewport.height) {
              me.game.world.removeChild(this);
          }
        } else if (this.__DIRECTION__ === 'up') {
          this.pos.y -= this.vel * time / 1000;
          if (this.pos.y - this.height <= 0) {
              me.game.world.removeChild(this);
          }
        } else if (this.__DIRECTION__ === 'right') {
          this.pos.x += this.vel * time / 1000;
          if (this.pos.x + this.width >= me.game.viewport.width) {
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

function rotateTank(tank, to) {
  const dirAngle = {up: 0, right: 90, down: 180, left: 270};
  const x = dirAngle[to] - dirAngle[tank.__DIRECTION__];
  tank.__DIRECTION__ = to;
  tank.rotate(x * Math.PI / 180);
}

me.device.onReady(function onReady() {
  game.onload();
});
