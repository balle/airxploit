'''
Created on 08.08.2010

@author: basti
'''

class NotATarget(Exception):
    def __init__(self, what):
        self.__msg = "Not an airxploit.core.target.Target object: " + str(what)
        
    def __str__(self):
        return self.__msg
