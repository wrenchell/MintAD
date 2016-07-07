#!/usr/bin/python

###############################################################################
 #
 # MintAD_pt2 
 #
 # Second part for the script that helps automate AD setup.  This one should be
 # run after the first one is run and then a restart.  This one will mostly be
 # editing config files, so bulletproofing is a MUST!
 #
 # Author: Mitchell Thompson
 # Copyright: Unitas-Inc 2016/07/07
 #
##

import sys
import os

def setup():
  # Clear the terminal and print the header
  os.system('./utils/clear.py')
  os.system('./app/header.py')

  print "This script will edit several root config files\n"

  print "This could be potentially harmful to a system if not executed properly!"

  print "If you stumbled across this script on accident, just type [^C]"

  raw_input("\nOtherwise, press ENTER to continue...\n\n")
  serverInfo()

def serverInfo():
  os.system('./utils/clear.py')
  os.system('./app/header.py')

  serverInput = raw_input('Enter the server name: ')
  
  # NOT SURE IF THE SERVER NAME NEEDS TO BE ALL CAPS OR NOT!
  serverName = serverInput.upper()
  # IF NOT THEN THIS NEEDS to BE CHANGED!!

  correct =  raw_input('The server name is: ' + serverName + ' \nis this correct? (y/n) ')

  correctInfo = correct.upper()

  if (correctInfo != 'Y'):
    serverInfo()
  else:
   begin(serverName)

def begin(s):
  # We will be using this function as a switch to process other data

  os.system('./utils/clear.py')
  os.system('./app/header.py')

  sudoAdmins()
  mapShare(s)
  profileTemplate()

def sudoAdmins():
  os.chdir('/')
  os.chdir('etc')
  print "\nGiving domain admins sudo right\n"
  print "Attempting to open \'etc\\sudoers\'\n"

  os.system('touch sudoers.tmp')
 # os.system('rm sudoers.old')
  try:
    superUsers = open('sudoers.tmp', 'r+')

  except IOError as err:
    print "I/O error ({0}): {1}".format(err.errno, err.strerror)
    sys.exit()

  print "Sucessfully opened \'etc\\sudoers\'\n"



  for line in superUsers:
    print line
    if (line == "# Members of the admin group may gain root privileges"):
      superUsers.write(line)
      superUsers.write('%DOMAIN_Admins ALL=(ALL)ALL')
    else:  
      superUsers.write(line)

  #os.system('mv sudoers sudoers.old && cp sudoers.tmp sudoers')

def mapShare(s):
  print "Got here"  
 


def profileTemplate():
  print "Got Here too"





setup()
