# Serial to MQTT gateway MicroPython application software
# 2023 Samuel Ramrajkar
#
# 2023-Oct-17 - v1 - Initial implementation

# Import required libraries
import uasyncio as asyncio
from machine import UART

uart = UART(1, 9600, tx=16, rx=15, rts=17, mode=UART.MODE_RS485, timeout=0, timeout_char=10)

async def sender():
    swriter = asyncio.StreamWriter(uart, {})
    while True:
        swriter.write('Hello uart\n')
        await swriter.drain()
        await asyncio.sleep(2)

async def receiver():
    sreader = asyncio.StreamReader(uart)
    while True:
        res = await sreader.read()
        if(None != res):
            print('Received', res)

async def main():
    asyncio.create_task(sender())
    asyncio.create_task(receiver())
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