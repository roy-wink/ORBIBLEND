import importlib.util
import os
import sys

import bpy


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADDON_INIT = os.path.join(ROOT, "abo-addon", "__init__.py")
ABO_FILES = [
    os.path.join(ROOT, "abo-files", name)
    for name in sorted(os.listdir(os.path.join(ROOT, "abo-files")))
    if name.endswith(".abo")
]


class Reporter:
    def __init__(self, filepath):
        self.filepath = filepath
        self._original_colors = {}

    def report(self, level, message):
        print(f"REPORT {level}: {message}")


def load_addon():
    spec = importlib.util.spec_from_file_location(
        "abo_addon",
        ADDON_INIT,
        submodule_search_locations=[os.path.dirname(ADDON_INIT)],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.register()
    return module


def summarize_scene(label):
    scene = bpy.context.scene
    print(f"\n== {label} ==")
    print(f"frames={len(scene.abo_frames)}")
    for frame in scene.abo_frames:
        print(
            f"frame={frame.index} atoms={frame.atom_count} "
            f"models={frame.model_count} vertices={frame.vertex_count} faces={frame.face_count} "
            f"description={frame.description.splitlines()[0]!r}"
        )
    abo_materials = [
        mat.name
        for mat in bpy.data.materials
        if mat.name.startswith(("molecule_material_", "orbital_material_", "bonds_material"))
    ]
    print(f"abo_materials={len(abo_materials)} {abo_materials[:20]}")


def main():
    addon = load_addon()
    from abo_addon.abo_parse_abofile import AboImport
    from abo_addon.py_abo_reader import PyAboReader
    from abo_addon.abo_render_addon import ABO_OT_CreateMeshesFromFrame, ABO_OT_EditMaterialColors

    for filepath in ABO_FILES:
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()
        AboImport.import_abofile(Reporter(filepath), bpy.context)
        bpy.context.scene.abo_active_frame_index = max(
            range(len(bpy.context.scene.abo_frames)),
            key=lambda i: bpy.context.scene.abo_frames[i].vertex_count,
        )
        summarize_scene(os.path.basename(filepath) + " imported")

        active_frame = PyAboReader().read_frame(filepath, bpy.context.scene.abo_active_frame_index)
        reporter = Reporter(filepath)
        ABO_OT_CreateMeshesFromFrame.clear_orbitals(reporter, bpy.context)
        ABO_OT_CreateMeshesFromFrame.generate_molecule(reporter, bpy.context, active_frame)
        ABO_OT_CreateMeshesFromFrame.validate_data(reporter, bpy.context, active_frame)
        ABO_OT_CreateMeshesFromFrame.generate_orbitals(reporter, bpy.context, active_frame)
        reporter.report({"INFO"}, "Meshes created successfully!")
        summarize_scene(os.path.basename(filepath) + " meshes")

        color_reporter = Reporter(filepath)
        try:
            result = ABO_OT_EditMaterialColors.invoke(color_reporter, bpy.context, None)
        except Exception as exc:
            result = f"ERROR {type(exc).__name__}: {exc}"
        print(f"edit_colors_invoke={result} color_entries={len(bpy.context.scene.abo_color_entries)}")


if __name__ == "__main__":
    main()
