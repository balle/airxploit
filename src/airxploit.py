#!/usr/bin/python
#!/usr/bin/python

from time import sleep
from airxploit.view.console import ConsoleView
from airxploit.core.airctl import AirCtl
import logging

logging.basicConfig(filename='airxploit.log', level=logging.DEBUG)

airctl = AirCtl()
airView = ConsoleView(airctl)

while True:
    airView.scan()
    sleep(10)
