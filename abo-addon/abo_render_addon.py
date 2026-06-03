import bpy

class ABO_PT_Initialize_workspace(bpy.types.Panel):
    """ Panel for preparing the workspace """
    bl_label = "Prepare workspace"
    bl_idname = "ABO_PT_Initialize_workspace"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ABO"

    def draw(self, context):
        layout = self.layout
        # scene = context.scene

        # Button for deleting everything on screen
        row = layout.row()
        row.label(text="Clear the workspace", icon="WORKSPACE")
        row = layout.row()
        row.operator("abo.delete_elements")

        # Button for seting up the camera/view/render settings
        row = layout.row()
        row.label(text="Set up camera settings", icon="CAMERA_DATA")
        row = layout.row()
        row.operator("abo.camera_setup")


class ABO_OT_Delete_elements(bpy.types.Operator):
    """ Class for deleting all unnecessairy elements """
    bl_label = "Delete unnecessairy elements"
    bl_idname = "abo.delete_elements"

    def execute(self, context):
        # Select everything
        bpy.ops.object.select_all(action="SELECT")

        # Deselect important objects if present
        for obj in ["Camera", "CameraPath", "SunLight", "LightCurve"]:
            if bpy.data.objects.get(obj) is not None:
                bpy.data.objects[obj].select_set(False)

        # Delete selected objects
        bpy.ops.object.delete()

        return {"FINISHED"}


class ABO_OT_Camera_setup(bpy.types.Operator):
    """ Class for the camera set-up """
    bl_label = "Camera set-up"
    bl_idname = "abo.camera_setup"

    def execute(self, context):
        scene = context.scene
        
        # Ensure the camera exists
        cam = bpy.data.objects.get("Camera")
        if not cam:
            bpy.ops.object.camera_add()
            cam = bpy.context.object

        # Set the camera on a specific location and rotation
        cam_distance = 15
        cam.location = (0, -cam_distance, 0)
        cam.rotation_euler = (1.5708, 0, 0)
        cam.data.clip_end = 1000

        # Set up EEVEE render settings
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
        Eevee = scene.eevee
        Eevee.volumetric_end = 1000
        Eevee.volumetric_tile_size = "2"
        Eevee.taa_render_samples = 512
        Eevee.use_volumetric_shadows = True
        Eevee.volumetric_shadow_samples = 64

        # Ensure transparent film, default animation format, and resolution
        scene.render.film_transparent = True
        scene.render.image_settings.file_format = "FFMPEG"
        scene.render.image_settings.color_mode = "RGB"
        scene.render.resolution_x = 2048
        scene.render.resolution_y = 2048        

        # Check if CameraPath already exists, and delete it
        camera_path = bpy.data.objects.get("CameraPath")
        if camera_path:
            bpy.data.objects.remove(camera_path)

        # Create a new CameraPath (circle) and link the camera
        bpy.ops.curve.primitive_bezier_circle_add(
            radius=cam_distance,
            enter_editmode=False,
            align="WORLD",
            location=(0, 0, 0)
        )
        camera_path = bpy.context.object
        camera_path.name = "CameraPath"
        camera_path.data.use_path = True
        camera_path.data.path_duration = 360

        # Link the camera to the CameraPath
        camera_path.select_set(True)
        cam.select_set(True)
        bpy.ops.object.parent_set(type="FOLLOW")

        # Remove possible existing light source
        light = bpy.data.objects.get("SunLight")
        if light:
            bpy.data.objects.remove(light)

        # Create a new sun light and set its properties
        bpy.ops.object.light_add(
            type='SUN',
            align='WORLD',
            location=(0, -0.8 * cam_distance, 7.5),
            rotation=(1.2217, 0, 0)
        )
        light = bpy.context.object
        light.name = "SunLight"
        light.data.energy = 4.0
        light.data.angle = 0.2618

        # Check if LightCurve already exists, and delete it
        light_curve = bpy.data.objects.get("LightCurve")
        if light_curve:
            bpy.data.objects.remove(light_curve)

        # Create a new LightCurve (circle) and link the light
        bpy.ops.curve.primitive_bezier_circle_add(
            radius=cam_distance,
            enter_editmode=False,
            align="WORLD",
            location=(0, 0, 0)
        )
        light_curve = bpy.context.object
        light_curve.name = "LightCurve"
        light_curve.data.use_path = True
        light_curve.data.path_duration = 360

        # Link the light to the LightCurve
        light_curve.select_set(True)
        light.select_set(True)
        bpy.ops.object.parent_set(type="FOLLOW")

        # Set animation length
        scene.frame_start = 1
        scene.frame_end = 360

        # Get or create Render tools collection
        render_tools_collection = bpy.data.collections.get("Render tools")
        if not render_tools_collection:
            render_tools_collection = bpy.data.collections.new("Render tools")
            scene.collection.children.link(render_tools_collection)

        # Link Camera, CameraPath, SunLight, and LightCurve to Render tools collection
        for obj in [cam, camera_path, light, light_curve]:
            if obj.name not in render_tools_collection.objects:
                render_tools_collection.objects.link(obj)

        # Unlink objects from other collections
        for obj in [cam, camera_path, light, light_curve]:
            for collection in obj.users_collection:
                if collection != render_tools_collection:
                    collection.objects.unlink(obj)

        # Switch to camera view
        if hasattr(context.space_data, "region_3d"):
            context.space_data.region_3d.view_perspective = "CAMERA"

        # Deselect objects to avoid unnecessary selection (scary orange line)
        bpy.ops.object.select_all(action="DESELECT")

        # Jump to the first frame
        bpy.ops.screen.frame_jump(end=False)

        return {"FINISHED"}


