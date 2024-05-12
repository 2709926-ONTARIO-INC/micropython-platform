import uasyncio as asyncio
import machine
from ktd2027 import KTD2026
from ADS1115 import ADS1115
from ADS1115 import ADS1115_COMP_0_GND, ADS1115_COMP_1_GND, ADS1115_COMP_2_GND
from ADS1115 import ADS1115_RANGE_256, ADS1115_RANGE_0512
from median_filter import MedianFilter

ADS1115_ADDRESS = const(0x48)
MEASUREMENT_BRIGHTNESS = const(250)

class DeviceController:
    GEOMETRY_85 = const(0)
    GEOMETRY_60 = const(1)
    GEOMETRY_20 = const(2)
    def __init__(self, adc, led_controller):
        self.adc = adc
        self.led_controller = led_controller
        self.geometry_85_led = self.led_controller.LED1
        self.geometry_85_ADC = ADS1115_COMP_0_GND
        self.geometry_60_led = self.led_controller.LED2
        self.geometry_60_ADC = ADS1115_COMP_1_GND
        self.geometry_20_led = self.led_controller.LED3
        self.geometry_20_ADC = ADS1115_COMP_2_GND
        self.gemotery_85_100_ADC = 0
        self.gemotery_60_100_ADC = 0
        self.gemotery_20_100_ADC = 0
        # Define the command dictionary
        self.commands = {
            '1': self.enable_led,
            '2': self.set_brightness,
            '3': self.read_adc,
            '4': self.disable_led,
            '5': self.read_all_adc_channels,
            '6': self.read_zero_calibrated_adc,
            '7': self.cal_geometry_to_100_gu,
            '8': self.measure_gloss_units,
            '9': self.exit_program
        }

    def menu(self):
        menu_text = """
        Device Control Menu:
        1. Enable LED
        2. Set LED Brightness
        3. Read ADC Value
        4. Disable LED
        5. Read RAW ADC Channels
        6. Raw Measurement
        7. Calibrate to 100 GU
        8. Read GU
        9. Exit
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
    
    async def read_all_adc_channels(self):
        voltage = self.read_adc_channel(ADS1115_COMP_0_GND)
        print("Channel 0: {:<4}".format(voltage))
        voltage = self.read_adc_channel(ADS1115_COMP_1_GND)
        print("Channel 1: {:<4}".format(voltage))
        voltage = self.read_adc_channel(ADS1115_COMP_2_GND)
        print("Channel 2: {:<4}".format(voltage))

        
    def read_adc_channel(self, channel, num_samples=17):
        self.adc.setCompareChannels(channel)
        total_voltage = 0
        flt = MedianFilter()
        average_voltage = 0
        for _ in range(num_samples):
            self.adc.startSingleMeasurement()
            while self.adc.isBusy():
                pass
            average_voltage = flt.add_value(self.adc.getRawResult())
        return average_voltage
        
    async def read_geometry_measurement(self, geometry = GEOMETRY_60):
        #Disables all LEDs then takes a refrence measurement for the geometry
        #Then turns the geometry led on takes mesurement and reports the diff
        led = 0
        adc = 0
        if(GEOMETRY_85 == geometry):
            led = self.geometry_85_led
            adc = self.geometry_85_ADC
        elif(GEOMETRY_20 == geometry):
            led = self.geometry_20_led
            adc = self.geometry_20_ADC
        else:
            led = self.geometry_60_led
            adc = self.geometry_60_ADC
        #Turn all LEDs off
        self.led_controller.led_ch_enable(self.geometry_85_led, False)
        self.led_controller.led_ch_enable(self.geometry_60_led, False)
        self.led_controller.led_ch_enable(self.geometry_20_led, False)
        #Take baseline ADC measurment
        base_line_adc = self.read_adc_channel(adc)
        #Turn on the LED needed for this measurement and set brightness
        self.led_controller.led_ch_enable(led, True)
        self.led_controller.set_brightness(led, MEASUREMENT_BRIGHTNESS)
        await asyncio.sleep(1)
        #Read the adc value
        measurement_adc = self.read_adc_channel(adc)
        #Turn off the current channel
        self.led_controller.led_ch_enable(led, False)
        return (measurement_adc - base_line_adc)
        
    async def read_zero_calibrated_adc(self):
        geometry_option = int(input("Enter gemotery 1:20    2:60    3:85    : "))
        geometry = self.GEOMETRY_60
        if(1 == geometry_option):
            geometry = self.GEOMETRY_20
        elif(3 == geometry_option):
            geometry = self.GEOMETRY_85
        measurement = await self.read_geometry_measurement(geometry)
        print(f"Measurment for selected geometry is {measurement}.")
    
    def get_gu(self, geometry, val):
        gu = 0
        ref_val = 0
        if(self.GEOMETRY_20 == geometry):
            ref_val = self.gemotery_20_100_ADC
        elif(self.GEOMETRY_60 == geometry):
            ref_val = self.gemotery_60_100_ADC
        elif(self.GEOMETRY_85 == geometry):
            ref_val = self.gemotery_85_100_ADC
        if(ref_val > 0):
            gu = val/ref_val
        else:
            gu = 0
        return gu * 100
    
    async def cal_geometry_to_100_gu(self):
        geometry_option = int(input("Enter gemotery 1:20    2:60    3:85    : "))
        geometry = self.GEOMETRY_60
        if(1 == geometry_option):
            geometry = self.GEOMETRY_20
        elif(3 == geometry_option):
            geometry = self.GEOMETRY_85
        measurement = await self.read_geometry_measurement(geometry)
        print(f"Calibration for selected geometry is {measurement}.")
        if(1 == geometry_option):
            self.gemotery_20_100_ADC = measurement
        elif(2 == geometry_option):
            self.gemotery_60_100_ADC = measurement
        elif(3 == geometry_option):
            self.gemotery_85_100_ADC = measurement
        
    async def measure_gloss_units(self):
        geometry_option = int(input("Enter gemotery 1:20    2:60    3:85    : "))
        geometry = self.GEOMETRY_60
        if(1 == geometry_option):
            geometry = self.GEOMETRY_20
        elif(3 == geometry_option):
            geometry = self.GEOMETRY_85
        measurement = await self.read_geometry_measurement(geometry)
        gu = self.get_gu(geometry, measurement)
        print(f"GU = {gu} with measurement {measurement}")
        
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
    i2c = machine.I2C(scl=machine.Pin(1), sda=machine.Pin(0))
    led_controller = KTD2026(i2c)
    adc = ADS1115(ADS1115_ADDRESS, i2c=i2c)
    adc.setVoltageRange_mV(ADS1115_RANGE_0512)
    controller = DeviceController(adc, led_controller)
    await controller.run()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
