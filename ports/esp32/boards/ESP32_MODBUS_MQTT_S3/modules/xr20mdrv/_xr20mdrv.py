import xr20m
import utime

CHANNELA = const(0)
CHANNELB = const(1)
timeout  = const(5000)     #Default time out in ms

class XR20M():
    def __init__(self, channel):
        '''
        create the xr20m channel object to be used as serial
        '''
        self.ch = channel
        self.timeout = timeout
    
    def set_time_out(self, newtimeout):
        self.timeout = newtimeout
    
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