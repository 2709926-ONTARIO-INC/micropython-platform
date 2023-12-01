import network
import uasyncio as asyncio

async def wifi_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('PoojaSam7855', '7855internet')
        while not sta_if.isconnected():
            await asyncio.sleep(2)
    print('network config:', sta_if.ifconfig())