'''
Created on 08.08.2010

@author: basti
'''
from airxploit.scanner.bluetooth import BluetoothScanner
import logging
import lightblue

class RfcommDiscovery(object):
    '''
    A simple RFCOMM scanner thats tries to connect to all 20 channels
    '''

    EVENT = "BLUETOOTH_RFCOMM_FOUND"
    SECTION = "rfcomm"

    def __init__(self, blackboard):
        self.__blackboard = blackboard
        self.__blackboard.registerEvent(RfcommDiscovery.EVENT)
        self.__blackboard.registerForEvent(BluetoothScanner.EVENT, self)
        self.__result = []
    
    def getResult(self):
        return self.__result
    
    def run(self):
        for target in self.__blackboard.readAllWithoutInfo(RfcommDiscovery.SECTION):
            logging.debug("Executing RFCOMM scanner for target " + target.addr)
            self.__result = []
            channels = []
            
            for scan in range(20):
                channel = RfcommService()
                channel.nr = scan+1

                try:
                    sock = lightblue.socket()
                    sock.connect((target.addr, scan+1))
                    sock.close
                
                    channel.open = True
                    logging.debug("Channel " + str(scan+1) + " open")
                except IOError:
                    channel.open = False
                    logging.debug("Channel " + str(scan+1) + " closed")
                
                channels.append(channel)
                
            if channels.count > 0:    
                self.__result = channels
                self.__blackboard.addInfo(target, RfcommDiscovery.SECTION, channels)
                self.__blackboard.fireEvent(RfcommDiscovery.EVENT)
            
    def gotEvent(self, event):        
        self.run()


class RfcommService(object):
    
    def __init__(self):
        self.nr = 0
        self.open = False
        
    def __str__(self):
        return "RFCOMM channel " + str(self.nr) + " " + str(self.open)
    