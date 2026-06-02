import importlib.util
import os
import sys
import time

import bpy


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADDON_DIR = os.path.join(ROOT, "abo-addon")
ADDON_INIT = os.path.join(ADDON_DIR, "__init__.py")


class Reporter:
    def __init__(self, filepath):
        self.filepath = filepath

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
    return module


def save(label, path):
    started = time.perf_counter()
    bpy.ops.wm.save_as_mainfile(filepath=path)
    elapsed = time.perf_counter() - started
    print(f"SAVE_SIZE {label}: bytes={os.path.getsize(path)} elapsed={elapsed:.3f}s path={path}")


def counts():
    scene = bpy.context.scene
    totals = {
        "frames": len(scene.abo_frames),
        "atoms": 0,
        "models": 0,
        "vertices": 0,
        "normals": 0,
        "faces": 0,
    }
    for frame in scene.abo_frames:
        totals["atoms"] += frame.atom_count
        totals["models"] += frame.model_count
        totals["vertices"] += frame.vertex_count
        totals["normals"] += frame.vertex_count
        totals["faces"] += frame.face_count
    return totals


def register_mesh_classes(addon):
    for class_name in (
        "ABO_PT_Tweak_view",
        "ABO_OT_RotateOrbitalsX",
        "ABO_OT_RotateOrbitalsZ",
        "ABO_OT_ChangeTransparency",
        "ABO_OT_ChangeZoom",
        "ABO_OT_EditMaterialColors",
        "ABO_OT_ConfirmMaterialColors",
        "ABO_OT_CancelMaterialColors",
        "ABO_MaterialColorContainer",
        "ABO_PT_Render",
        "ABO_OT_RenderSingleFrame",
        "ABO_OT_RenderAnimationConfirm",
        "ABO_OT_ConfirmRenderAnimation",
    ):
        try:
            bpy.utils.register_class(getattr(addon.abo_render_addon, class_name))
        except ValueError:
            pass


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    filepath = args[0] if args else os.path.join(ROOT, "abo-files", "bh3.abo")
    label = os.path.splitext(os.path.basename(filepath))[0]

    load_addon()
    from abo_addon.abo_parse_abofile import AboImport
    from abo_addon.py_abo_reader import PyAboReader
    from abo_addon.abo_render_addon import ABO_OT_CreateMeshesFromFrame

    print(f"SAVE_SIZE source: bytes={os.path.getsize(filepath)} path={filepath}")
    AboImport.import_abofile(Reporter(filepath), bpy.context)
    print(f"SAVE_SIZE stored_counts: {counts()}")
    save("after_import_no_mesh", f"/tmp/{label}-import-only.blend")

    scene = bpy.context.scene
    active_index = max(
        range(len(scene.abo_frames)),
        key=lambda i: scene.abo_frames[i].vertex_count,
    )
    scene.abo_active_frame_index = active_index
    active_frame = PyAboReader().read_frame(filepath, active_index)
    reporter = Reporter(filepath)
    ABO_OT_CreateMeshesFromFrame.clear_orbitals(reporter, bpy.context)
    ABO_OT_CreateMeshesFromFrame.generate_molecule(reporter, bpy.context, active_frame)
    ABO_OT_CreateMeshesFromFrame.validate_data(reporter, bpy.context, active_frame)
    ABO_OT_CreateMeshesFromFrame.generate_orbitals(reporter, bpy.context, active_frame)
    save("after_visible_meshes", f"/tmp/{label}-with-meshes.blend")

    scene.abo_frames.clear()
    save("after_clearing_stored_abo_frames", f"/tmp/{label}-meshes-only.blend")


if __name__ == "__main__":
    main()
