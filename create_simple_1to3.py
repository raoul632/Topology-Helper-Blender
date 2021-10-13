import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy import data as D, context as C
import bmesh
from code import InteractiveConsole


#snipet pour créé un fake breakpoint, create fake break point usefull for debug 
def debug():
    import code
    namespace = globals().copy()
    namespace.update(locals())
    code.interact(local=namespace) 
    
    

#THREETOONE_OT <-- class naming convention
#F3 -> mesh -> threetoone
class THREETOONE_OT_add_object(Operator):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_threetoone"
    bl_label = "Add Mesh ThreeeToOne"
    bl_options = {'REGISTER', 'UNDO'}
    
    def createMaterial(self):
        #on créé les material, create material
        mat_green = None
        mat_gray = None
        mat_red = None
        
        lst_materials_name = []
        for i in D.materials:
           lst_materials_name.append(i.name)
        
        if("green_topo_helper" in lst_materials_name):
            mat_green = D.materials["green_topo_helper"]  
        else:
            mat_green = D.materials.new("green_topo_helper")
            mat_green.diffuse_color = (0.0,0.8,0.0,1.0)
        if("gray_topo_helper" in lst_materials_name):
            mat_gray = D.materials["gray_topo_helper"]   
        else:
            mat_gray = D.materials.new("gray_topo_helper")
            mat_gray.diffuse_color = (0.8,0.8,0.8,1.0)
            
        if("red_topo_helper" in lst_materials_name):    
            mat_red = D.materials["red_topo_helper"]
        else: 
            mat_red = D.materials.new("red_topo_helper")
            mat_red.diffuse_color = (0.8,0.0,0.0,1.0)
            
        lst_mat = [mat_green, mat_gray, mat_red]
        #return a material list
        return lst_mat
    
    def createThreeFaceToOne(self):
        verts = [
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (1.0, 1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.25,0.60,0.0),
            (0.75,0.60,0.0),
            (0.25,0.0,0.0),
            (0.75,0.0,0.0)]

        # chaque face est un tuple qui contiens les indices 
        #qui pointe sur le tableau ci dessus
        faces=[(0,1,4,6), (1,4,5,2),(4,5,7,6),(2,5,7,3)]

        # idem sauf qu'ici on définie les edge ou les bords
        #donc 2 point 
        
        edges = []


        # on créé le mesh avec les données definie ci-dessus
        mesh_name = "1To3_Sample"
        mesh_data = D.meshes.new(mesh_name)
        mesh_data.from_pydata(verts, edges, faces)

        # Returns True if any invalid geometry was removed.
        corrections = mesh_data.validate(
          verbose=True,
          clean_customdata=True)

        # Load BMesh with mesh data.
        bm = bmesh.new()
        bm.from_mesh(mesh_data)
        bm.to_mesh(mesh_data)
        bm.free()
        
        mesh_obj = D.objects.new(mesh_data.name, mesh_data)
        C.collection.objects.link(mesh_obj)
        return mesh_obj


    def execute(self, context):

        lst_mat = self.createMaterial()
        #create mesh 
        mesh_obj = self.createThreeFaceToOne()
        
        #add material to our mesh object 
        mesh_obj.data.materials.append(lst_mat[0])
        mesh_obj.data.materials.append(lst_mat[1])
        mesh_obj.data.materials.append(lst_mat[2])   

        #set our target object to active
        C.view_layer.objects.active = mesh_obj
       
        mesh_obj.data.polygons[0].material_index = 1
        mesh_obj.data.polygons[3].material_index = 1
        mesh_obj.data.polygons[1].material_index = 3
        mesh_obj.data.polygons[2].material_index = 0

        return {'FINISHED'}


def register():
    bpy.utils.register_class(THREETOONE_OT_add_object)



def unregister():
    bpy.utils.unregister_class(THREETOONE_OT_add_object)


if __name__ == "__main__":
    register()
