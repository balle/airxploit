'''
Created on 31.07.2010

@author: basti
'''

import logging
from airxploit.scanner.bluetooth import BluetoothScanner
from airxploit.scanner.wlan import WlanScanner
from airxploit.core.target import Wlan, Bluetooth
import airxploit.fuckup
import airxploit.discovery
import re

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
        self.__commands = {
                         "discover" : lambda s, p: s.loadDiscoveryPlugin(p),
                         "scan" : lambda s: s.scan()
                         }
        self.__discoveryCommand = {
                                   "sdp" : lambda s: airxploit.discovery.sdp.SdpBrowser(self.__blackboard),
                                   "rfcomm" : lambda s: airxploit.discovery.rfcomm.RfcommScanner(self.__blackboard)
                                   }

    def getCommands(self):
        return self.__commands.keys()
    
    def runCommand(self, cmdline):
        cmd = re.split(r"\s", cmdline)
        
        if cmd[0] in self.__commands:
            if len(cmd) == 2:
                self.__commands[cmd[0]](self, cmd[1])
            else:
                self.__commands[cmd[0]](self)
        else:
            raise airxploit.fuckup.not_a_command.NotACommand(cmd)

    def loadDiscoveryPlugin(self, plugin):
        if plugin in self.__discoveryCommand:
            self.__discoveryCommand[plugin](self)
        else:
            raise airxploit.fuckup.not_a_command.NotACommand()
            
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
