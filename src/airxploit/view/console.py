'''
Created on 31.07.2010

@author: basti
'''

from airxploit.core.aircontroller import AirController
import logging
import os

class ConsoleView(object):
    '''
    console view
    '''


    def __init__(self, airctl):
        self.__controller = AirController(airctl)
        self.__airctl = airctl
        self.__airctl.registerForEvent(AirController.WLAN_EVENT, self)
        self.__airctl.registerForEvent(AirController.BLUETOOTH_EVENT, self)
    
    def scan(self):
        print "\r" * 16
        print "\n<<< Scanning..."
        self.__controller.scan()
    
    def gotEvent(self, event):
        logging.debug("Got event " + event)
        self.clearScreen()
        print "Link\tAddr\t\t\tName"

        for target in self.__controller.getBluetoothTargets():
            print "-\t" + target.addr + "\t" + target.name

        for target in self.__controller.getWlanTargets():
            print str(target.quality) + "\t" + target.addr + "\t" + target.name + "\t\t\t"

#
    def clearScreen(self):
        os.system("clear")
        #print("\x1B[2J")