class ABO_PT_Import_abofile(bpy.types.Panel):
    """ Panel for importing the abo file """
    bl_label = "Import .abo file"
    bl_idname = "ABO_PT_Import_abofile"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ABO"

    def draw(self, context):
        layout = self.layout
        # scene = context.scene

        # Button for importing .abo file
        row = layout.row()
        row.label(text="Import molecule and orbitals", icon="FILE_NEW")
        row = layout.row()
        row.operator("abo.import_abofile")


class ABO_OT_Import_abofile(bpy.types.Operator):
    """ Class for importing .abo file """
    bl_label = "Import .abo file"
    bl_idname = "abo.import_abofile"

    # Import file constraints
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(
        default="*.abo",
        options={"HIDDEN"},
    )

    def invoke(self, context, event):
        # Import file selector
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        # Actually import .abo file and populate models
        from .abo_parse_abofile import AboImport
        AboImport.import_abofile(self, context)
        
        # Select first frame
        scene = context.scene
        scene.abo_active_frame_index = 0

        return {"FINISHED"}


class ABO_Atom(bpy.types.PropertyGroup):
    """Represents an atom"""
    index: bpy.props.IntProperty(name="Atom index")
    an: bpy.props.IntProperty(name="Atomic number")
    x: bpy.props.FloatProperty(name="X")
    y: bpy.props.FloatProperty(name="Y")
    z: bpy.props.FloatProperty(name="Z")


class ABO_Model(bpy.types.PropertyGroup):
    """Represents lightweight model metadata."""
    index: bpy.props.IntProperty(name="Model index")
    color: bpy.props.FloatVectorProperty(name="Color", size=4, subtype='COLOR', min=0.0, max=1.0)
    vertex_count: bpy.props.IntProperty(name="Vertex count")
    face_count: bpy.props.IntProperty(name="Face count")


class ABO_Frame_property(bpy.types.PropertyGroup):
    """Represents lightweight frame metadata."""
    index: bpy.props.IntProperty(name="Frame index")
    description: bpy.props.StringProperty(name="Description")
    atom_count: bpy.props.IntProperty(name="Atom count")
    model_count: bpy.props.IntProperty(name="Model count")
    vertex_count: bpy.props.IntProperty(name="Vertex count")
    face_count: bpy.props.IntProperty(name="Face count")


