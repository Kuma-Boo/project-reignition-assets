import bpy
import colorsys

#from -1 to 1
brightness_change = .5
saturation_change = .5

#Generates a duplicate vertex group as a backup
for obj in bpy.context.selected_objects:
    #Not a mesh
    if obj.type != 'MESH':
        continue
    
    for poly in obj.data.polygons:
            for loop_index in poly.loop_indices:
                color = obj.data.color_attributes[0].data[loop_index].color
                hsv_col = colorsys.rgb_to_hsv(color[0], color[1], color[2])
                brightend_color = colorsys.hsv_to_rgb(hsv_col[0], hsv_col[1], hsv_col[2] + brightness_change)
                
                color[0] = brightend_color[0]
                color[1] = brightend_color[1]
                color[2] = brightend_color[2]
                
                obj.data.color_attributes[0].data[loop_index].color = color
