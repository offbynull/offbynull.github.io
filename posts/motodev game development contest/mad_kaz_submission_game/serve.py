#!/usr/bin/env python3
"""Serve the bundled game locally, with no internet connection required."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from pathlib import Path
import webbrowser
url="http://localhost:8080/"
server=ThreadingHTTPServer(("127.0.0.1",8080),partial(SimpleHTTPRequestHandler,directory=str(Path(__file__).resolve().parent)))
print("Mad Kaz: "+url+" (keep this window open; Ctrl+C stops the server)",flush=True)
webbrowser.open(url)
try: server.serve_forever()
except KeyboardInterrupt: pass
finally: server.server_close()
