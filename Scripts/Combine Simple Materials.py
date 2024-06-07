import bpy
from bpy import context

import builtins as __builtin__

def console_print(*args, **kwargs):
    for a in context.screen.areas:
        if a.type == 'CONSOLE':
            c = {}
            c['area'] = a
            c['space_data'] = a.spaces.active
            c['region'] = a.regions[-1]
            c['window'] = context.window
            c['screen'] = context.screen
            s = " ".join([str(arg) for arg in args])
            for line in s.split("\n"):
                bpy.ops.console.scrollback_append(c, text=line)

def print(*args, **kwargs):
    """Console print() function."""

    console_print(*args, **kwargs) # to py consoles
    __builtin__.print(*args, **kwargs) # to system console
    
matDictionary = {
}

for obj in bpy.data.objects:
    if obj.type != "MESH":
        continue

    for mat_slot in obj.material_slots:
        if not mat_slot.material:
            continue
        
        if not mat_slot.material.node_tree:
            continue            
        
        found_image = False
        image_count = 0
        for x in mat_slot.material.node_tree.nodes:
            if x.type != 'TEX_IMAGE':
                if x.type == "BSDF_PRINCIPLED":
                    x.inputs[7].default_value = 0.0 #Remove specular
                    x.inputs[9].default_value = 1.0 #Max Roughness
                elif x.type != "OUTPUT_MATERIAL":
                    mat_slot.material.node_tree.nodes.remove(x)
                continue

            image_count += 1
            if x.image is None:
                continue
            
            found_image = True
            key = str(x.image.name).split('.')[0]

        if image_count is 1 and found_image is True:
            if key in matDictionary:
                m = matDictionary[key]
                mat_slot.material = m
            else:
                matDictionary[key] = mat_slot.material
            
            mat_slot.material.use_backface_culling = True