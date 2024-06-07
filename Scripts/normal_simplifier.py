bl_info = {
    "name": "Ssamad Normal Simplifier",
    "blender": (3, 60, 1),
    "category": "Object",
}

import bpy
import mathutils
import math


class Vertexlocation(bpy.types.Operator):
    bl_idname ="object.v_location"
    bl_label= "vertex location"
    
    def execute(self,context):
        obj=context.object
        if obj and obj.type== 'MESH':
            obj.update_from_editmode()
            selected_v = [v for v in obj.data.vertices if v.select]
            if selected_v :
                for vertex in selected_v:
                    self.report({'INFO'} ,f"Vertex({vertex.index})  Location :{vertex.co}") 
            else :
                self.report({'INFO'},"Select a mesh's vertices") 
        else :
            self.report({'INFO'},"Select a mesh's vertices")   

        return {'FINISHED'} 

    



class Normalpanel(bpy.types.Panel):
    bl_label = "Normal Edit"
    bl_idname = "PT_normalsedit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Ss Normals'
   
    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("object.corner_normal",icon='EMPTY_DATA',text="Corner normal data")
        row = layout.row()
        row.operator("object.corner_simplifier",icon='SNAP_VOLUME',text="Simplify corners")
        layout.prop(context.scene, "threshold_percentage")
        row = layout.row()
        row.operator("object.corner_clear",icon='CON_FOLLOWPATH',text="Clear corners")
class Cornerclear(bpy.types.Operator):
    bl_idname ="object.corner_clear"
    bl_label= "corner clear "
    
    def execute(self,context):
        
       bpy.ops.mesh.set_normals_from_faces()
           
        
class Cornersimplifier(bpy.types.Operator):
    bl_idname ="object.corner_simplifier"
    bl_label= "corner simplifer "
    bl_options = {'REGISTER', 'UNDO'}

    
    threshold_angle: bpy.props.FloatProperty(
        name="Threshold angle",
        default=12.0,
        min=0.0,
        max=180.0,
        step=500.0,)
        
    simplification_magnitude: bpy.props.FloatProperty(
        name="Simplification magnitude",
        default=.01,
        min=0.0,
        max=1.0,
        step=.001,)
        
    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            processed_vertices = []
            threshold_angle = self.threshold_angle
            obj.data.use_auto_smooth = True
            obj.data.calc_normals_split()
            
            custom_normals = [mathutils.Vector((-1, -1, -1)) for _ in range(len(obj.data.loops))]
            for i in range(len(obj.data.loops)):
                if i not in processed_vertices:
                    custom_normals[i] = obj.data.loops[i].normal
                
                    for j in range(len(obj.data.loops)):
                        difference = vector_difference(custom_normals[i], obj.data.loops[j].normal)
                        self.report({'INFO'},f"corner({difference}")
                        
                        if difference <= threshold_angle:
                            processed_vertices.append(j)
                            custom_normals[j] = custom_normals[i]
            
           
            
           
            
        
            
            obj.data.calc_normals_split()
            obj.data.normals_split_custom_set(custom_normals)  
            
    
            
            
            
             
        return{'FINISHED'}

        

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



def register():
  
    bpy.utils.register_class(Normalpanel)
    bpy.utils.register_class(Cornernormals)
    bpy.utils.register_class(Cornersimplifier)
    bpy.utils.register_class(Cornerclear)

def unregister():
    
    bpy.utils.unregister_class(Normalpanel)
    bpy.utils.unregister_class(Cornernormals)
    bpy.utils.unregister_class(Cornersimplifier)
    bpy.utils.unregister_class(Cornerclear)
  

if __name__ == "__main__":
    register() 

 