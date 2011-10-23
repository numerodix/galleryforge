"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import logging, os
import output


def setCommonLogParams(level=logging.INFO):
	logging.basicConfig(
		level=level,
		format='%(message)s'
	)


def makeVerbose():
	setCommonLogParams(logging.INFO)


def makeQuiet():
	setCommonLogParams(logging.CRITICAL)


def logb(s):
	m = "\n"
	p(m)
	m = " " + output.white("+")*77
	p(m)
	m = " " + 3*"+" + " " + output.green(s)
	p(m)
	m = " " + output.white("+")*77 + "\n"
	p(m)

def logm(s):
	m = output.green(" * ") + output.white(s)
	p(m)

def logmw(s):
	m = output.yellow(" * ") + output.white(s)
	p(m)

def logfe(s):
	m = "Fatal error: " + output.red(s)
	p(m)

def logt(s):
	m = output.green("  +++++ ") + output.white(s)
	m += output.green(" +++++ ") + "\n"
	p(m)

def log(s):
	p(s)


def p(s):
	if not os.name == "posix":
		output.nocolor()
	logging.basicConfig(format='%(message)s')
	logging.error(s)



if __name__ == "__main__":
	makeVerbose()
	log("testing")