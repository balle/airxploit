'''
Created on 04.09.2010

@author: basti
'''

import os
import logging
import re

import airxploit.fuckup

class PluginController(object):
    '''
    read plugin dirs
    load plugins on demand
    '''
    
    def __init__(self, pcc):
        self.pcc = pcc
        self.scanner = {}
        self.__plugins = {}
        self.__plugins["exploit"] = {}
        self.__plugins["scanner"] = {}
        self.__plugins["discovery"] = {}

    
    '''
    read a plugin dir
    import all plugins
    return hash of plugins with plugin name => plugin with package 
    '''
    def importPlugins(self, category):
        plugins = {}

        for file in os.listdir("src/airxploit/" + category):
                if re.search(r"__init__", file) == None and re.search(r"py$", file):
                        plugin_name = re.sub(r".py$", "", file)
                        plugin = "airxploit." + category + "." + plugin_name
                        logging.debug("importing plugin " + plugin)
                        eval("__import__('" + plugin + "')")
                        plugins[plugin_name] = plugin
        return plugins

    '''
    read all plugins
    generate closures for loading plugins
    plugins will not be loaded immediately cause they register themself for events in __init__
    '''
    def initPlugins(self):
        for category in ("scanner", "discovery", "exploit"):
            for name in self.importPlugins(category):
                self.__plugins[category][name] = lambda s, category, name: self.initPlugin(category, name)

    '''
    init the given plugin
    '''
    def initPlugin(self, category, name):
        logging.debug("Load plugin " + "airxploit." + category + "." + name + "." + name.capitalize() + category.capitalize()) 
        return eval("airxploit." + category + "." + name + "." + name.capitalize() + category.capitalize() + "(self.pcc)")

    '''
    show all plugins of a category
    '''
    def showPlugins(self, category):
        if category in self.__plugins:
            return self.__plugins[category]
    
    '''
    init one or all plugins of a given category
    '''    
    def loadPlugin(self, category, plugin):
        if category in self.__plugins:
            if plugin == "all" or plugin == "":
                for p in self.__plugins[category]:
                    if category == "scanner":
                        self.__scanner[p] = self.__plugins[category][p](self, category, p)
                    else:
                        self.__plugins[category][p](self, category, p)
            elif plugin in self.__plugins[category]:
                if category == "scanner":
                    self.__scanner[plugin] = self.__plugins[category][plugin](self, category, plugin)
                else:
                    self.__plugins[category][plugin](self, category, plugin)
            else:
                raise airxploit.fuckup.not_a_command.NotACommand()
