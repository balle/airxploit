'''
Created on 31.07.2010

@author: basti
'''

from airxploit.core.eventmachine import EventMachine

class AirCtl(object):
    '''
    This module encapsulates the airxploit event machine, system configuration
    required by all components 
    '''


    def __init__(self):
        self.__event = EventMachine()        
        
    def registerEvent(self, name):
        return self.__event.register(name)
    
    def fireEvent(self, name):
        return self.__event.fire(name)

    def registerForEvent(self, name, obj):
        return self.__event.registerFor(name, obj)
