'use strict';
js2me.config.width=176;js2me.config.height=205;js2me.config.fullHeight=220;js2me.config.workers=false;
js2me.engine='js/program_zazu.js';
js2me.setFullscreen=function(){};
js2me.showError=function(message){document.getElementById('alert').style.display='block';document.getElementById('alert').textContent=String(message);};
const held=new Map(), keyMap={ArrowUp:-1,ArrowDown:-2,ArrowLeft:-3,ArrowRight:-4,Enter:-5,' ':-5,z:-6,Z:-6,x:-7,X:-7,'*':42,'#':35};
function press(id,key){if(!js2me.manifest||held.has(id))return;held.set(id,key);js2me.sendKeyPressEvent(key);}
function release(id){const key=held.get(id);if(key!==undefined){held.delete(id);if(![...held.values()].includes(key))js2me.sendKeyReleasedEvent(key);}}
function releaseAll(){for(const id of [...held.keys()])release(id);}
document.addEventListener('keydown',e=>{const key=keyMap[e.key]??(/^\d$/.test(e.key)?e.key.charCodeAt(0):undefined);if(key!==undefined){e.preventDefault();press(e.code,key);}});
document.addEventListener('keyup',e=>release(e.code));window.addEventListener('blur',releaseAll);document.addEventListener('visibilitychange',()=>{if(document.hidden)releaseAll();});
for(const button of document.querySelectorAll('[data-key]')){button.addEventListener('pointerdown',e=>{e.preventDefault();button.setPointerCapture(e.pointerId);press('pointer'+e.pointerId,+button.dataset.key)});for(const type of ['pointerup','pointercancel','lostpointercapture'])button.addEventListener(type,e=>release('pointer'+e.pointerId));}
document.getElementById('restart').onclick=()=>location.reload();
document.getElementById('start').onclick=async function(){this.disabled=true;this.textContent='Playing';document.getElementById('screen').textContent='Loading original game…';try{window.madKazSynth=new WebAudioTinySynth({quality:1,voices:64});await window.madKazSynth.getAudioContext().resume();}catch(e){console.warn('Audio unavailable',e);}try{const response=await fetch('game.jar');if(!response.ok)throw new Error('Game download failed');js2me.launchJAR(await response.blob());document.getElementById('status').textContent='Complete the original first-run setup with OK. Progress stays in this browser.';}catch(e){js2me.showError(e.message);this.disabled=false;this.textContent='Try again';}};
