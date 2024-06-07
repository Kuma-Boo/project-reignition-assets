import os
import bpy

path = r"C:\Users\Kuma\Documents\GitHub\Sonic Remake Project\Models\Sand Oasis\original rip";
path = path.replace('\\', '/');
path_to_obj_dir = os.path.join('s:\\', path)
file_list = sorted(os.listdir(path_to_obj_dir))
obj_list = [item for item in file_list if item.endswith('.dae')]
for item in obj_list:
    path_to_file = os.path.join(path_to_obj_dir, item)
    bpy.ops.wm.collada_import(filepath = path_to_file)