'''
Created on 31.07.2010

@author: basti
'''

class Target(object):
    '''
    AirXploit target
    '''


    def __init__(self):
        self.name = "unknown"
        self.addr = None
        self.encryption = None
        self.quality = None
        self.__additional_information = {}

    def writeInfo(self, section, info):
        self.__additional_information[section] = info

    def readInfo(self, section):
        if section in self.__additional_information:
            return self.__additional_information[section]
        else:
            return None
    
    def hasInfo(self, section):
        if section in self.__additional_information:
            return True
        else:
            return False
    
class Bluetooth(Target):
    '''
    Bluetooth target
    '''


    def __init__(self):
        Target.__init__(self)

class Wlan(Target):
    '''
    Wlan target
    '''


    def __init__(self):
        Target.__init__(self)
        self.channel = None
        
