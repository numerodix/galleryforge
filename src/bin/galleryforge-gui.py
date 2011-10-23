#!/usr/bin/python

import os, sys
path_root = os.path.join("None")
path = os.path.join("None", "gui")

sys.path.append(path_root)
sys.path.append(path)
import guimain

os.chdir(path)
guimain.main()
