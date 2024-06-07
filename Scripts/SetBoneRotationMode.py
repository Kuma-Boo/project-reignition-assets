import bpy
from bpy import context

to_mode = 'XYZ'

for pb in context.selected_pose_bones:
    pb.rotation_mode = to_mode