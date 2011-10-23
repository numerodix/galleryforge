"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import os, glob, shutil, string
import Image
from logger import *
from config import config

class GalleryImage:
	
	filename_root = None
	thumbnail_filename = None
	
	format = None
	dim_x = 0
	dim_y = 0
	
	has_thumbnail = False
	thumbnail_suffix = None
	
	image_quality = None
	thumb_quality = None
	
	
	def __init__(self, filename_root):
		self.filename_root = filename_root
		
		self.image_quality = int(config.settings['image_quality'])
		self.thumb_quality = int(config.settings['thumbnail_quality'])
		
		self.readImage()
	
	
	def readImage(self):
		img = Image.open(self.filename_root)
		self.format = img.format
		(self.dim_x, self.dim_y) = img.size
		
		self.thumbnail_suffix = config.settings['thumbnail_suffix']
		(root, ext) = os.path.splitext(self.filename_root)
		self.thumbnail_filename = root + self.thumbnail_suffix + ext
		
	
	def rename(self, targetname):
		if len(glob.glob(targetname)) >= 1:
			logmw("Skipping rename for " + targetname)
			return
		
		logm("Renaming " + targetname)
		os.rename(self.filename_root, targetname)
		self.filename_root = targetname
		self.readImage()
	
	
	def makeTargetFormat(self):
		(root, ext) = os.path.splitext(self.filename_root)
		if not ext in ('.jpg', '.jpe', '.jpeg', '.gif', '.png'):
			self.convert()
	
	
	def convert(self, format='JPEG'):
		(root, ext) = os.path.splitext(self.filename_root)
		new_name = root + "." + string.lower(format)
		
		img = Image.open(self.filename_root)
		img.save(new_name, format, quality=100)
		del img # deallocate object to avoid file locks
		
		os.remove(self.filename_root)
		self.filename_root = new_name
		self.readImage()
	
	
	def hasThumbnail(self):
		if len(glob.glob(self.thumbnail_filename)) != 0:
			return True
		return False
	
	
	def makeThumbnail(self, x, y):
		if self.hasThumbnail():
			logmw("Skipping thumbnail for " + self.filename_root)
			return
		
		logm("Creating thumbnail for " + self.filename_root)
		shutil.copyfile(self.filename_root, self.thumbnail_filename)
		thumb = GalleryImage(self.thumbnail_filename)
		thumb.resize(x, y, qual=self.thumb_quality)
		
	
	def deleteThumbnail(self):
		if os.path.exists(self.thumbnail_filename):
			os.remove(self.thumbnail_filename)

	
	def makeTargetSize(self, x, y):
		self.resize(x, y, qual=self.image_quality)
	
	
	def resize(self, x, y, filt=Image.ANTIALIAS, aspect_ratio=True, qual=95):
		self.readImage()
		
		# keep aspect ration intact
		if aspect_ratio:
			(x, y) = self.getAspectRation(self.dim_x, self.dim_y, x, y)
			
		# dimensions are already of target size, exiting
		# also, do not enlarge images
		if (x >= self.dim_x) and (y >= self.dim_y):
			logmw("Skipping resize for " + self.filename_root)
			return
		
		logm("Resizing " + self.filename_root)
		img = Image.open(self.filename_root)
		size = (x, y)
		imgres = img.resize(size, filt)
		imgres.save(self.filename_root, quality=qual)


	def getAspectRation(self, oldx, oldy, x, y):
		oldr = float(oldx) / float(oldy)
		r = float(x) / float(y)
		
		f = 1
		if oldr > r:
			f = float(oldx) / float(x)
		else:
			f = float(oldy) / float(y)
			
		x = int(oldx / f)
		y = int(oldy / f)

		return (x, y)


