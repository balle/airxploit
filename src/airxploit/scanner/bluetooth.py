'''
Created on 25.07.2010

@author: basti
'''

import lightblue
import airxploit.core
import sys
import logging

class BluetoothScanner(object):
    '''
    Scan for Bluetooth devices
    You can register for BLUETOOTH_TARGET_FOUND event to get notified if we found somethin
    '''

    EVENT = "BLUETOOTH_TARGET_FOUND"

    def __init__(self, pcc):
        self.__targets = {}
        self.__pcc = pcc
        self.__pcc.registerEvent(BluetoothScanner.EVENT)
        self.__pcc.registerService("BluetoothScanner", self)
        
    def getResult(self):
        return self.__targets.values()
    
    def run(self):
        current_targets = {}
        logging.debug("Scanning for bluetooth devices")
        
        try:
            for device in lightblue.finddevices():
                target = airxploit.core.target.Bluetooth()
                target.addr = device[0]
                target.name = device[1]
                current_targets[target.addr] = target
                logging.debug("Found bluetooth device " + device[0] + " " + device[1])

        except IOError:
            pass
        
        got_new_targets = False
        
        for key in current_targets:
            if key not in self.__targets:
                got_new_targets = True
                self.__targets[key] = current_targets[key]
                self.__pcc.addTarget( current_targets[key] )

        if got_new_targets:
            self.__pcc.fireEvent(BluetoothScanner.EVENT)    
