'''
Created on 04.09.2010

@author: basti
'''

import logging
import airxploit.fuckup

class ServiceRegistry(object):
    '''
    Register a plugin as a service
    Let other plugins load that services
    '''
    
    def __init__(self):
        self.__services = {}
        
    def register(self, name, plugin):
        if name not in self.__services:
            self.__services[name] = plugin
            logging.debug("Registered service " + name + " -> " + str(plugin))
        else:
            logging.error("Service " + name + " already registered")

    def unregister(self, name):
        if name in self.__services:
            del self.__services[name]
            logging.debug("Unregister service " + name)
        else:
            raise airxploit.fuckup.not_a_service.NotAService(name)
        
    def getService(self, name):
        if name in self.__services:
            return self.__services[name]
        else:
            raise airxploit.fuckup.not_a_service.NotAService(name)
    
    def services(self):
        return self.__services.keys()
