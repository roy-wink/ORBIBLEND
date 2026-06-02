import bpy

class AboImport():
    @staticmethod
    def import_abofile(self, context):
        import os
        from .py_abo_reader import PyAboReader
        reader = PyAboReader()

        # Empty orbitals, molecule and bonds collection if filled
        orbitals_collection = bpy.data.collections.get("Orbitals")
        molecule_collection = bpy.data.collections.get("Molecule")
        bonds_collection = bpy.data.collections.get("Bonds")
        for collection in [orbitals_collection, molecule_collection, bonds_collection]:
            if collection:
                for obj in list(collection.objects):
                    collection.objects.unlink(obj)
                    bpy.data.objects.remove(obj)

        for material in list(bpy.data.materials):
            if material.name.startswith(("molecule_material_", "orbital_material_", "bonds_material")):
                bpy.data.materials.remove(material)

        # Start reading lightweight metadata from the .abo file. Dense mesh arrays
        # are loaded on demand when a frame is rendered into Blender meshes.
        try:
            frames = reader.read_abofile_metadata(self.filepath)

            # Clear any existing frames
            context.scene.abo_frames.clear()
            context.scene.abo_filepath = self.filepath
            context.scene.abo_meshes_created = False
            context.scene.abo_color_editing = False
            context.scene.abo_color_entries.clear()

            # Add only frame metadata to the scene.
            for frame_data in frames:
                new_frame = context.scene.abo_frames.add()
                new_frame.index = frame_data["index"]
                new_frame.description = frame_data["description"]
                new_frame.atom_count = frame_data["atom_count"]
                new_frame.model_count = frame_data["model_count"]
                new_frame.vertex_count = frame_data["vertex_count"]
                new_frame.face_count = frame_data["face_count"]

            self.report({"INFO"}, f"Successfully imported {len(frames)} frames from {os.path.basename(self.filepath)}")

            for frame in context.scene.abo_frames:
                print(f"Frame {frame.index}: {frame.description}")

        except Exception as e:
            self.report({"ERROR"}, f"Failed to read .abo file: \n{e}")
            return {"CANCELLED"}
        
