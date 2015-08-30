#!/usr/bin/python

import os, sys
path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'galleryforge',
)

sys.path.append(path)
import launch

os.chdir(path)
launch.main()
