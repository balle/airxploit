'''
Created on 31.07.2010

@author: basti
'''

from airxploit.scanner.bluetooth import BluetoothScanner
from airxploit.scanner.wlan import WlanScanner
import logging

class AirController(object):
    '''
    Control the air
    '''

    BLUETOOTH_EVENT = BluetoothScanner.EVENT
    WLAN_EVENT = WlanScanner.EVENT

    def __init__(self, airctl):
        self.__bt = BluetoothScanner(airctl)
        self.__wlan = WlanScanner(airctl)
        self.__wlan.iface = "wlan0"

    
    def scan(self):
        self.__bt.scan()
        self.__wlan.scan()
        
    def getWlanTargets(self):
        return self.__wlan.getTargets()    

    def getBluetoothTargets(self):
        return self.__bt.getTargets()
