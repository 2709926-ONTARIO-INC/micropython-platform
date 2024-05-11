import time

class KTD2026:
    #LED channels
    LED1 = const(0)
    LED2 = const(1)
    LED3 = const(2)
    LED4 = const(3)
    
    #Internal registers
    REG_EN          = const(0)
    REG_CH_ENABLE   = const(4)
    REG_LED1_IOUT   = const(6)
    REG_LED2_IOUT   = const(7)
    REG_LED3_IOUT   = const(8)
    REG_LED4_IOUT   = const(9)
    
    #Other constants
    ALWAYS_OFF      = const(0)
    ALWAYS_ON       = const(1)
    def __init__(self, i2c, address=0x30):
        self.i2c = i2c
        self.address = address
        self.current_led_state = 0
        self.initialize()

    def initialize(self):
        # Reset the device by writing to register 0
        self.write_register(REG_EN, 0x07)
        time.sleep(0.1)
        self.write_register(REG_EN, 0x1C)
        time.sleep(0.1)
        
    def set_brightness(self, led_ch, level):
        if(led_ch > self.LED4):
            return -1
        self.write_register(REG_LED1_IOUT + led_ch, level)

    def led_ch_enable(self, led_ch, enable=False):
        if led_ch > self.LED4:
            return -1
        # Adjust only the bits for the specified LED channel
        if enable:
            self.current_led_state |= (self.ALWAYS_ON << (led_ch * 2))  # Set bits to enable
        else:
            self.current_led_state &= ~(0x03 << (led_ch * 2))  # Clear bits to disable

        # Write the updated state back to the register
        self.write_register(self.REG_CH_ENABLE, self.current_led_state)


        
    def write_register(self, register, value):
        self.i2c.writeto_mem(self.address, register, bytearray([value]))

    def read_register(self, register):
        return self.i2c.readfrom_mem(self.address, register, 1)