class ABO_PT_Frames(bpy.types.Panel):
    """ Panel to display imported frames """
    bl_label = ".abo frames"
    bl_idname = "ABO_PT_Frames"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ABO"

    @classmethod
    def poll(cls, context):
        return hasattr(context.scene, "abo_frames") and len(context.scene.abo_frames) > 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Display the custom UIList
        row = layout.row()
        row.template_list(
            "ABO_UL_Frames",  # Use the custom UIList class
            "abo_frames",
            scene,
            "abo_frames",
            scene,
            "abo_active_frame_index"
        )

        # Add details for the active frame
        if scene.abo_frames and scene.abo_active_frame_index >= 0:
            active_frame = scene.abo_frames[scene.abo_active_frame_index]

            # Show multi-line descriptions. First line is already shown
            description_lines = active_frame.description.splitlines()
            if len(description_lines) > 1:
                layout.label(text="Additional Description:")
                for line in description_lines[1:]:
                    layout.label(text=line)

            # Add the checkbox to co-mesh the atoms and bonds
            row = layout.row()
            row.prop(scene, "abo_show_molecule", text="Show Molecule")
            
            # If no models, disable checkbox (already set to True via update function)
            if active_frame.model_count == 0:
                row.enabled = False

            if active_frame.model_count > 0:
                layout.label(text=f"Models: {active_frame.model_count}")
                layout.label(text=f"Vertices: {active_frame.vertex_count}")
                layout.label(text=f"Faces: {active_frame.face_count}")
            
            # Unit selection dropdown
            layout.prop(scene, "abo_unit_selection", text="Units")

            # Button to generate meshes for the models
            layout.operator("abo.create_meshes_from_frame", text="Create Meshes")


class ABO_UL_Frames(bpy.types.UIList):
    """Custom UIList to display frame descriptions"""

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        # 'item' is the current frame (ABO_Frame_property)
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            display_text = item.description.split('\n')[0]
            layout.label(text=f"{item.index}: {display_text}")
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text=str(item.index))


class ABO_OT_CreateMeshesFromFrame(bpy.types.Operator):
    """Generate mesh objects for all models in the selected frame"""
    bl_idname = "abo.create_meshes_from_frame"
    bl_label = "Create Meshes from Frame"

    _timer = None         # Timer for the modal operator
    _tasks = []           # Task queue
    _is_running = False   # Flag to indicate the process is ongoing

    def execute(self, context):
        scene = context.scene

        # Ensure a valid frame is selected
        if not scene.abo_frames or scene.abo_active_frame_index < 0:
            self.report({'ERROR'}, "No frame selected")
            return {'CANCELLED'}

        if not scene.abo_filepath:
            self.report({'ERROR'}, "No .abo file path stored. Import a file first.")
            return {'CANCELLED'}

        from .py_abo_reader import PyAboReader
        active_frame = PyAboReader().read_frame(scene.abo_filepath, scene.abo_active_frame_index)

        # Prepare task queue
        self._tasks = [
            lambda: self.clear_orbitals(context),
            lambda: self.generate_molecule(context, active_frame),
            lambda: self.validate_data(context, active_frame),
            lambda: self.generate_orbitals(context, active_frame)
        ]
        self._tasks.append(self.finalize)

        # Start modal operator
        self._is_running = True
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        bpy.context.workspace.status_text_set("Generating meshes...")

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self._tasks:
                # Execute the next task in the queue
                task = self._tasks.pop(0)
                task()
            else:
                # All tasks are complete
                self.finish_modal(context)
                return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def clear_orbitals(self, context):
        """Clear all objects in the 'Orbitals' collection."""
        orbitals_collection = bpy.data.collections.get("Orbitals")
        if orbitals_collection:
            for obj in list(orbitals_collection.objects):
                orbitals_collection.objects.unlink(obj)
                bpy.data.objects.remove(obj)

    def generate_molecule(self, context, active_frame):
        """Generate the molecule."""
        from .abo_create_molecule import CreateMolecule
        scene = context.scene
        molecule_collection = bpy.data.collections.get("Molecule")
        bonds_collection = bpy.data.collections.get("Bonds")

        if scene.abo_show_molecule:
            molecule_maker = CreateMolecule()
            molecule_maker.create_molecule(molecule_maker, context, active_frame, molecule_collection)
        else:
            # Delete existing molecules if not asked for
            for collection in [molecule_collection, bonds_collection]:
                if collection:
                    for obj in list(collection.objects):
                        collection.objects.unlink(obj)
                        bpy.data.objects.remove(obj)

    def validate_data(self, context, active_frame):
        """Validate data in the models."""
        if len(active_frame["models"]) > 0:
            for model in active_frame["models"]:
                vertices = model["vertices"]
                faces = model["faces"]
                normals = model["normals"]

                # Skip empty models
                if not vertices or not faces:
                    self.report({'INFO'}, f"Skipping model {model.index} due to empty vertices and/or faces")
                    continue

                # Validate face indices
                for face in faces:
                    if any(v >= len(vertices) for v in face):
                        print(f"Invalid face detected: {face} (max vertex index is {len(vertices) - 1})")
                        raise ValueError(f"Invalid face indices in model {model['index']}")

                # Validate the normals
                if len(normals) != 0 and len(normals) != len(vertices):
                    raise ValueError(f"Normals count ({len(normals)}) does not match vertices count ({len(vertices)}) in model {model['index']}")

                print(f"Data validation successful for model {model['index']}")
                self.report({'INFO'}, f"Model {model['index']}: {len(vertices)} vertices, {len(faces)} faces, {len(normals)} normals")

    def generate_orbitals(self, context, active_frame):
        """Generate orbitals."""
        from .abo_create_orbitals import CreateOrbitals

        if len(active_frame["models"]) > 0:
            CreateOrbitals.create_orbitals(self, active_frame, bpy.data.collections.get("Orbitals"))

    def finalize(self):
        """Finalize the operation."""
        bpy.ops.object.select_all(action="DESELECT")
        if bpy.context.space_data and hasattr(bpy.context.space_data, "shading"):
            bpy.context.space_data.shading.type = 'MATERIAL'
        bpy.context.workspace.status_text_set(None)
        self.report({'INFO'}, "Meshes created successfully!")
        bpy.context.scene.abo_meshes_created = True


    def finish_modal(self, context):
        """Clean up the modal operator."""
        # Clear the status bar
        context.workspace.status_text_set(None)
        context.window_manager.event_timer_remove(self._timer)
        self._is_running = False


