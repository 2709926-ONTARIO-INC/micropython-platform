import machine
import time
from ktd2027 import KTD2026
# Usage
i2c = machine.I2C(scl=machine.Pin(1), sda=machine.Pin(0))
led_driver = KTD2026(i2c)

# Example operations
while True:
        #Turn On LED1, LED2,LED3
        led_driver.led_ch_enable(led_driver.LED1, True)
        led_driver.led_ch_enable(led_driver.LED2, True)
        led_driver.led_ch_enable(led_driver.LED3, True)
        led_driver.led_level(led_driver.LED1, 0x10)
        led_driver.led_level(led_driver.LED2, 0x40)
        led_driver.led_level(led_driver.LED3, 0x10)
        time.sleep(5)
        led_driver.led_ch_enable(led_driver.LED1, False)
        led_driver.led_ch_enable(led_driver.LED2, False)
        led_driver.led_ch_enable(led_driver.LED3, False)
        time.sleep(5)