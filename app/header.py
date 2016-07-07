#!/usr/bin/python

###############################################################################
 #
 # Script to detect the width of the terminal and print the header
 #
 # Copyright (C) 2016 June 14  Mitchell Thompson
 #
 ##

import os
import sys
import fcntl
import termios
import struct

version = "0.1.0"

def detect():
  lines, cols = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, '1234'))
  temp = '%d' % (cols)
  width = int(temp)
  display(width)
  
 
def display(size):
  header = ""

  for x in range(0, size):
    header += ("#")

  header += ("\n #\n # Linux Mint Active Directory Intregration " + version + "\n #\n")
  
  for x in range(0, size):
    header += ("#")

  header += "\n"
  
  print header


detect()
