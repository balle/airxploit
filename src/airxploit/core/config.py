'''
Created on 05.09.2010

@author: basti
'''

from pyxml2obj import XMLin
import logging

class Config(object):
    '''
    Parse airxploit xml config
    '''
    
    def __init__(self):
        logging.debug("Parse config conf/airxploit.conf")
        self.__cfg = XMLin( open("conf/airxploit.conf","r").read() )

    '''
    get a config setting
    '''
    def get(self, name):
        if name in self.__cfg["config"]:
            return str(self.__cfg["config"][name])
    
    '''
    get a tool command
    '''
    def cmd(self, name):
        if name in self.__cfg["tools"]:
            return str(self.__cfg["tools"][name])
