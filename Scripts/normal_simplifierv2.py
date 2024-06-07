bl_info = {
    "name": "Ssamad Normal Simplifier",
    "blender": (3, 60, 1),
    "category": "Object",
}

import bpy
import mathutils
import math
import bmesh
from collections import deque
import random

    



class Normalpanel(bpy.types.Panel):
    bl_label = "Normal Edit"
    bl_idname = "PT_normalsedit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TestTab'
   
    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("object.corner_normal",icon='EMPTY_DATA',text="Corner normal data")
        row = layout.row()
        row.operator("object.select_unconnected_verts",icon='SNAP_MIDPOINT',text="Select Cornerless verts")
        row = layout.row()
        row.operator("object.corner_simplifier",icon='SNAP_VOLUME',text="Simplify corners")
        layout.prop(context.scene, "threshold_percentage")
        row = layout.row()
        row.operator("object.corner_clear",icon='CON_FOLLOWPATH',text="Clear corners")
class Cornerclear(bpy.types.Operator):
    bl_idname ="object.corner_clear"
    bl_label= "corner clear "
    
    def execute(self,context):
        
      
       bpy.ops.mesh.customdata_custom_splitnormals_clear()
       
           
        
class Cornersimplifier(bpy.types.Operator):
    bl_idname ="object.corner_simplifier"
    bl_label= "corner simplifer "
    bl_options = {'REGISTER', 'UNDO'}

    
    threshold_angle: bpy.props.FloatProperty(
        name="Threshold angle",
        default=0,
        min=0.0,
        max=180.0,
        step=500.0,) 
        
    change_origin: bpy.props.IntProperty(
        name="Change Origin",
        default=0,
        min=0,
        max=100000000
        )
    
        
    def execute(self, context):
            obj = context.active_object
            if obj and obj.type == 'MESH':
              
                processed_loops = []
                modified_loops=[]
                threshold_angle = self.threshold_angle
                origin=self.change_origin if self.change_origin<len(obj.data.vertices) else len(obj.data.vertices)-1
                
                obj.data.use_auto_smooth = True
                obj.data.calc_normals_split()
                loop_vert=vertex_loop(obj)
                tree=tree_order(obj,tree_order(obj,0)[origin])
                self.report({'INFO'},f"{tree}")
                tree= [i for i in tree if i not in cornorless_id(obj)]
                self.report({'INFO'},f"{tree}")
                
                
                
                custom_normals = [mathutils.Vector((-1, 0, 0)) for _ in range(len(obj.data.loops))]
                
                for vert in tree : 
                    adjacent_loops=[]
                    
                    adjacent_loops.extend(loop_vert[vert])
                   
                    for i in get_adjacent_vertices(obj,vert):
                        adjacent_loops.extend(loop_vert[i])
                   
                    for loopid in loop_vert[vert] :
                         if loopid not in modified_loops :
                             custom_normals[loopid]=obj.data.loops[loopid].normal
                
                
                         for adjloop in adjacent_loops:
                             if  adjloop!=loopid:
                                 difference = vector_difference(custom_normals[loopid], obj.data.loops[adjloop].normal)
                                 if adjloop in processed_loops:
                                     difference = vector_difference(custom_normals[loopid],custom_normals[adjloop])
                                 if difference <= threshold_angle:
                                    #self.report({'INFO'},f"{loopid,adjloop,difference}")
                                                    
                                    processed_loops.append(loopid)
                    
                                    modified_loops.append(adjloop)
                                    custom_normals[adjloop] = custom_normals[loopid] 
                                    #self.report({'INFO'},f"{custom_normals[adjloop],custom_normals[loopid]}")
                                    #self.report({'INFO'},f"{processed_loops,processed_verts}")
                                                
                                            
                         
                     
                obj.data.calc_normals_split()
                
                #custom_normals[loop_vert[tree[0]][0]]=(0,0,-1) 
                    
               
                obj.data.normals_split_custom_set(custom_normals)  
                #self.report({'INFO'},f"{custom_normals}")
                
        
                
                
                
                 
            return{'FINISHED'}



def vertex_loop(obj):
    vertex_loop= {}
    
    for loop in obj.data.loops:
        vertex_index = loop.vertex_index
        loop_index = loop.index

        if vertex_index not in vertex_loop:
            vertex_loop[vertex_index] = [loop_index]
        else:
            vertex_loop[vertex_index].append(loop_index)

    return vertex_loop


def tree_order(obj, vertex_id):
    visited = set()
    queue = deque([vertex_id])
    unique_adjacent_verts = []

    while queue:
        current_vertex = queue.popleft()
        if current_vertex not in visited:
            visited.add(current_vertex)
            unique_adjacent_verts.append(current_vertex)
            adjacent_verts = get_adjacent_vertices(obj, current_vertex)
            for vert in adjacent_verts:
                if vert not in visited:
                    queue.append(vert)

    return unique_adjacent_verts


def get_adjacent_vertices(obj, vertex_id):
    
    
    adjacent_vertices = []
    vertex = obj.data.vertices[vertex_id]
    
    for edge in obj.data.edges:
        if vertex.index in edge.vertices:
            adjacent_vertices.append(edge.vertices[0] if edge.vertices[1] == vertex.index else edge.vertices[1])
    
    return adjacent_vertices







class Cornernormals(bpy.types.Operator):
    bl_idname ="object.corner_normal"
    bl_label= "corner normal"
    def execute(self,context):
        obj=context.active_object
        if obj and obj.type == 'MESH':
            obj.update_from_editmode()
            obj.data.use_auto_smooth = True
            obj.data.calc_normals_split()
            obj.data.update()
            for loop in obj.data.loops:
                self.report({'INFO'},f"corner({loop.index}):{loop.normal}")
        return{'FINISHED'}

    
       
        

def vector_difference(v1, v2):
    vector_v1 = mathutils.Vector(v1)
    vector_v2 = mathutils.Vector(v2)
    angle_rad = vector_v1.angle(vector_v2)
    angle_deg = math.degrees(angle_rad)
    return round(abs((angle_deg)), 2)

class Select_unconnected_vertices(bpy.types.Operator):
    bl_idname="object.select_unconnected_verts"
    bl_label=" select unconnected verts"
    
    
    
    def execute(self,context):
        obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        for i in range(len(obj.data.polygons)):
            obj.data.polygons[i].select = True
            
            
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='INVERT')
       
          
      
        
        return {'FINISHED'}


def cornorless_id(obj):
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    for i in range(len(obj.data.polygons)):
        obj.data.polygons[i].select = True
            
            
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    selected_vertices=[]
        
    for vertex in obj.data.vertices:
        if vertex.select:
            selected_vertices.append(vertex.index)
    
    return selected_vertices
        
        

def register():
  
    bpy.utils.register_class(Normalpanel)
 
    bpy.utils.register_class(Cornernormals)
    bpy.utils.register_class(Cornersimplifier)
    bpy.utils.register_class(Cornerclear)
    bpy.utils.register_class(Select_unconnected_vertices)

def unregister():
    
    bpy.utils.unregister_class(Normalpanel)
  
    bpy.utils.unregister_class(Cornernormals)
    bpy.utils.unregister_class(Cornersimplifier)
    bpy.utils.unregister_class(Cornerclear)
    bpy.utils.unregister_class(Select_unconnected_vertices)
  

if __name__ == "__main__":
    register() 