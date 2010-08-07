#!/usr/bin/python
#!/usr/bin/python

from time import sleep
from airxploit.view.console import ConsoleView
from airxploit.core.blackboard import Blackboard
import logging

logging.basicConfig(filename='airxploit.log', level=logging.DEBUG)

blackboard = Blackboard()
airView = ConsoleView(blackboard)

airView.header()

while True:
    airView.scan()
    sleep(10)
