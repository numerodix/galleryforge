#!/usr/bin/python

"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""


import sys
import imagetest
import blackboxtest
import configtest
import testhelper

verbose = testhelper.get_verbose()

imagetest.run(verbose)
blackboxtest.run(verbose)
configtest.run(verbose)
