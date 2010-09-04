#!/usr/bin/python

from airxploit.view.console import ConsoleView
from airxploit.core.plugin_control_center import PluginControlCenter
import logging

logging.basicConfig(filename='airxploit.log', level=logging.DEBUG)

airView = ConsoleView( PluginControlCenter() )

airView.header()
airView.run()
