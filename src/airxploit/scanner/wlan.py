'''
Created on 25.07.2010

@author: basti
'''

import errno
import sys
from pythonwifi.iwlibs import Wireless
import airxploit.core
import logging

class WlanScanner(object):
    '''
    Scan for Wlan devices
    You can register for WLAN_TARGET_FOUND event to get notified if we found somethin
    '''

    EVENT = "WLAN_TARGET_FOUND"

    def __init__(self, airctl):
        self.iface = "wlan0"
        self.__targets = {}
        self.__airctl = airctl
        self.__airctl.registerEvent(WlanScanner.EVENT)
    
    def getTargets(self):
        return self.__targets.values()
    
    def scan(self):
        current_targets = {}
        logging.debug("Scanning for wlan devices")
        
        try:
            wifi = Wireless(self.iface)
            results = wifi.scan()
        except IOError, e:
            if e.id != errno.EPERM:
                print "Interface " + wifi.ifname + " doesnt support scanning"
            else:
                print "Permission denied"
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

        if got_new_targets:
            self.__airctl.fireEvent(WlanScanner.EVENT)
        