from machine import I2C

class SC16IS752:
    #General Registers
    SC16IS750_REG_RHR        const(0x00)
    SC16IS750_REG_THR        const(0X00)
    SC16IS750_REG_IER        const(0X01)
    SC16IS750_REG_FCR        const(0X02)
    SC16IS750_REG_IIR        const(0X02)
    SC16IS750_REG_LCR        const(0X03)
    SC16IS750_REG_MCR        const(0X04)
    SC16IS750_REG_LSR        const(0X05)
    SC16IS750_REG_MSR        const(0X06)
    SC16IS750_REG_SPR        const(0X07)
    SC16IS750_REG_TCR        const(0X06)
    SC16IS750_REG_TLR        const(0X07)
    SC16IS750_REG_TXLVL      const(0X08)
    SC16IS750_REG_RXLVL      const(0X09)
    SC16IS750_REG_IODIR      const(0X0A)
    SC16IS750_REG_IOSTATE    const(0X0B)
    SC16IS750_REG_IOINTENA   const(0X0C)
    SC16IS750_REG_IOCONTROL  const(0X0E)
    SC16IS750_REG_EFCR       const(0X0F)
    
    #Special Registers
    SC16IS750_REG_DLL        const(0x00)
    SC16IS750_REG_DLH        const(0X01)

    #Enhanced Registers
    SC16IS750_REG_EFR        const(0X02)
    SC16IS750_REG_XON1       const(0X04)
    SC16IS750_REG_XON2       const(0X05)
    SC16IS750_REG_XOFF1      const(0X06)
    SC16IS750_REG_XOFF2      const(0X07)

    SC16IS750_INT_CTS        const(0X80)
    SC16IS750_INT_RTS        const(0X40)
    SC16IS750_INT_XOFF       const(0X20)
    SC16IS750_INT_SLEEP      const(0X10)
    SC16IS750_INT_MODEM      const(0X08)
    SC16IS750_INT_LINE       const(0X04)
    SC16IS750_INT_THR        const(0X02)
    SC16IS750_INT_RHR        const(0X01)
    
    SC16IS752_CHANNEL_A      const(0x00)
    SC16IS752_CHANNEL_B      const(0x01)
    SC16IS752_CHANNEL_BOTH   const(0x00)
    
    SC16IS750_CRYSTCAL_FREQ  const(16000000)

    i2c_obj = None
    def __init__(self, i2c):
        '''
        Set up the I2C bus object and initialize the common aspect of the chip
        '''
        self.i2c_obj = i2c
    
    def WriteRegister(channel, reg_addr, val):
        self.i2c_obj.writeto((reg_addr << 3 | channel << 1), bytearray(val))
        
    def ReadRegister(channel, reg_addr):
        return self.i2c_obj.readfrom((reg_addr << 3 | channel << 1), 1)[0]
        
    def ResetDevice():
        reg  = self.ReadRegister(SC16IS752_CHANNEL_BOTH, SC16IS750_REG_IOCONTROL);
        self.WriteRegister(SC16IS752_CHANNEL_BOTH, SC16IS750_REG_IOCONTROL, reg[] | 0x08)
        
    def set_baudrate(self, channel, baudrate):
        # Calculate the divisor
        prescaler = 1 if (self.ReadRegister(channel, SC16IS750_REG_MCR) & 0x80) == 0 else 4
        divisor = self.SC16IS750_CRYSTCAL_FREQ // (prescaler * baudrate * 16)

        # Update LCR register
        temp_lcr = self.ReadRegister(channel, SC16IS750_REG_LCR)
        temp_lcr |= 0x80
        self.WriteRegister(channel, SC16IS750_REG_LCR, temp_lcr)

        # Write to DLL and DLH
        self.WriteRegister(channel, SC16IS750_REG_DLL, divisor & 0xFF)
        self.WriteRegister(channel, SC16IS750_REG_DLH, (divisor >> 8) & 0xFF)

        # Restore LCR register
        temp_lcr &= 0x7F
        self.WriteRegister(channel, SC16IS750_REG_LCR, temp_lcr)

        # Calculate the actual baud rate and error
        actual_baudrate = self.SC16IS750_CRYSTCAL_FREQ // (prescaler * 16 * divisor)
        error = int(((actual_baudrate - baudrate) * 1000) / baudrate)
        # Optionally, you can print the information. In MicroPython, use 'print' instead of ESP_LOGI
        print(f"Desired baudrate: {baudrate}, Calculated divisor: {divisor}, Actual baudrate: {actual_baudrate}, Baudrate error: {error}")

        return error
        
    def set_line(self, channel, data_length, parity_select, stop_length):
        temp_lcr = self.ReadRegister(channel, SC16IS750_REG_LCR)
        temp_lcr &= 0xC0  # Clear the lower six bits of LCR (LCR[0] to LCR[5])

        # Setting data length
        if data_length == 5:
            pass
        elif data_length == 6:
            temp_lcr |= 0x01
        elif data_length == 7:
            temp_lcr |= 0x02
        elif data_length == 8:
            temp_lcr |= 0x03
        else:
            temp_lcr |= 0x03  # Default to 8 bits

        # Setting stop bits
        if stop_length == 2:
            temp_lcr |= 0x04

        # Setting parity
        if parity_select == 0:
            pass  # No parity
        elif parity_select == 1:
            temp_lcr |= 0x08  # Odd parity
        elif parity_select == 2:
            temp_lcr |= 0x18  # Even parity
        elif parity_select == 3:
            temp_lcr |= 0x03  # Force '1' parity
        elif parity_select == 4:
            pass  # Force '0' parity

        self.WriteRegister(channel, SC16IS750_REG_LCR, temp_lcr)
        
    # FIFO Enable
    def fifo_enable(self, channel, fifo_enable):
        temp_fcr = self._read_register(channel, SC16IS750_REG_FCR)
        temp_fcr = temp_fcr & 0xFE if fifo_enable == 0 else temp_fcr | 0x01
        self._write_register(channel, SC16IS750_REG_FCR, temp_fcr)

    # FIFO Reset
    def fifo_reset(self, channel, rx_fifo):
        temp_fcr = self._read_register(channel, SC16IS750_REG_FCR)
        temp_fcr |= 0x04 if rx_fifo == 0 else 0x02
        self._write_register(channel, SC16IS750_REG_FCR, temp_fcr)

    # FIFO Set Trigger Level
    def fifo_set_trigger_level(self, channel, rx_fifo, length):
        temp_reg = self._read_register(channel, SC16IS750_REG_MCR)
        temp_reg |= 0x04
        self._write_register(channel, SC16IS750_REG_MCR, temp_reg)

        temp_reg = self._read_register(channel, SC16IS750_REG_EFR)
        self._write_register(channel, SC16IS750_REG_EFR, temp_reg | 0x10)

        if rx_fifo == 0:
            self._write_register(channel, SC16IS750_REG_TLR, length << 4)
        else:
            self._write_register(channel, SC16IS750_REG_TLR, length)

        self._write_register(channel, SC16IS750_REG_EFR, temp_reg)

    # FIFO Available Data
    def fifo_available_data(self, channel):
        self.fifo_available[channel] = self._read_register(channel, SC16IS750_REG_RXLVL)
        return self.fifo_available[channel]

    # FIFO Available Space
    def fifo_available_space(self, channel):
        return self._read_register(channel, SC16IS750_REG_TXLVL)
        
    def write_byte(self, channel, val):
        # Wait until there's space in the FIFO
        while (self._read_register(channel, SC16IS750_REG_LSR) & 0x20) == 0:
            pass  # You could add a timeout here for safety

        # Write the value to the THR (Transmit Holding Register)
        self._write_register(channel, SC16IS750_REG_THR, val)