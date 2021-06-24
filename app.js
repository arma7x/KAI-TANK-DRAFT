var game = {
  resources: [
    { name: "greentank", type: "image", "src": "tank-green.png",  }
  ],
  loaded: function() {
    me.pool.register("greentank", game.Tank);
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
  },
};


game.PlayScreen = me.Stage.extend({
  onResetEvent: function() {
    me.game.world.addChild(me.pool.pull("greentank"));
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
    this.minX = (this.height / 2);
    this.maxX = me.game.viewport.width - (this.height / 2);
    this.minY = (this.height / 2);
    this.maxY = me.game.viewport.height - (this.height / 2);
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

    return true;
  }
});

function rotateTank(tank, to) {
  const dirAngle = {up: 0, right: 90, down: 180, left: 270};
  const x = dirAngle[to] - dirAngle[tank.__DIRECTION__];
  tank.__DIRECTION__ = to;
  tank.rotate(x * Math.PI / 180);
}
