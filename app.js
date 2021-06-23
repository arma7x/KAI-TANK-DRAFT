var game = {
  resources: [
    { name: "greentank", type: "image", "src": "tank-green.png" }
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


game.PlayScreen = me.ScreenObject.extend({
  onResetEvent: () => {
    me.game.world.addChild(me.pool.pull("greentank"));
    me.game.world.addChild(new me.ColorLayer("background", "#000"), 0);
  }
});

game.Tank = me.Sprite.extend({
  init: function() {
    this._super(me.Sprite, "init", [
      me.game.viewport.width / 2 - 16, // 16 = 32 / 2 where 32 is width
      me.game.viewport.height - 16,
      { image: me.loader.getImage("greentank"), width: 32, height: 32 }
    ]);
  }
});
