#!/usr/bin/env python

import os, sys
path_root = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'galleryforge',
)
path = os.path.join(path_root, "gui")

sys.path.append(path_root)
sys.path.append(path)
import guimain

os.chdir(path)
guimain.main()
