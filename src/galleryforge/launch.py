#!/usr/bin/python
#
# <desc> Static HTML gallery generator from image directories </desc>

"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import sys
from gallery import Gallery
from logger import *
from config import config

def main(basepath=None):
	
	if basepath == None:
		if (len(sys.argv) == 2):
			basepath = sys.argv[1]
		else:
			print "Must supply basedir of gallery"
			return False
#			sys.exit(1)
	
	config.read()
	gallery = Gallery(basepath)
	if gallery.scanDirs():
		gallery.deleteIndex()
		gallery.createAlbums()
		
		log("Done.")


if __name__ == "__main__":
	main()
