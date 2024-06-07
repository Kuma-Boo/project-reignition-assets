# Copyright (c) 2019 Winston Yallow.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
#, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# This script was created in a very quick and dirty way for a game jam. Use
# at your own risk. This file may overwrite files.
# When you run this script inside blender it will export EVERY Curve it can
# find. The exported file will be named based on the object name in blender.
# Be sure to only use valid file name characters. The location will be in
# the same folder as the .blend file.

# It looks like tilted points have some bugs. I do not need tilted points so
# this will remain unfixed. If you know a solution feel free to comment on
# https://gist.github.com/winston-yallow/41b2bab5bd71dc7711ecc4a761a3632c

# Uncomment the next line only when you are sure that you want to use this
# script (at your own risk):
import bpy
from mathutils import *
from math import *

C = bpy.context
D = bpy.data

precision = 4
export_template = """[gd_resource type="Curve3D" format=2]

[resource]
_data = {{
"points": PoolVector3Array( {points_str} ),
"tilts": PoolRealArray( {tilts_str} ),
}}
widths = [{width_str}]
up_vector_enabled = false
"""

# Copy 'widths = []' to the actual Path3D node's properties.


def abs_path(name):
    return bpy.path.abspath("//" + name)


def export_curve(off, curve, name, template=export_template, p=precision):
    print("EXPORT:", name)
    
    points = []
    tilts = []
    widths = []
    
    for bezpoint in curve.bezier_points:
        
        point = bezpoint.co + off
        handle_l = bezpoint.handle_left - bezpoint.co
        handle_r = bezpoint.handle_right - bezpoint.co
        
        # We use the same conventions as the blender exporter plugin.
        # This way it is easy to combine them.
        points += [
            handle_l.x, handle_l.z, -handle_l.y,
            handle_r.x, handle_r.z, -handle_r.y,
            point.x, point.z, -point.y
        ]
        tilts.append(bezpoint.tilt)
        widths.append(bezpoint.radius)
    
    # round everything to prevent errors in godot:
    points = [round(i, p) for i in points]
    tilts = [round(i, p) for i in tilts]
    
    file_content = template.format(
        points_str=", ".join(str(i) for i in points),
        tilts_str=", ".join(str(i) for i in tilts),
        width_str=", ".join(str(i) for i in widths),
    )
    
    with open(name, "w") as f:
        f.write(file_content)


for obj in C.scene.objects:
    if obj.type == "CURVE":
        positionOffset = obj.data.splines[0].bezier_points[0].co; #Offset of object
        if len(obj.data.splines) == 1:
            export_file_name = abs_path(obj.name + ".tres")
            export_curve(
                obj.location - positionOffset,
                obj.data.splines[0],
                export_file_name
            )
        else:
            i = 0
            for subcurve in obj.data.splines:
                export_file_name = abs_path(obj.name + "_" + str(i) + ".tres")
                export_curve(
                    obj.location - positionOffset,
                    subcurve,
                    export_file_name
                )
                i += 1
