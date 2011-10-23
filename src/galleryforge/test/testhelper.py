"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import os, sys, Image, ImageDraw
import unittest

def createDummyImage(filename, x=800, y=600):
	img = Image.new("RGB", (x, y))
	draw = ImageDraw.Draw(img)
	draw.ellipse((200, 100, 600, 500), outline="#ffffff")
	draw.ellipse((202, 102, 598, 498), outline="#ffffff")
	img.save(filename)
	

def deteleFile(filename):
	os.remove(filename)


def splitPath(path, count=1):
	for i in range(0, count):
		path = os.path.split(path)[0]
	return path


def get_verbose():
	verbose = 1
	if len(sys.argv) > 1 and sys.argv[1] == "-v":
		verbose = 2
	sys.argv = sys.argv[:1]
	return verbose
