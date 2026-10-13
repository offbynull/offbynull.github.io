js2me.createClass({
	/*
	 * protected GameCanvas(boolean suppressKeyEvents)
	 */
	_init$Z$V : function (suppressKeyEvents) {
		javaRoot.$javax.$microedition.$lcdui.$Canvas.prototype._init$$V.apply(this);
        this.buffer=document.createElement('canvas');this.buffer.width=js2me.config.width;this.buffer.height=js2me.config.fullHeight;
	},
	/*
	 * protected Graphics getGraphics()
	 */
	$getGraphics$$Ljavax_microedition_lcdui_Graphics_: function () {
		var graphics = new javaRoot.$javax.$microedition.$lcdui.$Graphics(this.buffer);
		return graphics;
	},
	/*
	 * public void flushGraphics(int x, int y, int width, int height)
	 */
	$flushGraphics$$V: function () {
		var context=this.element.getContext('2d');context.setTransform(1,0,0,1,0,0);context.clearRect(0,0,this.element.width,this.element.height);context.drawImage(this.buffer,0,0);
	},
	/*
	 * public int getKeyStates()
	 */
	$getKeyStates$$I: function () {
		var gameState = this.gameState;
		this.gameState = 0;
        for(var key in this.keysState){if(this.keysState[key]){var action=this.gameActionMapping[key];if(action!=null)this.gameState|=1<<action;}}
		return gameState;
	},
	superClass: 'javaRoot.$javax.$microedition.$lcdui.$Canvas'
});

