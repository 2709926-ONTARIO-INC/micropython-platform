# Serial to MQTT gateway MicroPython Helper Library
# 2023 Samuel Ramrajkar
#
# 2023-Oct-16 - v1 - Initial implementation

# Import required libraries
from micropython import const
from machine import Pin, SPI, ADC
import machine, time

# TinyS2 Hardware Pin Assignments

# Sense Pins
APP_VERSION = const(1)

def get_application_version():
    '''
    Returns the current application version
    '''
    return APP_VERSION
