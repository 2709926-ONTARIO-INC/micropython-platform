import network
from web_srv import web
import uasyncio as asyncio
import frozen_www

app = web.App(host='0.0.0.0', port=80)

# root route handler
@app.route('/')
async def handler(r, w):
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/html; charset=utf-8\r\n')
    w.write(b'\r\n')
    with open('/www/index.html', 'r') as f:
        w.write(f.read())
    await w.drain()
    
@app.route('/wifi.html')
async def handler(r, w):
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/html; charset=utf-8\r\n')
    w.write(b'\r\n')
    with open('/www/wifi.html', 'r') as f:
        w.write(f.read())
    await w.drain()

@app.route('/ethernet.html')
async def handler(r, w):
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/html; charset=utf-8\r\n')
    w.write(b'\r\n')
    with open('/www/ethernet.html', 'r') as f:
        w.write(f.read())
    await w.drain()
    
@app.route('/mqtt.html')
async def handler(r, w):
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/html; charset=utf-8\r\n')
    w.write(b'\r\n')
    with open('/www/mqtt.html', 'r') as f:
        w.write(f.read())
    await w.drain()
    
@app.route('/4g-lte.html')
async def handler(r, w):
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/html; charset=utf-8\r\n')
    w.write(b'\r\n')
    with open('/www/4g-lte.html', 'r') as f:
        w.write(f.read())
    await w.drain()
