# Serial to MQTT gateway MicroPython application software
# 2023 Samuel Ramrajkar
#
# 2023-Oct-17 - v1 - Initial implementation

# Import required libraries
import uasyncio as asyncio
from base64 import b64encode, b64decode
from machine import UART
from wifi_mgr import wifi_connect

uart = UART(1, 9600, tx=16, rx=15, rts=17, mode=UART.MODE_RS485, timeout=10, timeout_char=10)
ser_to_mqtt = list()

async def sender():
    swriter = asyncio.StreamWriter(uart, {})
    while True:
        if(len(ser_to_mqtt) > 0):
            swriter.write(b64decode(ser_to_mqtt.pop(0)))
            await swriter.drain()
        await asyncio.sleep(2)

async def receiver():
    sreader = asyncio.StreamReader(uart)
    while True:
        res = await sreader.read(1024)
        if(None != res):
            print('Received', res)
            ser_to_mqtt.append(b64encode(res))

async def main():
    asyncio.create_task(sender())
    asyncio.create_task(receiver())
    asyncio.create_task(wifi_connect())
    while True:
        await asyncio.sleep(1)

def app_entry():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()
        print('as_demos.auart.test() to run again.')

app_entry()
