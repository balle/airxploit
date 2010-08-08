'''
Created on 25.07.2010

@author: basti
'''

import errno
import sys
from pythonwifi.iwlibs import Wireless
import airxploit.core
import logging
from airxploit.fuckup.permission_denied import PermissionDenied
from airxploit.fuckup.big_shit import BigShit

class WlanScanner(object):
    '''
    Scan for Wlan devices
    You can register for WLAN_TARGET_FOUND event to get notified if we found somethin
    '''

    EVENT = "WLAN_TARGET_FOUND"

    def __init__(self, blackboard):
        self.iface = "wlan0"
        self.__targets = {}
        self.__blackboard = blackboard
        self.__blackboard.registerEvent(WlanScanner.EVENT)
    
    def getResult(self):
        return self.__targets.values()
    
    def run(self):
        current_targets = {}
        logging.debug("Scanning for wlan devices")
        
        try:
            wifi = Wireless(self.iface)
            results = wifi.scan()
        except IOError, e:
            if e.id != errno.EPERM:
                raise BigShit("Interface " + wifi.ifname + " doesnt support scanning")
            else:
                raise PermissionDenied("Cannot scan for wifi :(")
                sys.exit(1)
        
        if len(results) > 0:
            (num_channels, frequencies) = wifi.getChannelInfo()
            
            for ap in results:
#               print ap.bssid + " " + frequencies.index(wifi._formatFrequency(ap.frequency.getFrequency())) + " " + ap.essid + " " + ap.quality.getSignallevel()
                target = airxploit.core.target.Wlan()
                target.quality = ap.quality.getSignallevel()
                target.name = ap.essid
                target.addr = ap.bssid
                current_targets[ap.bssid] = target
                logging.debug("Found wlan device " + ap.bssid + " " + " " + ap.essid)
        
        got_new_targets = False
        
        for key in current_targets:
            if key not in self.__targets:
                got_new_targets = True
                self.__targets[key] = current_targets[key]
                self.__blackboard.add( current_targets[key] )

        if got_new_targets:
            self.__blackboard.fireEvent(WlanScanner.EVENT)
        