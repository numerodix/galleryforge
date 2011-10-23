"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import os
from ConfigParser import SafeConfigParser
from logger import *
import logger

class config:
	
	settings = {}
	
	settings['gallery_path'] = ""
	
	settings['image_size_x'] = 740
	settings['image_size_y'] = 740
	
	settings['thumbnail_size_x'] = 200
	settings['thumbnail_size_y'] = 200
	#	thumbnail_size_y = int( thumbnail_size_x * 0.75 )
	settings['thumbnail_suffix'] = "_thumb"
	
	settings['image_quality'] = 95
	settings['thumbnail_quality'] = 85
	
	settings['album_cols'] = 2
	settings['album_rows'] = 3
	
	settings['image_extensions'] = "jpg,jpe,jpeg,gif,png,tif,tiff"
	
	settings['rebuild_thumbnails'] = False
	
	settings['dummyimg'] = "null.png"
	
	settings['tmp_first'] = "[&lt;&lt; First]"
	settings['tmp_prev'] = "[&lt; Previous]"
	settings['tmp_index'] = "[Index]"
	settings['tmp_next'] = "[Next &gt;]"
	settings['tmp_last'] = "[Last &gt;&gt;]"
	
	settings['script_basepath'] = os.path.abspath(os.path.dirname(logger.__file__))
	
	settings['template_dir'] = "templates"
	
	settings['template_image'] = os.path.join(settings['template_dir'], "image.tmp")
	settings['template_album'] = os.path.join(settings['template_dir'], "album.tmp")
	settings['template_index'] = os.path.join(settings['template_dir'], "index.tmp")
	
	
	section = "Main"
	
	home = None
	if os.name == "posix":
		home = os.environ['HOME']
	elif os.name == "nt":
		home = os.environ['USERPROFILE']
	
	config_file = os.path.join(home, ".galleryforgerc")
	
	
	def store(cls, settings):
		log("Saving settings to file " + cls.config_file)
		conf = SafeConfigParser()
		conf.add_section(cls.section)
		for i in settings:
			conf.set(cls.section, i, str(settings[i]))
		cfile = open(cls.config_file, "w")
		conf.write(cfile)
		cfile.close()
	
	
	def read(cls):
		if os.path.exists(cls.config_file):
			log("Loading settings from file " + cls.config_file)
			conf = SafeConfigParser()
			cfile = open(cls.config_file, "r")
			conf.readfp(cfile)
			for i in conf.items(cls.section):
				if i[1] == "True":
					cls.settings[i[0]] = True
				elif i[1] == "False":
					cls.settings[i[0]] = False
				else:
					cls.settings[i[0]] = i[1]
			#for i in settings:
				#conf.set("Main", i, str(settings[i]))
		
			cfile.close()
		return cls.settings
	
	
	store = classmethod(store)
	read = classmethod(read)


if __name__ == "__main__":
	config.settings['image_size_x'] = '740'
	print config.settings['image_size_x']
