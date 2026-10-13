# Mad Kaz — portable deployment

## Website
Upload the extracted contents to any static HTTPS host. `index.html` must be at the site's root or the root of your chosen subfolder. No build, Node server, API, account, CDN or external game assets are required. All runtime files are bundled.

After the first online visit, wait for **Offline ready**. Then this same URL can load and play without internet, including its music and dynamically loaded emulator classes. Browser storage must remain enabled. Clearing site data or browser cache removes offline files and saved progress. Browser storage eviction can also remove cached files. Revisit online to restore the cache.

Keep `sw.js` alongside `index.html`, served as JavaScript. HTTPS is required for website offline caching. Relative paths support deployment in a subfolder. If your host enforces a Content Security Policy, permit the bundled scripts and original page's inline script/style; do not block dynamic same-origin script loading.

## Fully offline on your computer
Install Python 3 beforehand, unzip this bundle, and run `python3 serve.py` (Windows: `py -3 serve.py`, or double-click `start-offline.bat`). It opens http://localhost:8080/ and uses only the files in this folder. Keep the terminal open while playing. No initial internet visit is required for this local-server option. Opening `index.html` directly using file:// is not supported by the game's loader.

## Controls and saving
Arrows move and navigate; Enter/Space selects; 1 or the Pause button pauses; Z/X are soft keys. Touch controls are included. Complete the original setup on first launch. Progress saves separately for each browser/origin; it does not automatically transfer from the previously hosted copy.

## Included content
The unmodified original game JAR contains all six zones and 34 level entries. Its eight modes, original MIDI scores and emulator are included. MIDI instruments are synthesized and may sound different from a Motorola handset. Original Bluetooth sharing and old download services are unsupported.

Game source: https://github.com/offbynull/mad_kaz
Emulator source: https://github.com/szatkus/js2me
Licenses: EMULATOR-LICENSE and SYNTH-LICENSE. Upstream game README declares public domain.

## Updating your deployment
The generated service worker cache version reflects all bundled runtime files. For subsequent code changes, regenerate this bundle using scripts/bundle-offline.py from the source project rather than editing a deployed cached file without changing the cache version. Close/reopen existing game tabs when updating.