class ABO_PT_Tweak_view(bpy.types.Panel):
    """ Panel to tweak the 3D view """
    bl_label = "tweak view"
    bl_idname = "ABO_PT_Tweak_view"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ABO"

    @classmethod
    def poll(cls, context):
        orbitals = bpy.data.collections.get("Orbitals")
        molecule = bpy.data.collections.get("Molecule")
        return bool(getattr(context.scene, "abo_meshes_created", False)) or bool(
            (orbitals and len(orbitals.objects) > 0) or (molecule and len(molecule.objects) > 0)
        )

    def draw(self, context):
        layout = self.layout
        # scene = context.scene

        # Row for X-axis rotation buttons
        row = layout.row()
        row.operator("abo.rotate_orbitals_x", text="X 15°").degrees = 15
        row.operator("abo.rotate_orbitals_x", text="X 90°").degrees = 90

        # Row for Z-axis rotation buttons
        row = layout.row()
        row.operator("abo.rotate_orbitals_z", text="Z 15°").degrees = 15
        row.operator("abo.rotate_orbitals_z", text="Z 90°").degrees = 90

        # Row for changing the transparency of the orbitals
        row = layout.row()
        row.operator("abo.change_transparency", text="Transp. down").d_alpha = 0.1
        row.operator("abo.change_transparency", text="Transp. up").d_alpha = -0.1

        # Row for zooming the camera view in or out
        row = layout.row()
        row.operator("abo.change_zoom", text="Zoom in").d_distance = -2.0
        row.operator("abo.change_zoom", text="Zoom out").d_distance = 2.0
        
        # Row for changing the colors
        row = layout.row()
        row.operator("abo.edit_material_colors", text="Edit colors")

        scene = context.scene
        if getattr(scene, "abo_color_editing", False):
            layout.separator()
            col = layout.column()

            for entry in scene.abo_color_entries:
                row = col.row()
                row.label(text=entry.material_name)
                row.prop(entry, "material_color", text="")

            row = layout.row()
            row.operator("abo.confirm_material_colors", text="Confirm")
            row.operator("abo.cancel_material_colors", text="Cancel")

def rotate_objects(axis, degrees, center=(0, 0, 0)):
    """Rotate atoms, bonds and orbitals over a defined axis."""
    import math
    from mathutils import Matrix

    for collection in ["Orbitals", "Molecule", "Bonds"]:
        object_collection = bpy.data.collections.get(collection)
        if not object_collection:
            continue

        # Convert degrees to radians
        radians = math.radians(degrees)

        # Create a rotation matrix for the specified axis
        rotation_matrix = Matrix.Rotation(radians, 4, axis)

        # Translate objects to the center point, apply rotation, and translate back
        translation_matrix = Matrix.Translation(center)
        inverse_translation_matrix = Matrix.Translation([-c for c in center])
        transformation_matrix = translation_matrix @ rotation_matrix @ inverse_translation_matrix

        for obj in object_collection.objects:
            # Apply the transformation to the object's location
            obj.location = transformation_matrix @ obj.location

            # Rotate the object's orientation (rotation_euler)
            rotation_euler = obj.rotation_euler.to_matrix().to_4x4()
            new_rotation = rotation_matrix @ rotation_euler
            obj.rotation_euler = new_rotation.to_euler()


