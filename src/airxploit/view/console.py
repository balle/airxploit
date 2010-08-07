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


    def __init__(self, blackboard):
        self.__controller = AirController(blackboard)
        self.__blackboard = blackboard
        self.__blackboard.registerForEvent("ALL", self)
    
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
            sdp = target.readInfo("sdp")
            
            if sdp != None:            
                print "\nPlugin: SDP"
                print "Channel\t\tName"
                
                for service in sdp:
                    print str(service.channel) + "\t\t" + service.name
                print "\n"
            
        for target in self.__controller.getWlanTargets():
            print str(target.quality) + "\t" + target.addr + "\t" + target.name + "\t\t\t"

#
    def clearScreen(self):
        os.system("clear")
        #print("\x1B[2J")