'''
Created on 05.09.2010

@author: basti
'''

import logging
from airxploit.core.blackboard import Blackboard
from airxploit.core.config import Config
from airxploit.core.eventmachine import EventMachine
from airxploit.core.serviceregistry import ServiceRegistry

class PluginControlCenter(object):
    '''
    This module encapsulates the airxploit event machine, service registry, system configuration
    and the blackboard for central information gathering
    '''

    def __init__(self):
        self.__blackbaord = Blackboard()
        self.__cfg = Config()
        self.__event = EventMachine()        
        self.__service = ServiceRegistry()

    def addTarget(self, target):
        return self.__blackbaord.add(target)
    
    def addInfo(self, target, section, info):
        return self.__blackbaord.addInfo(target, section, info)
    
    def readAll(self):
        return self.__blackbaord.readAll()
     
    def readAllWithoutInfo(self, section):
        return self.__blackbaord.readAllWithoutInfo(section)
    
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

    def getCfg(self, name):
        return self.__cfg.get(name)
    
    def getTool(self, name):
        return self.__cfg.cmd(name)
