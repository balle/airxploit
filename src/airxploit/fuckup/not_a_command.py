'''
Created on 13.08.2010

@author: basti
'''
class NotACommand(Exception):
    def __init__(self, what):
        self.__msg = "Not an airxploit.command.Command object: " + str(what)
        
    def __str__(self):
        return self.__msg
