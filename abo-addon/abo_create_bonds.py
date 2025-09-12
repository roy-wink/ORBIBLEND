import bpy

# Note:
# This class completely work in Angstrom

class CreateBonds:
    @staticmethod
    def get_distance(coor_1, coor_2):
        import math

        x_a, y_a, z_a = coor_1
        x_b, y_b, z_b = coor_2

        return math.sqrt((x_b - x_a) ** 2 + (y_b - y_a) ** 2 + (z_b - z_a) ** 2)


    @staticmethod
    def do_draw_bond(element_1, element_2, distance, unit):
        """Determine if a bond must be drawn between two elements"""
        
        # Sort elements from low to high
        elements = (min(element_1, element_2), max(element_1, element_2))

        # Define everything in Angstrom
        if unit == 'BOHR':
            distance = distance / 1.88372

        # Bonds with hydrogen
        if elements[0] == 1:
            if elements[1] <= 20:
                max_distance = 1.2
            else:
                max_distance = 2.0
                
        # Both elements within He - Ca
        elif elements[0] <= 20 and elements[1] <= 20:
            max_distance = 2.0
        
        # Any element Sc+
        else:
            max_distance = 2.5

        # return True if a bond must be drawn
        return distance <= max_distance


    @staticmethod
    def create_cylinder(atom_1, atom_2, length, radius):
        import math

        coor_1 = (atom_1.x, atom_1.y, atom_1.z)
        coor_2 = (atom_2.x, atom_2.y, atom_2.z)

        # Calculate midpoint of cylinder
        midpoint = (
            (coor_1[0] + coor_2[0]) / 2,
            (coor_1[1] + coor_2[1]) / 2,
            (coor_1[2] + coor_2[2]) / 2,
        )

        # Calculate the vector between the two atoms
        direction = (
            coor_2[0] - coor_1[0],
            coor_2[1] - coor_1[1],
            coor_2[2] - coor_1[2]
        )

        # Calculate the rotation
        x, y, z, = direction
        xy_length = math.sqrt(x ** 2 + y ** 2)
        rot_y = math.atan2(xy_length, z)
        rot_z = math.atan2(y, x)

        # Create the cylinder
        cylinder_name = f"bond_{atom_1.index}_{atom_2.index}"
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radius,
            depth=length,
            location=midpoint
        )
        cylinder = bpy.data.objects.get("Cylinder")
        cylinder.name = cylinder_name
        cylinder.rotation_euler = (0, rot_y, rot_z)

        # Light grey
        color = (0.31, 0.31, 0.31, 1.0)

        # Check if material exists, else make new material        
        material_name = "bonds_material"
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
            bsdf_node.inputs["Base Color"].default_value = color  # Set color

            # Create a Material Output node
            output_node = nodes.new(type="ShaderNodeOutputMaterial")
            output_node.location = (200, 0)

            # Connect the BSDF node to the Material Output node
            links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

        # Assign material to the object
        if cylinder.data.materials:
            cylinder.data.materials[0] = material
        else:
            cylinder.data.materials.append(material)

        return cylinder


    @staticmethod
    def create_bonds(self, context, active_frame):
        # Get or create Bonds collecton
        bonds_collection = bpy.data.collections.get("Bonds")
        if bonds_collection:
            for obj in list(bonds_collection.objects):
                bonds_collection.objects.unlink(obj)
                bpy.data.objects.remove(obj)
        else:
            bonds_collection = bpy.data.collections.new("Bonds")
            bpy.context.scene.collection.children.link(bonds_collection)

        radius = 0.1
        unit = context.scene.abo_unit_selection
        if unit == 'BOHR':
            radius = radius * 1.88372

        from itertools import combinations
        atoms = active_frame.atoms
        atom_combinations = combinations(range(len(atoms)), 2)
        for combination in atom_combinations:
            atom_1 = atoms[combination[0]]
            element_1 = atom_1.an
            coor_1 = (atom_1.x, atom_1.y, atom_1.z)

            atom_2 = atoms[combination[1]]
            element_2 = atom_2.an
            coor_2 = (atom_2.x, atom_2.y, atom_2.z)

            distance = self.get_distance(coor_1, coor_2)
            if self.do_draw_bond(element_1, element_2, distance, unit):
                cylinder = self.create_cylinder(atom_1, atom_2, distance, radius)

                # Link the bond to the 'Bonds' collection
                bonds_collection.objects.link(cylinder)

                # Unlink the cylinder from the Scene Collection (default collection)
                for collection in cylinder.users_collection:
                    if collection != bonds_collection:
                        collection.objects.unlink(cylinder)
