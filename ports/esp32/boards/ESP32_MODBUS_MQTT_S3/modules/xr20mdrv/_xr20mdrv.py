import xr20m
import utime

CHANNELA        = const(0)
CHANNELB        = const(1)
timeout         = const(5000)     #Default time out in ms
BAUD_DEFAULT    = const(9600)

#parity constants
NO_PAITY        = const(0)
ODD_PARITY      = const(1)
EVEN_PARITY     = const(2)

#Stop bit
STOP_1          = const(1)
STOP_2          = const(2)

class XR20M():
    def __init__(self, channel):
        '''
        create the xr20m channel object to be used as serial
        '''
        self.ch = channel
        self.timeout = timeout
        self.baud = BAUD_DEFAULT
        self.parity = NO_PAITY
        self.stop = STOP_1
    
    def set_time_out(self, newtimeout):
        '''
        Set the time out in milli seconds
        '''
        self.timeout = newtimeout
    
    def set_baud_rate(self, baud=9600):
        '''
        Set the baud rate for this channel. Defaults to 9600
        '''
        self.baud = baud
        xr20m.xr20m_set_baud(self.ch, self.baud)
        
    def set_line_encoding(self, parity, stop_bits):
        '''
        Set the line encoding. Data length is always fixed at 8 bits
        '''
        self.parity = parity
        self.stop = stop_bits
        xr20m.xr20m_set_line(self.ch, self.parity, self.stop)
    
    def write(self, buf):
        '''
        Transmit the data in buf     
        '''
        for _byte in buf:
            xr20m.xr20m_write(self.ch, _byte)
                
    def any(self):
        '''
        Checks if there are any bytes that can be read without blocking for this channel
        '''
        return xr20m.xr20m_any(self.ch)
    
    def read(self, nbytes = None):
        data_array = bytearray()
        read_bytes = 0
        if self.timeout < 10:
            _timeout = 10
        else:
            _timeout = self.timeout
        while _timeout > 0:
            utime.sleep_ms(10)
            _timeout = _timeout - 10
            if self.any():
                data_array.append(xr20m.xr20m_pop(self.ch))
                read_bytes = read_bytes + 1
                if (None != nbytes) and (read_bytes == nbytes):
                    break;
        return data_array
        
#Init the i2c to UART IC
xr20m.xr20m_init()
#Create the singletons for the two channels
XR20M_CHA = XR20M(CHANNELA)
XR20M_CHB = XR20M(CHANNELB)