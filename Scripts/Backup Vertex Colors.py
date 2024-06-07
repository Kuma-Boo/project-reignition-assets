import bpy

#Set to True to create a backup
#Set to False if replacing active vertex group with backup
backup = False
clear_backup = False #Set to True to delete backups

#Generates a duplicate vertex group as a backup
for obj in bpy.context.selected_objects:
	#Not a mesh
	if obj.type != 'MESH':
		continue

	if len(obj.data.color_attributes) == 0: #Nothing to backup
		continue

	bpy.context.view_layer.objects.active = obj
	
	if clear_backup:
		while len(obj.data.color_attributes) > 1:
			obj.data.color_attributes.remove(obj.data.color_attributes[1])	
		continue
	
	if backup:
		#Ensure there's only one vertex group
		while len(obj.data.color_attributes) > 1:
			obj.data.color_attributes.remove(obj.data.color_attributes[1])		
		bpy.ops.geometry.color_attribute_duplicate()
	elif len(obj.data.color_attributes) == 2:
		obj.data.color_attributes.remove(obj.data.color_attributes[0])
		bpy.ops.geometry.color_attribute_duplicate()
	
	obj.data.color_attributes[0].name = "VertexColor"
	
	if len(obj.data.color_attributes) <= 1: #No backup found
		continue
		
	obj.data.color_attributes[1].name = "VertexColorBackup"

	obj.data.color_attributes.active_color_index = 0
	bpy.ops.geometry.color_attribute_render_set(name="VertexColor")
		