#!/usr/bin/python
###############################################################################
 #
 # Quick script to automate the third party app responces
 # 
##

print "Running pbis install script, this make take some time..."

import os
import subprocess 
child = subprocess.Popen(['bash','./pbis-open-8.3.0.3287.linux.x86_64.deb.sh'], stdin=subprocess.PIPE)

child.stdin('no')
child.stdin('yes')


