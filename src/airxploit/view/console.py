'''
Created on 31.07.2010

@author: basti
'''

from airxploit.core.aircontroller import AirController
import airxploit.fuckup
import logging
import os
import random
import sys
import re

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
                                          ?8P                                        """

        greet_msg = ["We eat wireless worlds.",
                    "Hack the planet!",
                    "Explore, exploit, exhibit.",
                    "Wanna play a game?",
                    "Exception caught: Unknown space-time",
                    "Whispering wireless wonders",
                    "Freedom for your fingers",
                   ]
        print greet_msg[ random.randint(0, len(greet_msg)-1) ]
        print ""

    def runAway(self):
        exit_msg = ["Got a wireless ride?",
                    "May the source be with you",
                    "Have a nice day!",
                    "HF",
                    "Ya leaving?",
                    "Hey dont go... Let us look over there!",
                    "What do you want to explore now?",
                    "Life is fun!",
                    ":)",
                    "byebyeo"
                       ]
        print exit_msg[ random.randint(0, len(exit_msg)-1) ]
        sys.exit(0)
    
    def run(self):
        self.listCommands()
        self.mainMenu()

    def listCommands(self):
        print "///[ Commands:"
        for cmd in self.__controller.getCommands():
            print "\t* " + cmd
        
        print "\n"
    
    def listPlugins(self, category):
        if category == "all" or category == "":
            for c in ["discover", "scan"]:
                print c
                plugins = self.__controller.showPlugins(c)
                for plugin in plugins:
                    print "\t" + plugin
                print ""

        else:
            plugins = self.__controller.showPlugins(category)
        
            if plugins == None:
                print "<<< Dunno what " + category + " is x.x"
            else:
                for plugin in plugins:
                    print plugin
        print ""
    
    def mainMenu(self):
        print ">>> ",
        
        cmd = sys.stdin.readline()
        cmd = cmd.strip()
        matched_show = re.match(r"^show\s?(.*)", cmd)
        
        if cmd == "help" or cmd == "":
            self.listCommands()
        elif cmd == "exit" or cmd == "quit":
            self.runAway()
        elif matched_show:
            self.listPlugins(matched_show.group(1))
        else:    
            try:
                cmd_successfull = [
                                   "g0t it!",
                                   "yeah",
                                   "ok",
                                   "ack",
                                   "yes, master.",
                                   ":)"
                                   ]
                self.__controller.runCommand(cmd)            
                print "<<< " + cmd_successfull[ random.randint(0, len(cmd_successfull)-1)]
            except airxploit.fuckup.not_a_command.NotACommand, e:
                print "<<< Unknown command"
            except airxploit.fuckup.big_shit.BigShit, e:
                print "<<< " + str(e)
                logging.error(str(e))
            except airxploit.fuckup.plugin_init.PluginInit, e:
                print "<<< " + str(e)
                logging.error(str(e))
            except TypeError, e:
                bad_command = [
                               "Ouch!",
                               "Wrong, wrong, wrong...",
                               "Eh... what?",
                               "lol"
                               ]
                print "<<< " + bad_command[ random.randint(0, len(bad_command)-1)]
                print str(e)
                logging.error(str(e))
        print "\n"        
        self.mainMenu()
            
    def gotEvent(self, event):
        logging.debug("Got event " + event)
        self.clearScreen()
        self.header()
        print "Link\tAddr\tChannel\t\t\tName"

        for target in self.__controller.getBluetoothTargets():
            print "-\t" + target.addr + "\t" + "-\t" + target.name
            sdp = target.readInfo("sdp")
            
            if sdp != None:            
                print "\nSDP agent"
                print "Channel\t\tName"
                
                for service in sdp:
                    print str(service.channel) + "\t\t" + service.name
                print "\n"

            rfcomm = target.readInfo("rfcomm")
            
            if rfcomm != None:            
                print "\nRFCOMM agent"
                print "Channel\t\tOpen"
                
                for channel in rfcomm:
                    print str(channel.nr) + "\t\t" + str(channel.open)
                print "\n"
            
        for target in self.__controller.getWlanTargets():
            print str(target.quality) + "\t" + target.addr + "\t" + str(target.channel) + "\t\t" + target.name + "\t\t\t" 

    def clearScreen(self):
        os.system("clear")
        #print("\x1B[2J")