#!/usr/bin/env python

from distutils.core import setup

setup(
	name='galleryforge',
	version='1.1.5',
	description='Creates static HTML album pages and images pages recursively',
	author='Martin Matusiak',
	author_email='numerodix@gmail.com',
	url='http://www.juventuz.net/numerodix/code.php',
	license='GPL',
	packages=['galleryforge', 'galleryforge.test', 'galleryforge.gui'],
#	package_dir = {'galleryforge': 'src'},
)