class ABO_OT_RotateOrbitalsX(bpy.types.Operator):
    """Rotate the Orbitals collection around the X-axis."""
    bl_idname = "abo.rotate_orbitals_x"
    bl_label = "Rotate Orbitals X"

    degrees: bpy.props.IntProperty(default=15)

    def execute(self, context):
        rotate_objects(axis='X', degrees=self.degrees)
        return {'FINISHED'}


class ABO_OT_RotateOrbitalsZ(bpy.types.Operator):
    """Rotate the Orbitals collection around the Z-axis."""
    bl_idname = "abo.rotate_orbitals_z"
    bl_label = "Rotate Orbitals Z"

    degrees: bpy.props.IntProperty(default=15)

    def execute(self, context):
        rotate_objects(axis='Z', degrees=self.degrees)
        return {'FINISHED'}


def change_alpha(d_alpha=-0.1):
    """Change Alpha value (transparency) of all orbital materials"""
    for material in bpy.data.materials:
        if material.name.startswith("orbital"):
            alpha = material.node_tree.nodes["Principled BSDF"].inputs[4]
            alpha.default_value = max(0.1, min(1, alpha.default_value + d_alpha))


class ABO_OT_ChangeTransparency(bpy.types.Operator):
    """Change the transparency of the orbitals"""
    bl_idname = "abo.change_transparency"
    bl_label = "Change Transparency"

    d_alpha: bpy.props.FloatProperty(default=-0.1)

    def execute(self, context):
        change_alpha(self.d_alpha)
        return {'FINISHED'}


def change_zoom(d_distance=-2.0):
    """Change camera zoom by adapting the scale of the CameraPath"""
    if not "CameraPath" in bpy.data.objects:
        raise KeyError("CameraPath not found. Set camera settings first.")
    else:
        camera_path = bpy.data.objects["CameraPath"]

    original_distance = bpy.context.scene.abo_camera_position
    current_distance = camera_path.scale[0] * original_distance
    new_distance = max(2.5, current_distance + d_distance)
    new_scale = new_distance / original_distance

    camera_path.scale = (new_scale, new_scale, 1.0)


class ABO_OT_ChangeZoom(bpy.types.Operator):
    """Zoom the camera view in or out"""
    bl_idname = "abo.change_zoom"
    bl_label = "Change Zoom"

    d_distance: bpy.props.FloatProperty(default=-2.0)

    def execute(self, context):
        change_zoom(d_distance=self.d_distance)
        return {'FINISHED'}


class ABO_OT_EditMaterialColors(bpy.types.Operator):
    bl_idname = "abo.edit_material_colors"
    bl_label = "Edit Material Colors"

    _original_colors = {}

    def invoke(self, context, event):
        scene = context.scene

        # Prepare color entries from materials
        scene.abo_color_entries.clear()
        self._original_colors.clear()

        for mat in bpy.data.materials:
            # Loop over all existing materials following naming convention
            if mat.name.startswith(("molecule_material_", 
                                    "orbital_material_", 
                                    "bonds_material")):
                
                # Get original color
                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                if bsdf:
                    color = bsdf.inputs["Base Color"].default_value[:]
                else:
                    # reaching this error is almost surely user error...
                    raise(KeyError, f"BSDF node not encountered for material {mat} \n\
                                      please re-generate meshes")
                
                # Make popup entry
                entry = scene.abo_color_entries.add()
                entry.material_name = mat.name
                entry.material_color = color
                
                # Cache original color
                self._original_colors[mat.name] = color

        if not scene.abo_color_entries:
            self.report({'WARNING'}, "No ABO-related materials found")
            return {'CANCELLED'}

        scene.abo_color_editing = True
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column()

        for entry in scene.abo_color_entries:
            row = col.row()
            row.label(text=entry.material_name)
            row.prop(entry, "material_color", text="")

        layout.separator()
        row = layout.row()
        row.operator("abo.confirm_material_colors", text="Confirm")
        row.operator("abo.cancel_material_colors", text="Cancel")

    def execute(self, context):
        return self.invoke(context, None)


