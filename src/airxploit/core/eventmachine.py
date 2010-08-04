'''
Created on 31.07.2010

@author: basti
'''

class EventMachine(object):
    '''
    The airXploit eventmachine
    Scanner, tools, exploits and other plugin can register and fire events
    while other plugins register themself as listeners
    think of observer pattern ;)
    '''


    def __init__(self):
        self.__events = {}
        self.__event_listeners = {}
    
    def register(self, name):
        '''
        register an event
        '''
        self.__events[name] = 1
        self.__event_listeners[name] = {}
    
    def unregister(self, name):
        '''
        unregister an event
        '''
        if name in self.__events:
            del self.__events[name]
            del self.__event_listeners[name]
        else:
            print "Unknown event " + name
        
    def registerFor(self, name, obj):
        '''
        register yourself as a listener for the given event
        listeners must implement an gotEvent(name) method
        '''
        if name in self.__events:
            self.__event_listeners[name][obj] = 1
        else:
            print "Unknown event " + name
    
    def unregisterFor(self, name, obj):
        '''
        unregister as listener for event
        '''
        if name in self.__events:
            del self.__event_listeners[name][obj]
        else:
            print "Unknown event " + name
        
    def fire(self, name):
        '''
        fire an event!
        this will iterate over all event listeners and call their gotEvent() method
        '''
        if name in self.__events:
            for listener in self.__event_listeners[name]:
                try:
                    listener.gotEvent(name)
                except NotImplementedError:
                    del self.__event_listeners[name][listener]
                    next

    def events(self):
        '''
        get a list of registered events
        '''
        return self.__events.keys()
