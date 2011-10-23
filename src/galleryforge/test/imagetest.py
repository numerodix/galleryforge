#!/usr/bin/python

"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import sys
sys.path.append("..")

from image import *
from testhelper import *
from logger import *
import unittest, glob


class ImageTest(unittest.TestCase):
	
	testimg = "img.jpg"
	
	
	def setUp(self):
		makeQuiet()
		createDummyImage(self.testimg)
		
	
	def tearDown(self):
#		pass
		deteleFile(self.testimg)
		
	
	def testReadImage(self):
		"""testReadImage: readImage() should set up image object with dimensions"""
		
		img = GalleryImage(self.testimg)
		img.readImage()

		self.assertNotEqual(img.dim_x, 0)
		self.assertNotEqual(img.dim_y, 0)
	
	
	def testMakeThumbnail(self):
		"""testMakeThumbnail: makeThumbnail() should make thumbnail of 
		correct size"""
		
		target = "img_thumb.jpg"
		x = 200
		y = 150
		
		img = GalleryImage(self.testimg)
		img.makeThumbnail(x, y)

		tl = len(glob.glob(target))
		self.assertNotEqual(tl, 0)
		
		thumb = GalleryImage(target)
		thumb.readImage()
		dim_x = thumb.dim_x
		dim_y = thumb.dim_y
		
		deteleFile(target)
		
		self.assertEqual(dim_x, x)
		self.assertEqual(dim_y, y)
	
	
	def testRename(self):
		"""testRename: rename() should both rename image and assign new 
		filename to member"""

		target = "img2.jpg"
		img = GalleryImage(self.testimg)
		
		img.rename(target)
		t = glob.glob(target)[0]
		f = img.filename_root
		
		img.rename(self.testimg)
		
		self.assertEqual(target, t)
		self.assertEqual(target, f)
	
	
	def testConvert(self):
		"""testConvert(): convert() should convert to given format"""
		
		tifimg = "conv_img.tiff"
		createDummyImage(tifimg)
		img = GalleryImage(tifimg)
		
		img.convert(format='JPEG')
		img.readImage()
		deteleFile("conv_img.jpeg")
		
		self.assertEqual(img.format, 'JPEG')
	
	
	def testResize(self):
		"""testResize: resize() should yield dimensions of the target size"""
		dim_x = 600
		dim_y = 600
		
		img = GalleryImage(self.testimg)
		img.resize(dim_x, dim_y, aspect_ratio=False)
		img.readImage()
		
		self.assertEqual(dim_x, img.dim_x)
		self.assertEqual(dim_y, img.dim_y)


	def testGetAspectRatio(self):
		"""testGetAspectRatio: getAspectRation() should return correct 
		target dimensions"""
		oldx = 200
		oldy = 100
		
		newx = 50
		newy = 20
		
		img = GalleryImage(self.testimg)
		
		(x, y) = img.getAspectRation(oldx, oldy, newx, newy)
		self.assertEqual(x, 40)
		self.assertEqual(y, 20)
		
		(x, y) = img.getAspectRation(oldx, oldy, newy, newx)
		self.assertEqual(x, 20)
		self.assertEqual(y, 10)


	def testNoEnlargeImage(self):
		"""testNoEnlargeImage: resize() should never enlarge images"""
		img = GalleryImage(self.testimg)
		dim_x = img.dim_x
		dim_y = img.dim_y
		
		# trying to enlarge image
		img.resize(dim_x+100, dim_y+100, aspect_ratio=False)
		
		img.readImage()
		adim_x = img.dim_x
		adim_y = img.dim_y
		
		self.assertEqual(adim_x, dim_x)
		self.assertEqual(adim_y, dim_y)



def run(verbosity=1):
	suite = unittest.makeSuite(ImageTest)
	unittest.TextTestRunner(verbosity=verbosity).run(suite)


if __name__ == "__main__":
	run(verbosity=get_verbose())
