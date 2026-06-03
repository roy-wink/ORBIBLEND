import bpy

class CreateMolecule:
    @staticmethod
    def _ang2bohr():
        return 1.88972


    @staticmethod
    def srgb_to_linearrgb(col):
        # ensure no gamma correction in the color
        # answer of Stephan Ahlf in:
        # https://blender.stackexchange.com/questions/153094/blender-2-8-python-how-to-set-material-color-using-hex-value-instead-of-rgb
        if   col < 0:
            return 0
        elif col < 0.04045:
            return col / 12.92
        else:
            return ((col + 0.055) / 1.055) ** 2.4


    @staticmethod
    def hex_to_rgba(self, hex_value):
        hex_color = hex_value[1:]

        red = int(hex_color[:2], base=16)
        s_red = red / 255.0
        lin_red = self.srgb_to_linearrgb(s_red)

        green = int(hex_color[2:4], base=16)
        s_green = green / 255.0
        lin_green = self.srgb_to_linearrgb(s_green)

        blue = int(hex_color[4:6], base=16)
        s_blue = blue / 255.0
        lin_blue = self.srgb_to_linearrgb(s_blue)

        return (lin_red, lin_green, lin_blue, 1.0)


    @staticmethod
    def create_molecule(self, context, active_frame, molecule_collection):
        # Create molecule collection if not present
        if not molecule_collection:
            molecule_collection = bpy.data.collections.new("Molecule")
            bpy.context.scene.collection.children.link(molecule_collection)
            present_molecule = []
        else:
            present_molecule = [tuple(obj.location) for obj in list(molecule_collection.objects)]
            present_molecule.sort()

        # check the bool if the viewport has been altered. If so, remove everything.

        # Compare molecules in collection - if equal to request, return finished
        new_molecule = [(atom[2], atom[3], atom[4]) for atom in active_frame["atoms"]]
        new_molecule.sort()

        if new_molecule == present_molecule and \
            context.scene.abo_previous_unit == context.scene.abo_unit_selection:
                # The molecule and the unit have not changed
            print('skipping molecule')
            return None

        # If not, clear all existing objects
        for obj in list(molecule_collection.objects):
            molecule_collection.objects.unlink(obj)
            bpy.data.objects.remove(obj)

        # Import atom data
        import os
        import json

        addon_directory = os.path.dirname(__file__)
        atom_info_path = os.path.join(addon_directory, "atom_info.json")
        with open(atom_info_path, "r") as file:
            atom_info = json.load(file)["atom"]

        generated_objects = []
        for atom in active_frame["atoms"]:
            sphere_segments = 256

            atom_index, atomic_number, atom_x, atom_y, atom_z = atom

            # Receive color and radius
            element = atom_info["element"][str(atomic_number)]
            atom_radius = float(atom_info["radius"][element])
            atom_color = self.hex_to_rgba(self, atom_info["color"][element])

            if context.scene.abo_unit_selection == 'BOHR':
                # Convert Angstrom to Bohr
                atom_radius = atom_radius * self._ang2bohr()

            # Add sphere
            bpy.ops.mesh.primitive_uv_sphere_add(
                segments=sphere_segments,
                ring_count=int(sphere_segments/4),
                radius=atom_radius,
                location=(atom_x, atom_y, atom_z),
                align="WORLD"
            )

            obj = bpy.context.object
            obj.name = f"molecule_atom_{atom_index}_{element}"

            # Check if material exists, else make new material
            material_name = f"molecule_material_{atomic_number}"
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
                bsdf_node.inputs["Base Color"].default_value = atom_color  # Set color

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

            # Link the atom to the 'Molecule' collection
            molecule_collection.objects.link(obj)

            # Unlink the object from the Scene Collection (default collection)
            for collection in obj.users_collection:
                if collection != molecule_collection:
                    collection.objects.unlink(obj)

            generated_objects.append(obj)

        # Start building bonds
        from .abo_create_bonds import CreateBonds
        bond_maker = CreateBonds()
        bond_maker.create_bonds(bond_maker, context, active_frame)

        # Set the unit in storage
        context.scene.abo_previous_unit = context.scene.abo_unit_selection
