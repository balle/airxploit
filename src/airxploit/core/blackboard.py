'''
Created on 31.07.2010

@author: basti
'''

from airxploit.core.eventmachine import EventMachine
from airxploit.core.serviceregistry import ServiceRegistry
import logging
import airxploit.core.target
from airxploit.fuckup.not_a_target import NotATarget

class Blackboard(object):
    '''
    This module encapsulates the airxploit event machine, service registry, system configuration
    required by all components and it is the central information gathering system
    '''


    def __init__(self):
        self.__event = EventMachine()        
        self.__service = ServiceRegistry()
        self.__targets = {}
               
    def add(self, target):
        if type(target).__bases__[0] == airxploit.core.target.Target and target.addr not in self.__targets:
            logging.debug("Adding target " + target.addr)
            self.__targets[target.addr] = target
        else:
            raise NotATarget(target)

    def addInfo(self, target, section, info):
        if type(target).__bases__[0] == airxploit.core.target.Target and target.addr in self.__targets:
            logging.debug("Adding info " + section + " to target " + target.addr)
            self.__targets[target.addr].writeInfo(section, info)
        else:
            raise NotATarget(target)
    
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

    def registerService(self, name, plugin):
        return self.__service.register(name, plugin)
    
    def unregisterService(self, name):
        return self.__service.unregister(name)
    
    def getService(self, name):
        return self.__service.getService(name)
