#Copyright 2016 Susmit Shannigrahi

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bluetooth
import time
import sys
from open_close import unlock_door, lock_door, reset_relays

import bt_manager
import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop
import re
import syslog

adapter = bt_manager.BTAdapter()

target_address = ""
deviceInRange = True
lastState = "away" #host down
currentState = "connected"

#pins
lock = 3 #pin 9 on harness, IN2, GPIO3
unlock_init = 17 #pin 1 on harness, IN4, GPIO17
unlock = 4 #pin 2 on harness, IN3, GPIO4
light = 2 #pin 4 on harness, IN1, GPIO2
sleepTime = 2

#unlock seq - pin 1 ground, pin 2 ground
#light - pin 4 ground
#lock - pin 9 ground

#Pairing is necessary for mac address spoofing
#sudo service bluetooth restart
#sudo hciconfig
#sudo hciconfig hci0 piscan
#sudo bluez-simple-agent

while True:
  try:
    btsocket=bluetooth.BluetoothSocket(bluetooth.L2CAP)
    btsocket.connect((target_address, 3))
    if btsocket.send("init") and lastState == "away":
      syslog.syslog("device found %s" %(target_address))
      syslog.syslog("Unlocking car...")
      unlock_door(lock,unlock_init, unlock, light)
      lastState = "connected"
      btsocket.close()
    time.sleep(sleepTime)
  except bluetooth.btcommon.BluetoothError as e:
#terrible way to check error, but e.errno didn't work
    if lastState == "connected" and "112" in str(e):
      syslog.syslog("Locking...")
      lock_door(lock, unlock_init, unlock, light)
      lastState = "away"
    time.sleep(sleepTime)
  except KeyboardInterrupt:
    btsocket.close()
    reset_relays(lock, unlock_init, unlock, light)
    time.sleep(sleepTime)
    sys.exit(1)
  except:
    #sys.exc_info()[0]
    lock_door(lock, unlock_init, unlock, light)
    btsocket.close()
