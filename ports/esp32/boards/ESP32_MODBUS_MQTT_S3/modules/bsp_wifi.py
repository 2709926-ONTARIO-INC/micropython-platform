import network

sta_if = None

def init_wifi(ssid, pwd):
    '''
    Initialize the wifi station interface on this board
    '''
    global sta_if
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to wireless network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        
def get_wifi_sta_status():
    '''
    Returns the current status of the wifi sta interface
    '''
    global sta_if
    return sta_if.isconnected()
    
def get_wifi_sta_ip_config():
    '''
    Returns the wifi sta ip configuration tuple
    '''
    global sta_if
    return sta_if.ifconfig()
    
def set_wifi_sta_ip_config(config):
    '''
    Set static IP configuration from the tuple
    '''
    global sta_if
    sta_if.ifconfig(config)