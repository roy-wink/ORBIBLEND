import bpy

class CreateMeshObject():
    @staticmethod
    def create_mesh_object(name, vertices, faces, normals=None):
        """Create a mesh object from vertices, faces, and optional normals"""
        
        # Create a new mesh and object
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        
        # Link the object to the current scene
        bpy.context.collection.objects.link(obj)
        
        try:
            # Populate the mesh with vertices and faces
            mesh.from_pydata(vertices, [], faces)
            
            # If normals are provided, set them
            if normals:   
                # Update the mesh normals
                mesh.normals_split_custom_set_from_vertices(normals)
                # mesh.use_auto_smooth = True  
            
            # Update the mesh to apply the changes
            mesh.update()
        
        except Exception as e:
            raise RuntimeError(f"Failed to create mesh '{name}': {e}")
        
        return obj
