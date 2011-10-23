#!/usr/bin/python

"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import sys, shutil
sys.path.append("..")

import launch
from config import config
from testhelper import *
from logger import *
import unittest, glob, time


class BlackBoxTest(unittest.TestCase):
	
	location = "gallery/cat/subcat/subsubcat/album"
	location2 = "gallery/cat/subcat2/subsubcat/album"
	location3 = "gallery/cat/subcat/subsubcat2/album"
	location4 = "gallery/cat2/subcat/subsubcat2/album"
	
	locations = [location, location2, location3, location4]
	
	absloc = os.path.abspath("gallery")
	
	imfile = "img.jpg"
	path = os.path.abspath(os.path.join(location, imfile))

	
	def setUp(self):
		makeQuiet()
		if os.path.exists(self.absloc):
			shutil.rmtree(self.absloc)
		for i in self.locations:
			abspath = os.path.abspath(i)
			os.makedirs(abspath)
	
	
	def tearDown(self):
		if os.path.exists(self.absloc):
			pass
			shutil.rmtree(self.absloc)
	
	
	def testNoClobber(self):
		"""testNoClobber: don't overwrite images from a previous run"""
		file = "0001.jpg"
		path = os.path.abspath(os.path.join(self.location, file))

		createDummyImage(path)
		
		launch.main(basepath=self.absloc)
		
		before_date = os.path.getmtime(path)
		
		launch.main(basepath=self.absloc)
		
		after_date = os.path.getmtime(path)
		
		self.assertEqual(before_date, after_date)


	def testScanDirs(self):
		"""testScanDirs: process [only] all directories with images"""
		for i in self.locations:
			imfile = os.path.join(i, self.imfile)
			
			if not i == self.location3:
				createDummyImage(imfile)
		
		launch.main(basepath=self.absloc)
		
		for i in self.locations:
			abspath = os.path.abspath(i)
			files = glob.glob(os.path.join(abspath, "*"))
			
			if i == self.location3:
				self.assertEqual(len(files), 0)
			else:
				search_for = ["0001.jpg", "0001_thumb.jpg", "0001.html",
					"a0001.html", "index.php", config.settings['dummyimg']]
				for f in search_for:
					absfile = os.path.join(abspath, f)
					self.assertTrue(absfile in files)


	def testRebuildThumbnails(self):
		"""testRebuildThumbnails: thumbnails should be rebuilt (broken on win32)"""
		
		file = "0001_thumb.jpg"
		path = os.path.abspath(os.path.join(self.location, file))
		createDummyImage(self.path)
		
		launch.main(basepath=self.absloc)
		
		before_date = os.path.getmtime(path)
		
		time_pre = time.strftime("%S", time.gmtime())
		time.sleep(1)		# make sure they are not created too soon
		time_post = time.strftime("%S", time.gmtime())
		self.assertNotEqual(time_pre, time_post)	# if test fails, should be here
		
		config.settings['rebuild_thumbnails'] = True
		launch.main(basepath=self.absloc)
		
		after_date = os.path.getmtime(path)
		self.assertNotEqual(before_date, after_date)


	def testMakeTargetFormat(self):
		"""testMakeTargetFormat: convert from non-web format to jpeg"""
		file = "0001.tiff"
		path = os.path.abspath(os.path.join(self.location, file))
		createDummyImage(path)
		
		launch.main(basepath=self.absloc)
		
		files = glob.glob(os.path.join(self.location, "0001.jp*"))
		parts = os.path.splitext(files[0])
		self.assertEqual(parts[1], ".jpeg")


	def testCheckIndex(self):
		"""testCheckIndex: index file should be well formed"""
		indexfile = os.path.join(self.absloc, "index")
		
		for i in self.locations:
			file = os.path.join(i, self.imfile)
			createDummyImage(file)
		
		launch.main(basepath=self.absloc)
		
		self.assertTrue(os.path.exists(indexfile))
		
		tmp = open(indexfile, 'r')
		lines = []
		for line in tmp.xreadlines():
			lines.append(line)
		tmp.close()
		
		for line in lines:
			parts = line.split(",")
			path = os.path.abspath(parts[3][:-1])
			path_exists = os.path.exists(path)
			self.assertTrue(path_exists)




def run(verbosity=1):
	suite = unittest.makeSuite(BlackBoxTest)
	unittest.TextTestRunner(verbosity=verbosity).run(suite)


if __name__ == "__main__":
	run(verbosity=get_verbose())