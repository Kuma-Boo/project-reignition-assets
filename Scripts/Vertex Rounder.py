import bpy

precision = 1000

for obj in bpy.context.selected_objects:
    if obj.type != "MESH":
        continue

    for vert in obj.data.vertices:
        vert.co.x = round(vert.co.x * precision) / precision
        vert.co.y = round(vert.co.y * precision) / precision
        vert.co.z = round(vert.co.z * precision) / precision