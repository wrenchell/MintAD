#!/usr/bin/python

###############################################################################
 #
 # errorCheck
 #
 # Error check will be an object class to help facilitate bullet proofing in 
 # MintAD scripts.
 #
 # Author: Mitchell Thompson
 # Copyright: Unitas-Inc 2016 07 08
 #
##

import sys
import os

class errorCheck():

  def checkInput(self, s, filename):
    error = 'false'
    
    linetoTest = s
    
    try:
      testF = open(filename, 'r')
    except IOError as err:
      print "In error Check I/O error ({0}): {1}".format(err.errno, err.strerror)
      print "File that failed was " + filename 
      sys.exit()

    for line in testF:
      line = line.strip()
      if (line == linetoTest):
        error = 'true'    
    testF.close() 
    return error
