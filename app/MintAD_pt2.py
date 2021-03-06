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
import errorCheck

finished1 = 'false'
finished2 = 'false'
finished3 = 'false'
skipNum = 0 
cwd = os.getcwd()

###############################################################################
 # 
 # setup
 #
 # First function call.  Mostly prints to the user.  Makes the subsequent 
 # function calls
 #
##
def setup():
  # Clear the terminal and print the header
  os.system('./utils/clear.py')
  os.system('./app/header.py')
  

  print "This script will edit several root config files\n"

  print "This could be potentially harmful to a system if not executed properly!"

  print "If you stumbled across this script on accident, just type [^C]"

  raw_input("\nOtherwise, press ENTER to continue...\n\n")
  serverInfo()


###############################################################################
 #
 # serverInfo
 # 
 # Prompts the user for and records the server name.
 # 
##
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


###############################################################################
 #
 # begin
 #
 # Serves as the main switchboard function for the class.  Calls all of the 
 # functions which do the writing to the sys files.
 #
 # NOTE: This function is likely unnessary.  I could probably consoildate the
 # functions to write in a more agnostic manner, but it would take time
 #
##
def begin(s):
  # We will be using this function as a switch to process other data

  os.system('./utils/clear.py')
  os.system('./app/header.py')

  sudoAdmins()
  mapShare(s)
  profileTemplate()
  end(s)


###############################################################################
 #
 # sudoAdmins
 #
 # sudoAdmins is the function that essentially 'writes' to the sudoers file.
 # It doesn't literally do this, as the level of permissions required to write
 # to 'sudoers' isn't really functially possible inside of a script.  Instead
 # it reads the entire 'sudoers' file, line by line, and writes it into a temp
 # file, adding what we need to add, where we need to add it.  It then backs up
 # the original 'sudoers' file as 'sudoers.old' and changes the temp file to 
 # be 'sudoers'.
 #
##
def sudoAdmins():
  os.chdir('/')
  os.chdir('etc')
  print "Giving domain admins sudo right"

  os.system('touch tempSudoers')

  sudoLine = '%DOMAIN_Admins ALL=(ALL)ALL'

  e = errorCheck.errorCheck()
  errorChecks = e.checkInput(sudoLine, 'sudoers')
  
  if (errorChecks == 'false'):
    print "\nWriting: "
    print "\n" + sudoLine + "\n"
    print "to \'/etc/sudoers\'\n\n"

    try:
      superUsers = open('sudoers', 'r+')
      tempSudoers = open('tempSudoers', 'r+')
    except IOError as err:
      print "I/O error ({0}): {1}".format(err.errno, err.strerror)
      sys.exit()

    print "Sucessfully opened \'etc\\sudoers\'\n"
   
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

    superUsers.close()
    tempSudoers.close()

    os.system('mv sudoers sudoers.old')
    os.system('mv tempSudoers sudoers')

  else:
    global skipNum
    skipNum += 1
    print "\nFile located at /etc/sudoers has already"
    print "been edited.  Not writing anything there.\n"


###############################################################################
 #
 # mapShare
 # 
 # The 'mapShare' function is basically the same as 'sudoAdmins' and performs 
 # and almost identical functionality.  As noted previously, could probably be
 # written in more agnostic fashion and consolidated.
 # 
##
def mapShare(s):
  print "Mapping the user share"
  print "\nInstalling libpam-mount"
  os.chdir('security')
  os.system('sudo apt-get install libpam-mount')

  strToWrite = '<volume user=\"*\"\nfstype=\"cifs\"\nserver=\"' + s + '\"\npath=\"home/%(DOMAIN_USER)\"\nmountpoint=\"~/H:_%(DOMAIN_USER)\"\n/>'
  strToTest = '<volume user=\"*\"'
  e = errorCheck.errorCheck()
  errorChecks = e.checkInput(strToTest, 'pam_mount.conf.xml')

  if (errorChecks == 'false'):
    print '\nWriting: \n'
    print  strToWrite + '\n'
    print 'to \'etc/security/pam_mount.conf.xml\'\n\n'

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
    
    pamMount.close()
    pamTemp.close()

    os.system('sudo rm pam_mount.conf.xml.old')
    os.system('mv pam_mount.conf.xml pam_mount.conf.xml.old') 
    os.system('mv tempPamMount.xml pam_mount.conf.xml')

  else:
    global skipNum 
    skipNum += 1
    print "\nFile located at /etc/security/pam_mount.conf.xml has already"
    print "been edited.  Not writing anything there.\n"

  os.chdir(os.pardir)


