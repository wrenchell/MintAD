#!/usr/bin/python

###############################################################################
 #
 # Simple script to clear the terminal screen to make output look better
 #
 # Copyright (C) 2016 June 02  Mitchell Thompson
 #
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program.  If not, see <http://www.gnu.org/licenses/>.
 #
 ##

import sys

def clear() :
	"""Clear screen, return cursor to top left"""
	sys.stdout.write('\033[2J')
	sys.stdout.write('\033[H')
	sys.stdout.flush()

clear()
