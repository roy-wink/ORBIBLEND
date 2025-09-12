import bpy

class CreateOrbitals:
    @staticmethod
    def create_orbitals(self, active_frame, orbitals_collection):
        from .abo_create_mesh import CreateMeshObject

        # Create the orbitals collection if not present
        if not orbitals_collection:
            orbitals_collection = bpy.data.collections.new("Orbitals")
            bpy.context.scene.collection.children.link(orbitals_collection)

        # Delete all existing orbital materials
        for material in bpy.data.materials:
            if material.name.startswith("orbital"):
                bpy.data.materials.remove(material)

        # Create mesh objects for each model
        generated_objects = []
        for model in active_frame.models:
            vertices = [(v.v1, v.v2, v.v3) for v in model.vertices]
            faces = [(f.f1, f.f2, f.f3) for f in model.faces]
            normals = [(n.n1, n.n2, n.n3) for n in model.normals]

            try:
                # Create the mesh
                obj = CreateMeshObject.create_mesh_object(f"orbital_model_{model.index}", vertices, faces, normals)

                # Create or retrieve material for the color
                color = model.color
                material_name = f"orbital_material_{model.index}"
                material = bpy.data.materials.get(material_name)
                if not material:
                    material = bpy.data.materials.new(name=material_name)
                    material.use_nodes = True

                    # Get the material's node tree
                    node_tree = material.node_tree
                    nodes = node_tree.nodes
                    links = node_tree.links

                    # Clear existing nodes
                    for node in nodes:
                        nodes.remove(node)

                    # Create a new Principled BSDF node
                    bsdf_node = nodes.new(type="ShaderNodeBsdfPrincipled")
                    bsdf_node.location = (0, 0)
                    bsdf_node.inputs["Base Color"].default_value = (*color[:3], 1.0)  # Set color
                    bsdf_node.inputs["Alpha"].default_value = color[3]  # Set alpha

                    # Create a Material Output node
                    output_node = nodes.new(type="ShaderNodeOutputMaterial")
                    output_node.location = (200, 0)

                    # Connect the BSDF node to the Material Output node
                    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

                # Assign material to the object
                if obj.data.materials:
                    obj.data.materials[0] = material
                else:
                    obj.data.materials.append(material)

                # Link the object to the 'Orbitals' collection
                orbitals_collection.objects.link(obj)

                # Unlink the object from the Scene Collection (default collection)
                for collection in obj.users_collection:
                    if collection != orbitals_collection:
                        collection.objects.unlink(obj)

                generated_objects.append(obj)
                self.report({'INFO'}, f"Mesh created for model {model.index}")

            except Exception as e:
                self.report({'WARNING'}, f"Error creating mesh for model {model.index}: {e}")
                continue

        # Rename models if there are exactly two
        if len(generated_objects) == 2:
            generated_objects[0].name = "Positive lobe"
            generated_objects[1].name = "Negative lobe"
        if len(generated_objects) == 1:
            generated_objects[0].name = "Single lobe"
