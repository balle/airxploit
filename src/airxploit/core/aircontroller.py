'''
Created on 31.07.2010

@author: basti
'''

import logging
from time import sleep
from airxploit.scanner.bluetooth import BluetoothScanner
from airxploit.scanner.wlan import WlanScanner
from airxploit.core.target import Wlan, Bluetooth
import airxploit.fuckup
import airxploit.discovery
from airxploit.core.plugincontroller import PluginController
import re
import os

class AirController(object):
    '''
    Control the air!
    Guess what thats the airxploit controller class used by the views
    '''

    BLUETOOTH_EVENT = BluetoothScanner.EVENT
    WLAN_EVENT = WlanScanner.EVENT

    def __init__(self, pcc):
        self.__pcc = pcc
        self.__pluginController = PluginController(pcc)
        self.__commands = {
                            "discover" : lambda s, p="": s.__pluginController.loadDiscoveryPlugin(p),
                            "scan" : lambda s,p="": s.__pluginController.loadScannerPlugin(p),
                            "show" : lambda s,p="": s.__pluginController.showPlugins(p),
                            "start" : lambda s,p="": s.scan(p)
                          }
        self.__pluginController.initPlugins()

    '''
    get all commands
    '''
    def getCommands(self):
        return self.__commands.keys()
    
    '''
    run a command
    '''
    def runCommand(self, cmdline):
        cmd = re.split(r"\s", cmdline)
        
        if cmd[0] in self.__commands:
            if len(cmd) == 2:
                self.__commands[cmd[0]](self, cmd[1])
            else:
                self.__commands[cmd[0]](self)
        else:
            raise airxploit.fuckup.not_a_command.NotACommand(cmd)

    
    '''
    scan for targets
    '''        
    def scan(self, mode=""):
        if mode == "loop":
            while True:
                self.doScanning()
                sleep(10);
        else:
            self.doScanning()
            
    def doScanning(self):
        scanner = self.__pluginController.getActiveScannerPlugins()
        if len(scanner) == 0:
            raise airxploit.fuckup.big_shit.BigShit("No scanner loaded");
        
        for plugin in scanner:
            scanner[plugin].run()
    
    '''
    get a list of wlan targets
    '''    
    def getWlanTargets(self):
        wlanTargets = []
        
        for target in self.__pcc.readAll().values():
            if type(target) == Wlan:
                wlanTargets.append(target)
                
        return wlanTargets    

    '''
    get a list of bluetooth targets
    '''
    def getBluetoothTargets(self):
        btTargets = []
        
        for target in self.__pcc.readAll().values():
            if type(target) == Bluetooth:
                btTargets.append(target)
                
        return btTargets    