###############################################################################
 #
 # profileTemplate
 #
 # The function 'profileTemplate' is -- again -- almost identical in 
 # functionality to the preceeding functions.  Could probably be consoldated.
 #
##
def profileTemplate():
  print "Applying the user profile template."
  os.chdir('pam.d')
  os.system('touch tempCommon')
  
  plateStr = 'session required 	pam_mkhomedir.so skel=/home/template/ umask=0022'

  e = errorCheck.errorCheck()
  errorChecks = e.checkInput(plateStr, 'common-session')

  if (errorChecks == 'false'):
    print '\nWriting: '
    print '\n' + plateStr + '\n'
    print 'to \'etc/pam.d/common-session\'\n\n'
  
    try:
      profile = open('common-session', 'r+')
      tempProfile = open('tempCommon', 'r+')
    except IOError as err:
      print "I/O error ({0}): {1}".format(err.errno, err.strerror)
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

    profile.close()
    tempProfile.close()

    os.system('mv common-session common-session.old')
    os.system('mv tempCommon common-session')  

  else:
    global skipNum 
    skipNum += 1
    print "\nThe File located at /etc/pam.d/common-session has already"
    print "been edited.  Not writing anything there.\n"

###############################################################################
 #
 # end
 # 
 # Honestly, do I need to explain this function?  No?  Good.
 #
##
def end(s):
  os.chdir("/")
  os.chdir('/etc')

  finalCheck = errorCheck.errorCheck()
  
  finished1 = finalCheck.checkInput('%DOMAIN_Admins ALL=(ALL)ALL','sudoers')

  os.chdir('security')
  finished2 = finalCheck.checkInput('<volume user=\"*\"','pam_mount.conf.xml')
  os.chdir(os.pardir)

  os.chdir('pam.d')
  finished3 = finalCheck.checkInput('session required 	pam_mkhomedir.so skel=/home/template/ umask=0022','common-session')
  
  errorNum = 0

  raw_input("\n\nScript has finished!  Press ENTER to continue...")
  os.chdir(cwd)
  os.system('./utils/clear.py')
  os.system('./app/header.py')

  print "Testing the files that were changed during the script."
  print "Testing /etc/sudoers: " + finished1
  print "Testing /etc/security/pam_mount.conf.xml: " + finished2
  print "Testing /etc/pam.d/common-session: " + finished3 + '\n\n'

  if (finished1 == 'false'):
    print "ERROR!  The file located at /etc/sudoers did not edit!"
    errorNum += 1
  if (finished2 == 'false'):
    print "ERROR! The file located at /etc/security/pam_mount.xml.conf did not edit!"
    errorNum += 1
  if (finished3 == 'false'):
    print "ERROR! The file located at /etc/pam.d/common-session did not edit!"
    errorNum += 1

  if (errorNum > 0):
    print "\nFinished with " + str(errorNum) + " errors!  This configuration has failed.  You will have to try again.  Exiting."
    sys.exit()  

  else:
    if (skipNum > 0):
      print "This script has finished without editing " + str(skipNum) 
      print "files because the files already had the lines we needed to add."  
      print "This is odd.  Check and make sure everything is ok.\n"

    print "Linux Mint Active Directory Intregration Completed!"
    print "The system must be restarted for most changes to take effect."

    raw_input('Press Enter to end...')


###############################################################################
 #
 # Function calls
 #
##  
setup()
