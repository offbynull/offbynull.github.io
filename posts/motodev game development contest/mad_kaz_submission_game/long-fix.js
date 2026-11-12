/* Java long arithmetic uses exactly 64 bits, never floating-point intermediates. */
(function(){
 const unsigned=a=>(BigInt(a.hi>>>0)<<32n)|BigInt(a.lo>>>0);
 const signed=a=>BigInt.asIntN(64,unsigned(a));
 const words=n=>{n=BigInt.asUintN(64,n);return {hi:Number(n>>32n),lo:Number(n&0xffffffffn)}};
 js2me.longToString=a=>signed(a).toString();
 js2me.ladd=(a,b)=>words(unsigned(a)+unsigned(b));
 js2me.lsub=(a,b)=>words(unsigned(a)-unsigned(b));
 js2me.lmul=(a,b)=>words(unsigned(a)*unsigned(b));
 js2me.lneg=a=>words(-signed(a));
 js2me.lcmp=(a,b)=>signed(a)<signed(b)?-1:signed(a)>signed(b)?1:0;
 js2me.lshl=(a,n)=>words(unsigned(a)<<BigInt(n&63));
 js2me.lshr=(a,n,arithmetic)=>words((arithmetic?signed(a):unsigned(a))>>BigInt(n&63));
 js2me.lxor=(a,b)=>words(unsigned(a)^unsigned(b));
 js2me.ldiv=(a,b)=>({div:words(signed(a)/signed(b)),rem:words(signed(a)%signed(b))});
})();
