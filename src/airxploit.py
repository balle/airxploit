#!/usr/bin/python

from airxploit.view.console import ConsoleView
from airxploit.core.blackboard import Blackboard
import logging

logging.basicConfig(filename='airxploit.log', level=logging.DEBUG)

blackboard = Blackboard()
airView = ConsoleView(blackboard)

airView.header()
airView.run()
