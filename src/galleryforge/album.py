#!/usr/bin/python

"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import os, glob, re, string
import Image
from config import config
from image import GalleryImage
from logger import *

class GalleryAlbum:
	
	dirname = None
	title = None
	images = []
	
	rows = None
	cols = None

	template_image = None
	template_album = None
	template_index = None
		
	dummyimg = None
	
	thumbnail_suffix = None
	
	img_exts = None
	
	
	def __init__(self, dirname, title):
		self.dirname = dirname
		self.title = title
		
		self.rows = int(config.settings['album_rows'])
		self.cols = int(config.settings['album_cols'])

		self.template_image = os.path.join(config.settings['script_basepath'],
			config.settings['template_image'])
		self.template_album = os.path.join(config.settings['script_basepath'],
			config.settings['template_album'])
		self.template_index = os.path.join(config.settings['script_basepath'],
			config.settings['template_index'])
			
		self.dummyimg = config.settings['dummyimg']
		
		self.thumbnail_suffix = config.settings['thumbnail_suffix']
		
		self.img_exts = config.settings['image_extensions']
		self.img_exts = self.img_exts.split(",")
	
	
	def scanImages(self):
		imgs = []
		
		# can all images in directory
		for i in self.img_exts:
			imgs.extend(glob.glob("*" + i))
			imgs.extend(glob.glob("*" + string.upper(i)))
		imgs.sort()
		
		self.images = imgs[:]
		
		# filter
		for i in imgs:
			# thumbnail
			if not i.count(self.thumbnail_suffix) == 0:
				self.images.remove(i)
			# dummyimg
			if i == self.dummyimg:
				self.images.remove(i)
			# duplicates
			if self.images.count(i) > 1:
				for c in range(1, self.images.count(i)):
					self.images.remove(i)


	def processImages(self, forcethumbs=False):
		self.scanImages()
		
		self.createDummyImage(self.dummyimg)
		
		c = 0
		for i in self.images:
			c += 1
			
			# create image object
			img = GalleryImage(i)
			
			if forcethumbs:
				img.deleteThumbnail()
			
			# rename image
			(root, ext) = os.path.splitext(i)
			num = string.zfill(str(c), 4)
			img.rename(num + ext)
			
			# convert if non-web format
			img.makeTargetFormat()
			self.images[c-1] = img.filename_root
			i = img.filename_root
			
			# make thumbnail
			img.makeThumbnail(config.settings['thumbnail_size_x'],
				config.settings['thumbnail_size_y'])
			
			# resize image to max allowed dimensions
			img.makeTargetSize(config.settings['image_size_x'],
				config.settings['image_size_y'])
				
			log("")	#newline
	
	
	def constructAlbum(self):
		logm("Creating album pages for " + self.dirname)
		
		self.createIndexPage()
		
		c = len(self.images)
		
		npages = c / ( self.rows * self.cols )
		if (c % ( self.rows * self.cols )):
			npages += 1
		
		for i in range(1, npages+1):
			npage = string.zfill(str(i), 4)
			
			lower = ( i - 1 ) * ( self.rows * self.cols ) + 1
			upper = ( i ) * ( self.rows * self.cols )
			
			imgs = self.images[lower-1:upper]
			self.constructAlbumPage(npage, npages, imgs)
	
	
	def constructAlbumPage(self, npage, npages, imgs):
		c = len(imgs)
		html = ""
		
		imgs.reverse()
		
		halt = False
		html += '<table class="classic">\n'
		for i in range(0, self.rows):
			if halt:
				break
			
			html += "\t<tr>\n\t"
			for i in range(0, self.cols):
				html += "\t<td>"
				if len(imgs) == 0:
					halt = True
				else:
					img = imgs.pop()
					(root, ext) = os.path.splitext(img)
					thumb = root + self.thumbnail_suffix + ext
					
					html += '<a href="' + root + '.html">'
					html += '<img class="albumimage" src="' + thumb + '"'
					html += ' alt="' + img + '"/>'
					html += '</a>'
				html += "</td>\n\t"
			html += "</tr>\n"
		html += "</table>\n"
		
		# set up navigation links
		(first, prev, index, next, last) = self.getNavLinks(int(npage),
			npages, ntype="album")
		
		# do template substitutions
		t = self.readTemplate(self.template_album)
		tmp = string.Template(t)
		out = tmp.substitute(album=html, title=self.title, first=first,
			prev=prev, next=next, last=last)
		
		# write page to disk
		page = open("a" + npage + ".html", 'w')
		page.write(out)
		page.close()
	
	
	def makeImagePages(self):
		logm("Creating image pages for " + self.dirname)
		self.scanImages()
		for i in self.images:
			self.constructImagePage(i)


	def constructImagePage(self, imagefile):
		# set up common variables
		(root, ext) = os.path.splitext(imagefile)

		# set up navigation links
		(first, prev, index, next, last) = self.getNavLinks(int(root),
			len(self.images))
		
		# do template substitutions
		t = self.readTemplate(self.template_image)
		tmp = string.Template(t)
		out = tmp.substitute(image=imagefile, title=self.title,
			first=first, prev=prev, index=index, next=next, last=last)
		
		# write page to disk
		page = open(root + ".html", 'w')
		page.write(out)
		page.close()
		

	def getNavLinks(self, cur, total, ntype="page"):
		if ntype == "album":
			html = '<a href="a${url}.html">${text}</a>'
		else:
			html = '<a href="${url}.html">${text}</a>'
		tmp = string.Template(html)
		
		first = config.settings['tmp_first']
		prev = config.settings['tmp_prev']
		index = config.settings['tmp_index']
		next = config.settings['tmp_next']
		last = config.settings['tmp_last']
		
		c = len(self.images)

		marker = -1
		if not cur == 1:
			marker = str(cur - 1)
			prev = tmp.substitute(text=config.settings['tmp_prev'],
				url=string.zfill(str(marker), 4))
			marker = str(1)
			first = tmp.substitute(text=config.settings['tmp_first'],
				url=string.zfill(str(marker), 4))
			
		if not cur == total:
			marker = str(cur + 1)
			next = tmp.substitute(text=config.settings['tmp_next'],
				url=string.zfill(str(marker), 4))
			marker = str(total)
			last = tmp.substitute(text=config.settings['tmp_last'],
				url=string.zfill(str(marker), 4))
		
		if not ntype == "album":
			marker = str( cur / ( self.rows * self.cols) )
			if not (cur % ( self.rows * self.cols)) == 0:
				marker = str( int(marker) + 1 )
			index = tmp.substitute(text=config.settings['tmp_index'],
				url="a"+string.zfill(str(marker), 4))

		return (first, prev, index, next, last)


	def createIndexPage(self):
		t = self.readTemplate(self.template_index)
		
		# write page to disk
		page = open("index.php", 'w')
		page.write(t)
		page.close()


	def readTemplate(self, filename):
		tmp = open(filename, 'r')
		s = ""
		for line in tmp.xreadlines():
			s+= line
		tmp.close()
		
		return s


	def createDummyImage(self, filename, x=1, y=1):
#		x=500
#		y=500
		if not os.path.exists(filename):
			img = Image.new("RGBA", (x, y))
			img.putpixel((0,0), (255, 255, 255, 0))
			img.save(filename)




if __name__ == "__main__":
	album = GalleryAlbum(".", ".")
	logt(" +++ Processing images +++ ")
	album.processImages()
	print " +++ Creating html pages +++ "
	album.makeImagePages()
	album.constructAlbum()
