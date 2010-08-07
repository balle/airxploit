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
    
    def header(self):
        print """
            d8,                                     d8b           d8,        
           `8P                                      88P          `8P    d8P  
                                                   d88               d888888P
 d888b8b    88b  88bd88b    ?88,  88P    ?88,.d88b,888   d8888b   88b  ?88'  
d8P' ?88    88P  88P'  `     `?8bd8P'    `?88'  ?88?88  d8P' ?88  88P  88P   
88b  ,88b  d88  d88          d8P?8b,       88b  d8P 88b 88b  d88 d88   88b   
`?88P'`88bd88' d88'         d8P' `?8b      888888P'  88b`?8888P'd88'   `?8b  
                                           88P'                              
                                          d88                                
                                          ?8P                                        
        """
    
    def scan(self):
        print "\r" * 16
        print "\n<<< Scanning..."
        self.__controller.scan()
    
    def gotEvent(self, event):
        logging.debug("Got event " + event)
        self.clearScreen()
        self.header()
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