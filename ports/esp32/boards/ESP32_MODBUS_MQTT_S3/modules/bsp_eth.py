from machine import Pin,SPI,unique_id
import network
import utime

lan = None

def init_eth():
    '''
    Initialize the ethernet interface on this board
    '''
    global lan
    rst = Pin(18, Pin.OUT)
    rst.value(0)
    utime.sleep_ms(500)
    rst.value(1)
    utime.sleep_ms(1500)
    s = SPI(2, sck = Pin(12), mosi=Pin(11), miso=Pin(13))
    lan = network.LAN(phy_type=network.PHY_W5500, phy_addr=0, spi=s, int=Pin(6), cs=Pin(10))
    lan.config(mac=bytearray(unique_id()))
    lan.config("mac")
    lan.active(1)
    
def get_lan_status():
    '''
    Returns the current status of the lan interface
    '''
    global lan
    return lan.isconnected()
    
def get_lan_ip_config():
    '''
    Returns the lan ip configuration tuple
    '''
    global lan
    return lan.ifconfig()
