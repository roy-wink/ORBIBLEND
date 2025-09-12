class PyAboReader():
    def read_abofile(self, filename):
        try:
            import struct
        except ModuleNotFoundError():
            raise ModuleNotFoundError('struct module not installed')
    
        if not filename.endswith('.abo'):
            return -1
    
        with open(filename, 'rb') as f:
            frames = []
            num_frames = struct.unpack('<h', f.read(2))[0]
            for frm in range(num_frames):
                frame_index = struct.unpack('<h', f.read(2))[0]
                description_length = struct.unpack('<h', f.read(2))[0]
                description = f.read(description_length).decode("utf-8")
    
                atoms = []
                num_atoms = struct.unpack('<h', f.read(2))[0]
                for atom in range(num_atoms):
                    atomic_number = struct.unpack('<b', f.read(1))[0]
                    atom_x = struct.unpack('<f', f.read(4))[0]
                    atom_y = struct.unpack('<f', f.read(4))[0]
                    atom_z = struct.unpack('<f', f.read(4))[0]
                    atoms.append((atom, atomic_number, atom_x, atom_y, atom_z))
    
                models = []
                num_models = struct.unpack('<h', f.read(2))[0]
                for model in range(num_models):
                    model_index = struct.unpack('<h', f.read(2))[0]
                    color_r = struct.unpack('<f', f.read(4))[0]
                    color_g = struct.unpack('<f', f.read(4))[0]
                    color_b = struct.unpack('<f', f.read(4))[0]
                    color_a = struct.unpack('<f', f.read(4))[0]
                    this_color = (color_r, color_g, color_b, color_a)
    
                    normals = []
                    vertices = []
                    num_vertices = struct.unpack('<I', f.read(4))[0]
                    for vert in range(num_vertices):
                        vert_1 = struct.unpack('<f', f.read(4))[0]
                        vert_2 = struct.unpack('<f', f.read(4))[0]
                        vert_3 = struct.unpack('<f', f.read(4))[0]
                        vertices.append((vert_1, vert_2, vert_3))
    
                        norm_1 = struct.unpack('<f', f.read(4))[0]
                        norm_2 = struct.unpack('<f', f.read(4))[0]
                        norm_3 = struct.unpack('<f', f.read(4))[0]
                        normals.append((norm_1, norm_2, norm_3))
    
                    faces = []
                    num_faces = struct.unpack('<I', f.read(4))[0]
                    for face in range(num_faces):
                        index_1 = struct.unpack('<I', f.read(4))[0]
                        index_2 = struct.unpack('<I', f.read(4))[0]
                        index_3 = struct.unpack('<I', f.read(4))[0]
                        faces.append((index_1, index_2, index_3))
    
                    this_model = {
                        'index':        model_index,
                        'color':        this_color,
                        'vertices':     vertices,
                        'normals':      normals,
                        'faces':        faces
                                 }
                    models.append(this_model)
    
                this_frame = {
                        'index':        frame_index,
                        'description':  description,
                        'atoms':        atoms,
                        'models':       models
                               }
                frames.append(this_frame)
    
        return frames
