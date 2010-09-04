'''
Created on 31.07.2010

@author: basti
'''
import logging
import airxploit.fuckup

class EventMachine(object):
    '''
    The airXploit eventmachine
    Scanner, tools, exploits and other plugin can register and fire events
    while other plugins register themself as listeners
    think of observer pattern ;)
    '''


    def __init__(self):
        self.__events = {}
        self.__events["ALL"] = 1
        
        self.__event_listeners = {}
        self.__event_listeners["ALL"] = {}
        
    def register(self, name):
        '''
        register an event
        '''
        if name != "ALL":
            self.__events[name] = 1
            self.__event_listeners[name] = {}
    
    def unregister(self, name):
        '''
        unregister an event
        '''
        if name in self.__events and name != "ALL":
            del self.__events[name]
            del self.__event_listeners[name]
        else:
            logging.error("Unknown event " + name)
            raise airxploit.fuckup.not_an_event.NotAnEvent(name)
        
    def registerFor(self, name, obj):
        '''
        register yourself as a listener for the given event
        listeners must implement an gotEvent(name) method
        event name "ALL" will register for all events
        '''
        if name in self.__events or name == "ALL":
            logging.debug("Registering " + str(obj) + " for event " + name)            
            self.__event_listeners[name][obj] = 1
        else:
            logging.error("Unknown event " + name)
            raise airxploit.fuckup.not_an_event.NotAnEvent(name)
    
    def unregisterFor(self, name, obj):
        '''
        unregister as listener for event
        '''
        if name in self.__events or name == "ALL":
            logging.debug("Unregistering " + str(obj) + " from event " + name)
            del self.__event_listeners[name][obj]
        else:
            logging.error("Unknown event " + name)
            raise airxploit.fuckup.not_an_event.NotAnEvent(name)
        
    def fire(self, name):
        '''
        fire an event!
        this will iterate over all event listeners and call their gotEvent() method
        '''
        if name in self.__events:
            logging.debug("Fireing event " + name)
            notify_listeners = {}
            notify_listeners = self.__event_listeners[name]
            notify_listeners.update(self.__event_listeners["ALL"])
            
            del_listeners = []
            
            for listener in notify_listeners:
                try:
                    listener.gotEvent(name)
                except AttributeError:
                    del_listeners.append(listener)
            
            for listener in del_listeners:
                del self.__event_listeners[name][listener]

    def events(self):
        '''
        get a list of registered events
        '''
        return self.__events.keys()
