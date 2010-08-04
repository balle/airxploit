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


class Bluetooth(Target):
    '''
    Bluetooth target
    '''


    def __init__(self):
        self.sdp = None
        self.rfcomm = None
        self.channel = None
        self.cod = None


class Wlan(Target):
    '''
    Wlan target
    '''


    def __init__(self):
        self.channel = None
        self.frequency = None
        self.encryption_type = None
