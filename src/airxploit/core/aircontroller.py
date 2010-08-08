'''
Created on 31.07.2010

@author: basti
'''

import logging
from airxploit.scanner.bluetooth import BluetoothScanner
from airxploit.scanner.wlan import WlanScanner
from airxploit.core.target import Wlan, Bluetooth
import airxploit.discovery

class AirController(object):
    '''
    Control the air
    '''

    BLUETOOTH_EVENT = BluetoothScanner.EVENT
    WLAN_EVENT = WlanScanner.EVENT

    def __init__(self, blackboard):
        self.__blackboard = blackboard
        self.__bt = BluetoothScanner(blackboard)
        self.__wlan = WlanScanner(blackboard)
        self.__wlan.iface = "wlan0"
        self.__sdp = airxploit.discovery.sdp.SdpBrowser(blackboard)

    
    def scan(self):
        self.__bt.run()
        self.__wlan.run()
        
    def getWlanTargets(self):
        wlanTargets = []
        
        for target in self.__blackboard.readAll().values():
            if type(target) == Wlan:
                wlanTargets.append(target)
                
        return wlanTargets    

    def getBluetoothTargets(self):
        btTargets = []
        
        for target in self.__blackboard.readAll().values():
            if type(target) == Bluetooth:
                btTargets.append(target)
                
        return btTargets    
