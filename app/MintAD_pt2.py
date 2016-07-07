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

cwd = os.getcwd()

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
  print "Giving domain admins sudo right"
  print "Attempting to open \'etc\\sudoers\'"

  os.system('touch tempSudoers')
  os.system('rm sudoers.old')
  try:
    superUsers = open('sudoers', 'r+')
    tempSudoers = open('tempSudoers', 'r+')
  except IOError as err:
    print "I/O error ({0}): {1}".format(err.errno, err.strerror)
    sys.exit()

  print "Sucessfully opened \'etc\\sudoers\'\n"

  sudoLine = '%DOMAIN_Admins ALL=(ALL)ALL'
  
  for line in superUsers:
    line = line.strip()
    if (line == "# Members of the admin group may gain root privileges"):
      tempSudoers.write(line)
      tempSudoers.write("\n")
      tempSudoers.write(sudoLine)
      tempSudoers.write("\n")
    else:  
      tempSudoers.write(line)
      tempSudoers.write('\n')

  os.system('mv sudoers sudoers.old')
  os.system('mv tempSudoers sudoers')

def mapShare(s):
  print "Mapping the user share"
  print "\nInstalling libpam-mount"
  os.chdir('security')
  os.system('sudo apt-get install libpam-mount')

  strToWrite = '<volume user=\"*\"\nfstype=\"cifs\"\nserver=\"' + s + '\"\npath=\"home/%(DOMAIN_USER)\"\nmountpoint=\"~/H:_%(DOMAIN_USER)\"\n/>'

  print '\nWriting: \n'
  print  strToWrite + '\n'
  print 'to \'etc/security/pam_mount.conf.xml'

  os.system('touch tempPamMount.xml')

  try:
    pamMount = open('pam_mount.conf.xml', 'r+')
    pamTemp = open('tempPamMount.xml', 'r+')
  except IOError as err:
    print "I/O error ({0}): {1}".format(err.errno, err.strerror)
    sys.exit()

  for line in pamMount:
    line = line.strip()
    if (line == '<!-- Volume definitions -->'):
      pamTemp.write(line)
      pamTemp.write('\n')
      pamTemp.write(strToWrite)
    else:
      pamTemp.write(line)
      pamTemp.write('\n')
 
  os.system('sudo rm pam_mount.conf.xml.old')
  os.system('mv pam_mount.conf.xml pam_mount.conf.xml.old') 
  os.system('mv tempPamMount.xml pam_mount.conf.xml')

  os.chdir(os.pardir)

def profileTemplate():
  print "Applying the user profile template."
  os.system('rm pam.d/tempCommon')
  os.system('touch pam.d/tempCommon')
  
  plateStr = 'session required 		pam_mkhomedir.so skel=/home/template/ umask=0022'

  print '\nWriting: '
  print '\n	' + plateStr + '	\n'
  print 'to \'etc/pam.d/common-session\'\n'
  
  try:
    profile = open('pam.d/common-session', 'r+')
    tempProfile = open('pam.d/tempCommon', 'r+')

  except IOError as err:
    print "I/O Error, file does not exist!"
    sys.exit()

  for line in profile:
    line = line.strip()
    if (line == '# and here are more per-package modules (the "Additional" block)'):

      tempProfile.write(line)
      tempProfile.write("\n")
      tempProfile.write(plateStr)
      tempProfile.write("\n")
    
    else:
      tempProfile.write(line)
      tempProfile.write("\n")

    os.system('mv pam.d/common-session pam.d/common-session.old')
    os.system('mv pam.d/tempCommon pam.d/common-session')  

setup()
