class PyAboReader:
    @staticmethod
    def _read_atoms(file_handle, count):
        import struct

        atoms = []
        for atom_index in range(count):
            atomic_number = struct.unpack("<b", file_handle.read(1))[0]
            atom_x = struct.unpack("<f", file_handle.read(4))[0]
            atom_y = struct.unpack("<f", file_handle.read(4))[0]
            atom_z = struct.unpack("<f", file_handle.read(4))[0]
            atoms.append((atom_index, atomic_number, atom_x, atom_y, atom_z))
        return atoms

    @staticmethod
    def _read_model(file_handle, include_mesh):
        import struct

        model_index = struct.unpack("<h", file_handle.read(2))[0]
        color = (
            struct.unpack("<f", file_handle.read(4))[0],
            struct.unpack("<f", file_handle.read(4))[0],
            struct.unpack("<f", file_handle.read(4))[0],
            struct.unpack("<f", file_handle.read(4))[0],
        )

        vertices = []
        normals = []
        num_vertices = struct.unpack("<I", file_handle.read(4))[0]
        if include_mesh:
            for _ in range(num_vertices):
                vertex = (
                    struct.unpack("<f", file_handle.read(4))[0],
                    struct.unpack("<f", file_handle.read(4))[0],
                    struct.unpack("<f", file_handle.read(4))[0],
                )
                normal = (
                    struct.unpack("<f", file_handle.read(4))[0],
                    struct.unpack("<f", file_handle.read(4))[0],
                    struct.unpack("<f", file_handle.read(4))[0],
                )
                vertices.append(vertex)
                normals.append(normal)
        else:
            file_handle.seek(num_vertices * 24, 1)

        faces = []
        num_faces = struct.unpack("<I", file_handle.read(4))[0]
        if include_mesh:
            for _ in range(num_faces):
                faces.append(
                    (
                        struct.unpack("<I", file_handle.read(4))[0],
                        struct.unpack("<I", file_handle.read(4))[0],
                        struct.unpack("<I", file_handle.read(4))[0],
                    )
                )
        else:
            file_handle.seek(num_faces * 12, 1)

        model = {
            "index": model_index,
            "color": color,
            "vertex_count": num_vertices,
            "face_count": num_faces,
        }
        if include_mesh:
            model["vertices"] = vertices
            model["normals"] = normals
            model["faces"] = faces
        return model

    def _read_frame(self, file_handle, include_mesh):
        import struct

        frame_index = struct.unpack("<h", file_handle.read(2))[0]
        description_length = struct.unpack("<h", file_handle.read(2))[0]
        description = file_handle.read(description_length).decode("utf-8")

        num_atoms = struct.unpack("<h", file_handle.read(2))[0]
        atoms = self._read_atoms(file_handle, num_atoms)

        models = []
        num_models = struct.unpack("<h", file_handle.read(2))[0]
        for _ in range(num_models):
            models.append(self._read_model(file_handle, include_mesh))

        return {
            "index": frame_index,
            "description": description,
            "atoms": atoms,
            "models": models,
            "atom_count": len(atoms),
            "model_count": len(models),
            "vertex_count": sum(model["vertex_count"] for model in models),
            "face_count": sum(model["face_count"] for model in models),
        }

    def _read_frames(self, filename, include_mesh, target_position=None):
        import struct

        if not filename.endswith(".abo"):
            raise ValueError(f"Expected a .abo file, got {filename}")

        with open(filename, "rb") as file_handle:
            frames = []
            num_frames = struct.unpack("<h", file_handle.read(2))[0]
            for frame_position in range(num_frames):
                frame = self._read_frame(file_handle, include_mesh=(include_mesh and frame_position == target_position if target_position is not None else include_mesh))
                if target_position is None:
                    frames.append(frame)
                elif frame_position == target_position:
                    return frame

        if target_position is not None:
            raise IndexError(f"Frame position {target_position} is outside {filename}")
        return frames

    def read_abofile(self, filename):
        return self._read_frames(filename, include_mesh=True)

    def read_abofile_metadata(self, filename):
        return self._read_frames(filename, include_mesh=False)

    def read_frame(self, filename, frame_position):
        return self._read_frames(filename, include_mesh=True, target_position=frame_position)
