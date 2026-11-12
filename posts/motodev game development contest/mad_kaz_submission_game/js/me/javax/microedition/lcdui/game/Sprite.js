js2me.createClass({
    _init$Ljavax_microedition_lcdui_Image_II$V:function(image,w,h){
        this.image=image;this.width=w;this.height=h;this.transform=0;this.x=0;this.y=0;
        this.columns=Math.floor(image.element.width/w);this.sequence=Array.from({length:this.columns*Math.floor(image.element.height/h)},function(_,i){return i});this.frame=0;
    },
    $setFrameSequence$_I$V:function(sequence){this.sequence=sequence?sequence.slice():Array.from({length:this.columns*Math.floor(this.image.element.height/this.height)},function(_,i){return i});this.frame=0;},
    $nextFrame$$V:function(){this.frame=(this.frame+1)%this.sequence.length;},
    $prevFrame$$V:function(){this.frame=(this.frame+this.sequence.length-1)%this.sequence.length;},
    $setFrame$I$V:function(frame){this.frame=frame;},
    $getFrame$$I:function(){return this.frame;},

	$TRANS_NONEI: 0,
	$TRANS_ROT90I: 5,
	$TRANS_ROT180I: 3,
	$TRANS_ROT270I: 6,
	$TRANS_MIRRORI: 2,
	$TRANS_MIRROR_ROT90I: 7,
	$TRANS_MIRROR_ROT180I: 1,
	$TRANS_MIRROR_ROT270I:  4,
	/*
	 * public Sprite(Image image)
	 */
	_init$Ljavax_microedition_lcdui_Image_$V: function (image) {
		this.image = image;
		this.width = image.element.width;
		this.height = image.element.height;
		this.transform = 0;
	},
	/*
	 * public void setTransform(int transform)
	 */
	$setTransform$I$V: function (transform) {
		this.transform = transform;
	},
	/*
	 * 
	 */
	$getWidth$$I: function () {
		if (this.transform != this.$TRANS_ROT90I && this.transform != this.$TRANS_ROT270I &&
			this.transform != this.$TRANS_MIRROR_ROT90I && this.transform != this.$TRANS_MIRROR_ROT270I) {
			return this.width;
		} else {
			return this.height;
		}
	},
	/*
	 * public final void paint(Graphics g)
	 */
	$paint$Ljavax_microedition_lcdui_Graphics_$V: function (graphics) {
		//TODO: animation and stuff
		if (graphics == null) {
			throw new javaRoot.$java.$lang.$NullPointerException();
		}
		graphics.$drawRegion$Ljavax_microedition_lcdui_Image_IIIIIIII$V(this.image, ((this.sequence?this.sequence[this.frame]:0)%(this.columns||1))*this.width, Math.floor((this.sequence?this.sequence[this.frame]:0)/(this.columns||1))*this.height, this.width, this.height,
			this.transform, this.x, this.y, 0);
	},
	superClass: 'javaRoot.$javax.$microedition.$lcdui.$game.$Layer'
});