class ABO_MaterialColorContainer(bpy.types.PropertyGroup):
    """Temporary storage container for material colors"""
    material_name: bpy.props.StringProperty()
    material_color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0,1.0,1.0,1.0),
        options={'SKIP_SAVE', 'HIDDEN'}
    )


class ABO_OT_ConfirmMaterialColors(bpy.types.Operator):
    bl_idname = "abo.confirm_material_colors"
    bl_label = "Apply Colors"

    def execute(self, context):
        for entry in context.scene.abo_color_entries:
            mat = bpy.data.materials.get(entry.material_name)
            bsdf = mat.node_tree.nodes.get("Principled BSDF") if mat else None
            if bsdf:
                bsdf.inputs["Base Color"].default_value = entry.material_color
                mat.diffuse_color = entry.material_color

        context.scene.abo_color_editing = False
        for area in context.screen.areas:
            area.tag_redraw()
        return {'FINISHED'}


class ABO_OT_CancelMaterialColors(bpy.types.Operator):
    bl_idname = "abo.cancel_material_colors"
    bl_label = "Cancel Color Changes"

    def execute(self, context):
        for entry in context.scene.abo_color_entries:
            mat = bpy.data.materials.get(entry.material_name)
            original = ABO_OT_EditMaterialColors._original_colors.get(entry.material_name)
            bsdf = mat.node_tree.nodes.get("Principled BSDF") if mat else None
            if bsdf and original:
                bsdf.inputs["Base Color"].default_value = original
                mat.diffuse_color = original

        context.scene.abo_color_editing = False
        for area in context.screen.areas:
            area.tag_redraw()
        return {'CANCELLED'}


class ABO_PT_Render(bpy.types.Panel):
    """ Panel to start rendering """
    bl_label = "render"
    bl_idname = "ABO_PT_Render"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ABO"

    @classmethod
    def poll(cls, context):
        orbitals = bpy.data.collections.get("Orbitals")
        molecule = bpy.data.collections.get("Molecule")
        return bool(getattr(context.scene, "abo_meshes_created", False)) or bool(
            (orbitals and len(orbitals.objects) > 0) or (molecule and len(molecule.objects) > 0)
        )

    def draw(self, context):
        layout = self.layout

        # Render single frame
        layout.operator("abo.render_single_frame", text="Render Current Frame", icon="RENDER_STILL")

        # Render animation with confirmation dialog
        layout.operator("abo.render_animation", text="Render Animation", icon="RENDER_ANIMATION")


def configure_single_frame_output(scene):
    """Configure output settings for a still render with transparency."""
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"


def configure_animation_output(scene):
    """Configure output settings for an RGB FFmpeg animation."""
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.image_settings.color_mode = "RGB"


class ABO_OT_RenderSingleFrame(bpy.types.Operator):
    """Render the current frame"""
    bl_idname = "abo.render_single_frame"
    bl_label = "Render Current Frame"

    def execute(self, context):
        configure_single_frame_output(context.scene)
        bpy.ops.render.render("INVOKE_DEFAULT")
        return {'FINISHED'}


class ABO_OT_RenderAnimationConfirm(bpy.types.Operator):
    """Ask for confirmation before rendering the animation"""
    bl_idname = "abo.render_animation"
    bl_label = "Render Animation"

    def execute(self, context):
        bpy.ops.abo.confirm_render_animation("INVOKE_DEFAULT")
        return {'FINISHED'}


class ABO_OT_ConfirmRenderAnimation(bpy.types.Operator):
    """Popup to confirm rendering animation"""
    bl_idname = "abo.confirm_render_animation"
    bl_label = "Render Animation"

    def execute(self, context):
        configure_animation_output(context.scene)
        bpy.ops.render.render("INVOKE_DEFAULT", animation=True)  # Start animation rendering
        self.report({'INFO'}, "Rendering animation started!")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)  # Use props dialog to customize text

    def draw(self, context):
        """Custom warning message inside the pop-up"""
        layout = self.layout
        layout.label(text="Rendering an animation may take a long time!", icon="ERROR")
        layout.label(text="Are you sure you want to continue?")



