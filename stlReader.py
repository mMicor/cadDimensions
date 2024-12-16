#!/usr/bin/python

# Python script to find STL dimensions
# Requrements: sudo pip install numpy-stl

import math
import stl
from stl import mesh
import numpy

# this stolen from numpy-stl documentation
# https://pypi.python.org/pypi/numpy-stl

# find the max dimensions, so we can know the bounding box, getting the height,
# width, length (because these are the step size)...
def extract_dimensions(cad_file):
    cad_mesh = mesh.Mesh.from_file(cad_file)
    minx = maxx = miny = maxy = minz = maxz = None
    for p in cad_mesh.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)

    width = maxx - minx
    height = maxy - miny
    area = width * height

    return {
        'width': width,
        'height': height,
        'area': area
    }

#main_body = mesh.Mesh.from_file(cad_file)

#minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(main_body)

# the logic is easy from there

#print ("File:", sys.argv[1])
#print ("X:", maxx - minx)
#print ("Y:", maxy - miny)
#print ("Z:", maxz - minz)