from ds1307 import DS1307
from machine import I2C, Pin
from time import gmtime, time

# DS1307 on 0x68
I2C_ADDR = const(0x68)     # DEC 104, HEX 0x68
ds1307 = None

def init_rtc():
    '''
    Initializes the rtc chip DS1307
    '''
    global ds1307
    i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    ds1307 = DS1307(addr=I2C_ADDR, i2c=i2c)
    
def get_rtc_time():
    '''
    Return the current RTC time
    '''
    global ds1307
    return ds1307.datetime
    
def set_rtc_time():
    '''
    Set the RTC time to the DS1307 chip.
    Returns True if operation was successful else returns False
    '''
    import ntptime
    global ds1307
    rc = False
    try:
        ntptime.settime()
        now = gmtime(time())
        ds1307.datetime = now
        rc = True
    except Exception as e:
        print(f"Error in setting RTC time from NTP server: {str(e)}")
    finally:
        return rc
        
def sync_rtc_time():
    '''
    Sets the system time to one from RTC
    '''
    import utime
    import machine
    tm = get_rtc_time()
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    