classes = (
    ABO_PT_Initialize_workspace,
    ABO_OT_Delete_elements,
    ABO_OT_Camera_setup,
    ABO_PT_Import_abofile,
    ABO_OT_Import_abofile,
    ABO_Atom,
    ABO_Model,
    ABO_Frame_property,
    ABO_UL_Frames,
    ABO_PT_Frames,
    ABO_OT_CreateMeshesFromFrame,
    ABO_PT_Tweak_view,
    ABO_OT_RotateOrbitalsX,
    ABO_OT_RotateOrbitalsZ,
    ABO_OT_ChangeTransparency,
    ABO_OT_ChangeZoom,
    ABO_OT_EditMaterialColors,
    ABO_MaterialColorContainer,
    ABO_OT_ConfirmMaterialColors,
    ABO_OT_CancelMaterialColors,
    ABO_PT_Render,
    ABO_OT_RenderSingleFrame,
    ABO_OT_RenderAnimationConfirm,
    ABO_OT_ConfirmRenderAnimation,
)


def register_properties():
    # Define starting camera distance, since this is used in multiple classes
    bpy.types.Scene.abo_camera_position = bpy.props.FloatProperty(
        name = "Starting Camera Position",
        description = "Initial position of the camera",
        default=15.0
    )
    
    # Define the frames
    bpy.types.Scene.abo_frames = bpy.props.CollectionProperty(
        type=ABO_Frame_property
    )
    
    # Define tha active frame
    bpy.types.Scene.abo_active_frame_index = bpy.props.IntProperty(
        name="Active Frame Index",
        default=0,
        update=update_active_frame  # Update function triggers when changing frames
    )

    # Define whether the molecule must be drawn
    bpy.types.Scene.abo_show_molecule = bpy.props.BoolProperty(
        name="Show Molecule",
        description="Toggle the display of the molecule",
        default=True
    )

    # Define the unit of the new objects
    bpy.types.Scene.abo_unit_selection = bpy.props.EnumProperty(
        name="Units",
        description="Select the unit for measurements",
        items=[
            ('BOHR', "Bohr", "Use Bohr as the unit"),
            ('ANGSTROM', "Angstrom", "Use Angstrom as the unit"),
        ],
        default='BOHR'
    )

    # Define the unit of the existing objects
    bpy.types.Scene.abo_previous_unit = bpy.props.EnumProperty(
        name="Previous Render Unit",
        description="Set the previously rendered unit",
        items=[
            ('BOHR', "Bohr", "Use Bohr as the unit"),
            ('ANGSTROM', "Angstrom", "Use Angstrom as the unit"),
            ('NONE', "None", "No render yet")
        ],
        default='NONE'
    )

    bpy.types.Scene.abo_filepath = bpy.props.StringProperty(
        name=".abo File Path",
        subtype="FILE_PATH",
        default=""
    )

    bpy.types.Scene.abo_meshes_created = bpy.props.BoolProperty(
        name="ABO Meshes Created",
        default=False,
        options={'SKIP_SAVE'}
    )

    bpy.types.Scene.abo_color_entries = bpy.props.CollectionProperty(
        type=ABO_MaterialColorContainer
    )

    bpy.types.Scene.abo_color_editing = bpy.props.BoolProperty(
        name="Editing ABO Colors",
        default=False,
        options={'SKIP_SAVE'}
    )


def update_active_frame(self, context):
    """Ensure 'Show Molecule' is checked when selecting a frame with no models"""
    if context.scene.abo_frames and self.abo_active_frame_index >= 0:
        active_frame = context.scene.abo_frames[self.abo_active_frame_index]
        if active_frame.model_count == 0:
            # Force checkbox to True when no models are present
            self.abo_show_molecule = True  


def register():
    """ Register """
    
    # Register initial classes
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # Register custom defined properties
    register_properties()


def unregister_properties():
    for property_name in (
        "abo_camera_position",
        "abo_frames",
        "abo_active_frame_index",
        "abo_show_molecule",
        "abo_unit_selection",
        "abo_previous_unit",
        "abo_filepath",
        "abo_meshes_created",
        "abo_color_entries",
        "abo_color_editing",
    ):
        if hasattr(bpy.types.Scene, property_name):
            delattr(bpy.types.Scene, property_name)


def unregister():
    """ Unregister """
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    unregister_properties()
