import bpy

for obj in bpy.context.selected_objects:
    if obj.data is not None:
        obj.data.name = obj.name

    #Not a mesh
    if obj.type != 'MESH':
        continue
    
    #Comment out if you want to keep uv names
    i = 0
    for uvmap in obj.data.uv_layers:
        uvmap.name = 'UVMap'
        i += 1
        if i > 1:
            uvmap.name = 'UVMap' + str(i)
    
    #Comment out if you want to keep multiple uvs
    #while len(obj.data.uv_layers) > 1:
    #    obj.data.uv_layers.remove(obj.data.uv_layers[1])
    #UV Code end
    
    #Combines vertex colors
    if len(obj.data.vertex_colors) == 0:
        continue
    
    original_vertex_color = obj.data.vertex_colors[0]
    skipped = False
    for vertex_colors_group in obj.data.vertex_colors:
        if not skipped:
            skipped = True
            continue
        
        i = 0
        for vertex_colors in vertex_colors_group.data:
            j = 0
            for value in vertex_colors.color:
                original_vertex_color.data[i].color[j] *= value
                j += 1
            i += 1
    
    #Clean up extra vertex color groups
    original_vertex_color.name = "VertexColor"
    while len(obj.data.vertex_colors) > 1:
        obj.data.vertex_colors.remove(obj.data.vertex_colors[1])
    #End Vertex Color
    
    
    #Removes Vertex Groups for all objects that don't have armatures
    if len(obj.modifiers) == 0:
        while len(obj.vertex_groups) > 0:
            obj.vertex_groups.remove(obj.vertex_groups[0])
    #End Vertex Group