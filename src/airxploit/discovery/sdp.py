'''
Created on 07.08.2010

@author: basti
'''
import lightblue
import sys
import logging
import airxploit.core
from airxploit.scanner.bluetooth import BluetoothScanner

class SdpBrowser(object):
    '''
    Browse SDP services of a Bluetooth target
    '''

    EVENT = "BLUETOOTH_SDP_FOUND"
    
    def __init__(self, blackboard):
        self.__blackboard = blackboard
        self.__blackboard.registerEvent(SdpBrowser.EVENT)
        self.__blackboard.registerForEvent(BluetoothScanner.EVENT, self)
    
    def gotEvent(self, event):        
        for target in self.__blackboard.readAllWithoutInfo("sdp"):
            try:
                logging.debug("Executing SDP browse for target " + target.addr)
                services = []
                
                for sdp in lightblue.findservices(target.addr):
                    service = SdpService()
                    service.name = sdp[2]
                    service.channel = sdp[1]
                    services.append(service)
                
                if services.count > 0:    
                    self.__blackboard.addInfo(target, "sdp", services)
                    self.__blackboard.fireEvent(SdpBrowser.EVENT)
                    #sock = lightblue.socket()
                    #sock.connect((target, service[1]))
                    #sock.close

            except IOError, e:
                pass
            
class SdpService(object):
    
    def __init__(self):
        self.name = ""
        self.channel = None
        
    def __str__(self):
        return str(self.channel) + " " + self.name
    