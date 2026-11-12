(function(){
 const status=document.getElementById('offline-status');
 if(!('serviceWorker' in navigator)||!window.isSecureContext){status.textContent='Offline caching requires HTTPS or localhost. All game files are bundled locally.';return;}
 navigator.serviceWorker.register('./sw.js').then(()=>navigator.serviceWorker.ready).then(()=>{status.textContent='Offline ready — this game can now load without an internet connection.';}).catch(()=>{status.textContent='Offline cache unavailable. You can still play using the included local server.';});
})();
