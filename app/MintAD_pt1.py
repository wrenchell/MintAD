#!/usr/bin/python

###############################################################################
 #
 # MintAD_pt1
 #
 # The first part of the python script to automate some of the more time 
 # eating steps of setting up active directory in Linux Mint.  This first part
 # should basically only add executable permisisons to the installer script and
 # then run that script.
 #
 # Author: Mitchell Thompson
 # Copyright: Unitas-inc  2016/07/07
##

import sys 
import os

# The begin function will start the script by outputing relevent info to the 
# user.
def begin():
  # Clearing the terminal for prettier output (UGLY METHOD)
  os.system('./utils/clear.py')
  os.system('./app/header.py')

  print """This script will give +x permissions to the bash script titled:
          \n\'pbis-open-8.3.0.3287.linux.x86_64.deb.sh\'\n"""
  
  print "This could be potentially harmful to a system if not executed properly!"
  
  print "If you stumbled across this script on accident, just type [^C]"

  raw_input("\nOtherwise, press ENTER to continue...\n\n")

  getInput()

def getInput():
  os.system('./utils/clear.py')
  os.system('./app/header.py')

  domainInput = raw_input('Enter the DOMAIN name: ')
  domainName = domainInput.upper()

  accntName = raw_input('Enter the user account name: ')
  
  os.system('./utils/clear.py')
  os.system('./app/header/.py')

  print "Domain name is : " + domainName
  print "Account name is: " + accntName

  correct = raw_input("Are these correct? (y/n): ")
  upperAnswer = correct.upper()
 
  if (upperAnswer != 'Y'):
    getInput()
  else:
    permissions(domainName, accntName)
    print "\n\n\n\n"
  

def permissions(d, a):
  os.system('chmod a+x pbis-open-8.3.0.3287.linux.x86_64.deb.sh')
  run(d, a)


def run(d, a):
  os.system('./pbis-open-8.3.0.3287.linux.x86_64.deb.sh')
  
  print "\n\nFinished bash script execution.  Running the newly installed scriptlocated in:"
  
  print "/opt/pbis/bin/domainjoin-cli\n\n"

  # We need to change pwd to be able to access what was just unpacked
  # We will change back right after
  os.chdir("/")
  os.system('./opt/pbis/bin/domainjoin-cli')
  os.chdir(os.pardir)
 

begin()

print "\n\n Script executed successfully.  Ready for Reboot and part 2"
raw_input("Press any key to continue...")
