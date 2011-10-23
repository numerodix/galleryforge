#!/usr/bin/python

"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import os, glob, string, sys
from os.path import join, getsize
from config import config
from album import GalleryAlbum
from logger import *


class Gallery:
	
	rebuild_thumbnails = None
	dummyimg = None

	img_exts = None
	
	imgdirs = None
	basepath = None
	scriptpath = None
	
	index = None
	
	
	def __init__(self, basepath):
		self.scriptpath = os.getcwd()
		self.basepath = os.path.abspath(basepath)
		
		self.rebuild_thumbnails = config.settings['rebuild_thumbnails']
		self.dummyimg = config.settings['dummyimg']
		
		self.img_exts = config.settings['image_extensions']
		self.img_exts = self.img_exts.split(",")
	
	
	def scanDirs(self):
		if self.basepath == None:
			logfe("Basepath not set")
		
		imgdirs = []
		
		# find non-empty directories
		for root, dirs, files in os.walk(self.basepath):
			if not len(files) == 0:
				for file in files:
					for ext in self.img_exts:
						if (not file.find(ext) == -1) and (not file == self.dummyimg):
							if imgdirs.count(root) == 0:
								imgdirs.append(root)
		
		self.imgdirs = imgdirs
		self.imgdirs.sort()
		
		# transform absolute paths to relative path format
		for d in self.imgdirs:
			self.imgdirs[self.imgdirs.index(d)] = d[len(self.basepath)+1:]
				
		self.imgdirs.sort()
		
		if len(self.imgdirs) == 0:
			log("No images found in sub directories of " + self.basepath
				 + ", exiting.")
			return False
		if self.imgdirs[0] == "":
			log("No images found in sub directories of " + self.basepath
				 + ", exiting. Did you mistakenly place the images in "
				 + self.basepath + "?")
			return False
		
		return True


	def createAlbums(self):
		os.chdir(self.basepath)
		curdir = os.getcwd()
		
		for d in self.imgdirs:
			os.chdir(d)
			
			(name, title) = self.getDirName(d)
			
			logb("Now creating gallery " + d)
			
			album = GalleryAlbum(name, title)
			logt("Processing images")
			album.processImages(forcethumbs=self.rebuild_thumbnails)
			logt("Creating html pages")
			album.makeImagePages()
			album.constructAlbum()
			log("")
			
			os.chdir(curdir)
			
			self.addDirToIndex(d, name, title)
			
		os.chdir(self.scriptpath)


	def getDirName(self, directory):
		dirname, dirtitle = directory, directory
		if directory.count("/") >= 0:
			dirname = directory.split("/").pop()
		
		try:
			# first 8 chars are all digits, this is a date
			date = int(dirname[:8])
			dirtitle = dirname[9:]
		except ValueError:
			# fall back on using the whole dirname as a title
			dirtitle = dirname
		dirtitle = string.replace(dirtitle, "_", " ")
		
		return (dirname, dirtitle)


	def addDirToIndex(self, path, name, title):
#		print path, name, title
		
		path = os.path.split(self.basepath)[1] + os.sep + path
		
		# make list of dirs in path
		dirs = path.split(os.sep)
		levels = len(dirs)
		
		# read all lines from existing index into list
		indexfile = os.path.join(self.basepath, "index")
		tmp = open(indexfile, 'r')
		lines = []
		for line in tmp.xreadlines():
			lines.append(line)
		tmp.close()
		
		for d in dirs[1:]:
			
			# find level in path for this dir
			level = dirs.index(d)
			
			p = ""
			for g in dirs[:level+1]:
				p += g + "/"
			
			t = ""
			if level == levels-1:
				t += "l,"		# mark leaf dirs with l
			else:
				t += " ,"	# mark rest with level number
			t += str(level) + ","
			t += d + ","
			t += p
			t += "\n"
			
			# write every line to index if it's not already there
			if not t in lines:
				
				page = open(indexfile, 'a')
				page.write(t)
				page.close()
		


	def deleteIndex(self):
		index = os.path.join(self.basepath, "index")
		if os.path.exists(index):
			os.remove(index)
		i = open(index, 'w')
		i.close()

