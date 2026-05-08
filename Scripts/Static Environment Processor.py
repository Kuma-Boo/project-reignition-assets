import bpy

def cleanup_and_join_by_material():
    # Ensure we are in Object Mode
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    # Get all visible mesh objects in the current view layer
    visible_meshes = [obj for obj in bpy.context.visible_objects if obj.type == 'MESH']
    visible_armatures = [obj for obj in bpy.context.visible_objects if obj.type == 'ARMATURE']

    # 1. Unparent meshes and clear transformations (keep transform)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in visible_meshes:
        obj.select_set(True)
    
    # Unparent while keeping visual transformation
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

    # 2. Clear all Modifiers and Vertex Groups
    for obj in visible_meshes:
        obj.modifiers.clear()
        obj.vertex_groups.clear()

    # 3. Delete Armatures
    bpy.ops.object.select_all(action='DESELECT')
    for arm in visible_armatures:
        arm.select_set(True)
    bpy.ops.object.delete()

    # 4. Join meshes by Material
    # Create a dictionary to group objects by their active material
    material_map = {}

    for obj in visible_meshes:
        # Get the first material slot name (or "None" if empty)
        mat_name = obj.active_material.name if obj.active_material else "NoMaterial"
        
        if mat_name not in material_map:
            material_map[mat_name] = []
        material_map[mat_name].append(obj)

    # Perform the join operation for each material group
    for mat_name, objs in material_map.items():
        if len(objs) > 1:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in objs:
                obj.select_set(True)
            
            # Set the first object as active to act as the join target
            bpy.context.view_layer.objects.active = objs[0]
            bpy.ops.object.join()

    print("Cleanup and Material Join complete.")

# Execute the function
cleanup_and_join_by_material()