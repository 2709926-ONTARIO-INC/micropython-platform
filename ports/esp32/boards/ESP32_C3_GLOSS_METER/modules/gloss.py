import uasyncio as asyncio
import machine
from ktd2027 import KTD2026

class DeviceController:
    def __init__(self, adc, led_controller):
        self.adc = adc
        self.led_controller = led_controller
        # Define the command dictionary
        self.commands = {
            '1': self.enable_led,
            '2': self.set_brightness,
            '3': self.read_adc,
            '4': self.disable_led,
            '5': self.exit_program
        }

    def menu(self):
        menu_text = """
        Device Control Menu:
        1. Enable LED
        2. Set LED Brightness
        3. Read ADC Value
        4. Disable LED
        5. Exit
        """
        print(menu_text)

    async def enable_led(self):
        led_number = int(input("Enter LED number to enable (1-4): "))
        self.led_controller.led_ch_enable(led_number - 1, True)
        print(f"LED {led_number} enabled.")
        
    async def disable_led(self):
        led_number = int(input("Enter LED number to disable (1-4): "))
        self.led_controller.led_ch_enable(led_number - 1, False)
        print(f"LED {led_number} disabled.")

    async def set_brightness(self):
        led_number = int(input("Enter LED number to set brightness (1-4): "))
        brightness = int(input("Enter brightness level (0-255): "))
        self.led_controller.set_brightness(led_number - 1, brightness)
        print(f"Brightness for LED {led_number} set to {brightness}.")

    async def read_adc(self):
        value = self.adc.read()
        print(f"Current ADC value: {value}")

    async def exit_program(self):
        print("Exiting program.")
        asyncio.get_event_loop().stop()

    async def run(self):
        while True:
            self.menu()
            choice = input("Enter your choice: ")
            command = self.commands.get(choice)
            if command:
                await command()
            else:
                print("Invalid option, please try again.")

# Assuming ADC and LEDController classes exist
async def main():
    adc = None
    i2c = machine.I2C(scl=machine.Pin(1), sda=machine.Pin(0))
    led_controller = KTD2026(i2c)
    controller = DeviceController(adc, led_controller)
    await controller.run()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
