'''
Created on 07.08.2010

@author: basti
'''
import lightblue
import sys
import logging
import airxploit.core
from airxploit.scanner.bluetooth import BluetoothScanner

class SdpDiscovery(object):
    '''
    Browse SDP services of a Bluetooth target
    '''

    EVENT = "BLUETOOTH_SDP_FOUND"
    SECTION = "sdp"
    
    def __init__(self, blackboard):
        self.__blackboard = blackboard
        self.__blackboard.registerEvent(SdpDiscovery.EVENT)
        self.__blackboard.registerForEvent(BluetoothScanner.EVENT, self)
        self.__result = []
        
    def getResult(self):
        return self.__result
    
    def run(self):
        for target in self.__blackboard.readAllWithoutInfo(SdpDiscovery.SECTION):
            try:
                logging.debug("Executing SDP browse for target " + target.addr)
                services = []
                
                for sdp in lightblue.findservices(target.addr):
                    service = SdpService()
                    service.name = sdp[2]
                    service.channel = sdp[1]
                    services.append(service)
                
                if services.count > 0:    
                    self.__result = services
                    self.__blackboard.addInfo(target, SdpDiscovery.SECTION, services)
                    self.__blackboard.fireEvent(SdpDiscovery.EVENT)

            except IOError, e:
                pass
        
    
    def gotEvent(self, event):        
        self.run()
        
class SdpService(object):
    
    def __init__(self):
        self.name = ""
        self.channel = None
        
    def __str__(self):
        return str(self.channel) + " " + self.name
    