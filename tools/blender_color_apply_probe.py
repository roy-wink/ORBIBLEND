import importlib.util
import os
import sys

import bpy


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADDON_DIR = os.path.join(ROOT, "abo-addon")
ADDON_INIT = os.path.join(ADDON_DIR, "__init__.py")
ABO_FILE = os.path.join(ROOT, "abo-files", "bh3.abo")


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
        submodule_search_locations=[ADDON_DIR],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.register()


def main():
    load_addon()
    from abo_addon.abo_parse_abofile import AboImport
    from abo_addon.py_abo_reader import PyAboReader
    from abo_addon.abo_render_addon import (
        ABO_OT_ConfirmMaterialColors,
        ABO_OT_CreateMeshesFromFrame,
        ABO_OT_EditMaterialColors,
    )

    AboImport.import_abofile(Reporter(ABO_FILE), bpy.context)
    scene = bpy.context.scene
    scene.abo_active_frame_index = 6
    active_frame = PyAboReader().read_frame(ABO_FILE, scene.abo_active_frame_index)
    reporter = Reporter(ABO_FILE)
    ABO_OT_CreateMeshesFromFrame.generate_molecule(reporter, bpy.context, active_frame)
    ABO_OT_CreateMeshesFromFrame.validate_data(reporter, bpy.context, active_frame)
    ABO_OT_CreateMeshesFromFrame.generate_orbitals(reporter, bpy.context, active_frame)
    ABO_OT_EditMaterialColors.invoke(reporter, bpy.context, None)

    target = next(entry for entry in scene.abo_color_entries if entry.material_name.startswith("orbital_material_"))
    target.material_color = (0.2, 0.4, 0.8, 1.0)
    ABO_OT_ConfirmMaterialColors.execute(reporter, bpy.context)

    material = bpy.data.materials[target.material_name]
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    print("COLOR_APPLY material", target.material_name)
    print("COLOR_APPLY diffuse", tuple(round(value, 3) for value in material.diffuse_color))
    print("COLOR_APPLY bsdf", tuple(round(value, 3) for value in bsdf.inputs["Base Color"].default_value))


if __name__ == "__main__":
    main()
