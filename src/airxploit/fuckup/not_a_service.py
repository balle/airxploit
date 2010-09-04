'''
Created on 05.09.2010

@author: basti
'''

class NotAService(Exception):
    def __init__(self, what):
        self.__msg = "Unknown service: " + str(what)
        
    def __str__(self):
        return self.__msg
