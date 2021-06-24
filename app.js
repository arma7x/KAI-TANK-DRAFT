var myId = parseInt(Math.random() * 1e10 + 1001);
var socket = null;
var currentPlayer = null;

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
  },
  onload: function () {
    if (!me.video.init(240, 320, {parent: document.body, scale: "auto", renderer: me.video.CANVAS})) {
      alert("Your browser does not support HTML5 Canvas :(");
      return;
    }

    me.audio.init("ogg");
    me.loader.preload(game.resources, this.loaded.bind(this));
    //socket = io("https://shangul.de1.hashbang.sh/",
      //{
        //path: "/server",
        //transports: ["websocket"],
      //}
    //);
  },
};


game.PlayScreen = me.Stage.extend({
  onResetEvent: function() {
    currentPlayer = me.game.world.addChild(me.pool.pull("greentank"));
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
        bX = currentPlayer.pos.x - 3, bY = currentPlayer.pos.y + (currentPlayer.height / 2), bD = 'down';
      else
        bX = currentPlayer.pos.x - 3, bY = currentPlayer.pos.y - (currentPlayer.height / 2) - 3, bD = 'up';
    } else {
      if (currentPlayer.__DIRECTION__ === 'right')
        bX = currentPlayer.pos.x + (currentPlayer.width / 2), bY = currentPlayer.pos.y - 3, bD = 'right';
      else
        bX = currentPlayer.pos.x + (currentPlayer.width / 2) - 3 - currentPlayer.width, bY = currentPlayer.pos.y - 3, bD = 'left';
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
    this.vel = 65;
    this.minX = (this.width / 2);
    this.maxX = me.game.viewport.width - (this.height / 2);
    this.minY = (this.height / 2);
    this.maxY = me.game.viewport.height - (this.height / 2);
    //socket.on("pos", function(data) {
    //  this.pos.x = data[0];
    //  this.pos.y = data[1];
    //});
  },
  update: function(time) {
    this._super(me.Sprite, "update", [time]);
    if (me.input.isKeyPressed("left")) {
      if (this.__DIRECTION__ !== 'left') {
        rotateTank(this, 'left');
      } else
        this.pos.x -= this.vel * time / 1000;
    } else if (me.input.isKeyPressed("right")){
      if (this.__DIRECTION__ !== 'right') {
        rotateTank(this, 'right');
      } else
        this.pos.x += this.vel * time / 1000;
    } else if (me.input.isKeyPressed("up")) {
      if (this.__DIRECTION__ !== 'up') {
        rotateTank(this, 'up');
      } else
        this.pos.y -= this.vel * time / 1000;
    } else if (me.input.isKeyPressed("down")) {
      if (this.__DIRECTION__ !== 'down') {
        rotateTank(this, 'down');
      } else
        this.pos.y += this.vel * time / 1000;
    }

    this.pos.y = me.Math.clamp(this.pos.y, this.minY, this.maxY);
    this.pos.x = me.Math.clamp(this.pos.x, this.minX, this.maxX);
    //socket.emit("move", {data: [this.pos.x - new_x, this.pos.y - new_y]});

    return true;
  }
});

game.Bullet = me.Entity.extend({
    init : function (x, y) {
        this._super(me.Entity, "init", [x, y, { width: 6, height: 6 }]);
        this.vel = 250;
        this.body.collisionType = me.collision.types.PROJECTILE_OBJECT;
        this.renderable = new (me.Renderable.extend({
            init : function () {
                this._super(me.Renderable, "init", [0, 0, 6, 6]);
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
