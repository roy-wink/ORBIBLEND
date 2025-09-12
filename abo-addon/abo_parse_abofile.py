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

        # Start reading the .abo file
        try:
            frames = reader.read_abofile(self.filepath)

            # Clear any existing frames
            context.scene.abo_frames.clear()

            # Add frames to the collection
            for frame_data in frames:
                new_frame = context.scene.abo_frames.add()
                new_frame.index = frame_data["index"]
                new_frame.description = frame_data["description"]

                # Populate atoms
                new_frame.atoms.clear()
                for atom in frame_data["atoms"]:
                    atom_item = new_frame.atoms.add()
                    atom_item.index, atom_item.an, atom_item.x, atom_item.y, atom_item.z = atom

                # Populate models
                new_frame.models.clear()
                for model_data in frame_data["models"]:
                    model_item = new_frame.models.add()
                    model_item.index = model_data["index"]
                    model_item.color = model_data["color"]

                    # Populate faces
                    model_item.faces.clear()
                    for face in model_data["faces"]:
                        face_item = model_item.faces.add()
                        face_item.f1, face_item.f2, face_item.f3 = face

                    # Populate vertices
                    model_item.vertices.clear()
                    for vertex in model_data["vertices"]:
                        vertex_item = model_item.vertices.add()
                        vertex_item.v1, vertex_item.v2, vertex_item.v3 = vertex

                    # Populate normals
                    model_item.normals.clear()
                    for normal in model_data["normals"]:
                        normal_item = model_item.normals.add()
                        normal_item.n1, normal_item.n2, normal_item.n3 = normal

            self.report({"INFO"}, f"Successfully imported {len(frames)} frames from {os.path.basename(self.filepath)}")

            for frame in context.scene.abo_frames:
                print(f"Frame {frame.index}: {frame.description}")

        except Exception as e:
            self.report({"ERROR"}, f"Failed to read .abo file: \n{e}")
            return {"CANCELLED"}
        