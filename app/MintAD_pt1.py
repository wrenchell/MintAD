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

  raw_input("\nOtherwise, press ENTER to continue...")


def permissions():
  os.system('chmod a+x pbis-open-8.3.0.3287.linux.x86_64.deb.sh')
  run()

def run():
  os.system('./pbis-open-8.3.0.3287.linux.x86_64.deb.sh')


begin()
permissions()

print "\n\n Script executed successfully.  Ready for Reboot and part 2"
raw_input("Press any key to continue...")
