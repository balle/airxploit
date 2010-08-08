'''
Created on 08.08.2010

@author: basti
'''

class PermissionDenied(Exception):
    def __init__(self, what):
        self.__msg = "Permission denied: " + what
    
    def __str__(self):
        return self.__msg
