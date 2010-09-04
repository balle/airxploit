'''
Created on 31.07.2010

@author: basti
'''

import logging
import airxploit.core.target
from airxploit.fuckup.not_a_target import NotATarget

class Blackboard(object):
    '''
    A blackboard for centralized information gathering
    Every plugin can add targets and read or add information about it
    '''

    def __init__(self):
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
