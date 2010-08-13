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
        self.__scanner = {}
        self.__commands = {
                         "discover" : lambda s, p="": s.loadDiscoveryPlugin(p),
                         "scan" : lambda s,p="": s.loadScannerPlugin(p),
                         "show" : lambda s,p="": s.showPlugins(p),
                         "start" : lambda s: s.scan()
                         }
        self.__scannerCommands = {
                                  "bluetooth" : lambda s: airxploit.scanner.bluetooth.BluetoothScanner(self.__blackboard),
                                  "wlan" : lambda s: airxploit.scanner.wlan.WlanScanner(self.__blackboard),
                                  }
        self.__discoveryCommands = {
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

    def showPlugins(self, category):
        if category == "scan":
            return self.__scannerCommands
        elif category == "discover":
            return self.__discoveryCommands 
           
    def getDiscoveryPlugins(self):
        return self.__discoveryCommands
    
    def loadDiscoveryPlugin(self, plugin):
        if plugin == "all" or plugin == "":
            for p in self.__discoveryCommands:
                self.__discoveryCommands[p](self)
        elif plugin in self.__discoveryCommands:
            self.__discoveryCommands[plugin](self)
        else:
            raise airxploit.fuckup.not_a_command.NotACommand()
            
    def getScannerPlugins(self):
        return self.__scannerCommands
    
    def loadScannerPlugin(self, plugin):
        if plugin == "all" or plugin == "":
            for p in self.__scannerCommands:
                self.__scanner[p] = self.__scannerCommands[p](self)
        elif plugin in self.__scannerCommands:
            self.__scanner[plugin] = self.__scannerCommands[plugin](self)
        else:
            raise airxploit.fuckup.not_a_command.NotACommand()
            
    def scan(self):
        if len(self.__scanner) == 0:
            raise airxploit.fuckup.big_shit.BigShit("No scanner loaded");
        
        for plugin in self.__scanner:
            if plugin == "wlan":
                self.__scanner[plugin].iface = "wlan0"
            
            self.__scanner[plugin].run()
        
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
