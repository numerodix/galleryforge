#!/usr/bin/python

"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Jan. 13, 2006

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import sys
sys.path.append("..")

from config import config
from testhelper import *
from logger import *
import unittest, glob

class ConfigTest(unittest.TestCase):
	
	
	def setUp(self):
		makeQuiet()
	
	
	def tearDown(self):
		settings = {}
		config.store(settings)
	
	
	def testSetProperty(self):
		"""testProperty: set a property and check that it's set"""
		set_value = '45'
		
		config.settings['image_size_x'] = set_value
		read_value = config.settings['image_size_x']
		
		self.assertEqual(set_value, read_value)
	
	
	def testWriteProperty(self):
		"""testWriteProperty: set a property, write config file, then read it back"""
		set_value = '45'
		
		settings = {}
		settings['image_size_x'] = set_value
		config.store(settings)
		
		config.read()
		read_value = config.settings['image_size_x']
		
		self.assertEqual(set_value, read_value)




def run(verbosity=1):
	suite = unittest.makeSuite(ConfigTest)
	unittest.TextTestRunner(verbosity=verbosity).run(suite)


if __name__ == "__main__":
	run(verbosity=get_verbose())
