'''
Created on 31.07.2010

@author: basti
'''

from airxploit.core.eventmachine import EventMachine
from airxploit.core.target import Target
import logging
import airxploit.core.target

class Blackboard(object):
    '''
    This module encapsulates the airxploit event machine, system configuration
    required by all components 
    '''


    def __init__(self):
        self.__event = EventMachine()        
        self.__targets = {}
               
    def add(self, target):
        if type(target).__bases__[0] == airxploit.core.target.Target and target.addr not in self.__targets:
            logging.debug("Adding target " + target.addr)
            self.__targets[target.addr] = target
        else:
            # TODO: throw exception
            pass

    def addInfo(self, target, section, info):
        if type(target).__bases__[0] == airxploit.core.target.Target and target.addr in self.__targets:
            logging.debug("Adding info " + section + " to target " + target.addr)
            self.__targets[target.addr].writeInfo(section, info)
        else:
            pass
    
    def readAll(self):
        return self.__targets
         
    def readAllWithoutInfo(self, section):
        interesting_targets = []
        
        for target in self.__targets.values():
            if not target.hasInfo(section):
                interesting_targets.append(target)
        
        return interesting_targets
         
    def registerEvent(self, name):
        return self.__event.register(name)
    
    def fireEvent(self, name):
        return self.__event.fire(name)

    def registerForEvent(self, name, obj):
        return self.__event.registerFor(name, obj)
