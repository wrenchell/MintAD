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


# ABANDON ALL HOPE!
def sudoAdmins():
  os.chdir('/')
  os.chdir('etc')
  print "Giving domain admins sudo right\n"
  #print "Attempting to open \'etc\\sudoers\'\n"

 # os.system('touch sudoers.neu')
 # os.system('rm sudoers.old')
 # try:
 #   superUsers = open('sudoers', 'r+')
 #   superUsersNeu = open('sudoers.neu', 'r+')
 # except IOError as err:
 #   print "I/O error ({0}): {1}".format(err.errno, err.strerror)
 #   sys.exit()

 # print "Sucessfully opened \'etc\\sudoers\'\n"

  sudoLine = '%DOMAIN_Admins ALL=(ALL)ALL'


  print 'I am going to open /etc/sudoers in visudo for you know.'
  print 'When the screen opens, you need to add a line into the file'
  print '\nUnder the line that reads: '
  print '\n	# Members of the admin group may gain root provileges	\n'
  print 'You need to type: '
  print "\n		" + sudoLine + "		\n"

  raw_input("Press ENTER when you are ready...")

  os.system('visudo -f sudoers')
  
 # for line in superUsers:
 #   print line
 #   if (line == "# Members of the admin group may gain root privileges"):
 #     superUsersNeu.write(line)
 #     superUsersNeu.write(sudoLine)
 #   else:  
 #     superUsersNeu.write(line)

  #os.system('mv sudoers sudoers.old && cp sudoers.neu sudoers')

def mapShare(s):
  print "Mapping the user share"
  print "Installing libpam-mount"
  os.chdir('security')
  os.system('sudo apt-get install libpam-mount')
  os.system('sudo chmod a+w pam_mount.conf.xml')

  strToWrite = '<volume user=\"*\"\nfstype=\"cifs\"\nserver=\"' + s + '\"\npath=\"home/%(DOMAIN_USER)\"\nmountpoint=\"~/H:_%(DOMAIN_USER)\"\n/>'

  print 'Writing: \n'
  print  strToWrite + '\n'
  print 'to \'etc/security/pam_mount.conf.xml'
  os.system('rm tempPamMount.xml')
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
      print line
    else:
      pamTemp.write(line)
      pamTemp.write('\n')
      print line  
 
  os.system('sudo rm pam_mount.conf.xml.old')
  os.system('mv pam_mount.conf.xml pam_mount.conf.xml.old') 
  os.system('mv tempPamMount.xml pam_mount.conf.xml')
  os.system('source pam_mount.conf.xml')
  os.chdir(os.pardir)
def profileTemplate():
  print "Got Here too"





setup()
