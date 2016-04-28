#!/usr/bin/python
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

import RPi.GPIO as GPIO

import time
import syslog

default_duration = 2
door_duration = 30

def close_switch(pin, duration):
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)
  time.sleep(duration)
  GPIO.output(pin, GPIO.HIGH)
  GPIO.cleanup()

def reset_relays(lock, unlock_init, unlock, light):
  for pin in (lock, unlock_init, unlock, light):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup()

def lock_door(lock, unlock_init, unlock, light):
  syslog.syslog("Close door called")
  close_switch(lock, default_duration)

def unlock_door(lock, unlock_init, unlock, light):
  #open door
  syslog.syslog("Open door called")
  close_switch(unlock_init, default_duration)
  # lights on
  close_switch(light, door_duration)
  lock_door(lock, unlock_init, unlock, light)
