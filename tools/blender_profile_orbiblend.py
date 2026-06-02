import importlib.util
import os
import resource
import sys
import time

import bpy


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADDON_DIR = os.path.join(ROOT, "abo-addon")
ADDON_INIT = os.path.join(ADDON_DIR, "__init__.py")


class Reporter:
    def __init__(self, filepath):
        self.filepath = filepath
        self._original_colors = {}

    def report(self, level, message):
        print(f"REPORT {level}: {message}")


def elapsed(label, started):
    seconds = time.perf_counter() - started
    rss_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print(f"PROFILE {label}: {seconds:.3f}s maxrss={rss_mb:.1f}MB")


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
    bpy.types.Scene.abo_color_entries = bpy.props.CollectionProperty(
        type=addon.abo_render_addon.ABO_MaterialColorContainer
    )
    bpy.types.Scene.abo_color_editing = bpy.props.BoolProperty(
        name="Editing ABO Colors",
        default=False,
        options={"SKIP_SAVE"},
    )


def frame_counts(frame):
    return {
        "atoms": frame.atom_count,
        "models": frame.model_count,
        "vertices": frame.vertex_count,
        "normals": frame.vertex_count,
        "faces": frame.face_count,
    }


def scene_counts():
    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    return {
        "objects": len(bpy.data.objects),
        "meshes": len(meshes),
        "materials": len(bpy.data.materials),
        "polygons": sum(len(obj.data.polygons) for obj in meshes),
        "vertices": sum(len(obj.data.vertices) for obj in meshes),
    }


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    filepath = args[0] if args else os.path.join(ROOT, "abo-files", "bh3.abo")

    t0 = time.perf_counter()
    load_addon()
    elapsed("load_addon", t0)

    from abo_addon.abo_parse_abofile import AboImport
    from abo_addon.py_abo_reader import PyAboReader
    from abo_addon.abo_render_addon import ABO_OT_CreateMeshesFromFrame, ABO_OT_EditMaterialColors

    t0 = time.perf_counter()
    frames = PyAboReader().read_abofile(filepath)
    elapsed("raw_reader", t0)
    print(
        "PROFILE raw_frames",
        [
            {
                "index": frame["index"],
                "atoms": len(frame["atoms"]),
                "models": len(frame["models"]),
                "vertices": sum(len(model["vertices"]) for model in frame["models"]),
                "faces": sum(len(model["faces"]) for model in frame["models"]),
            }
            for frame in frames
        ],
    )

    t0 = time.perf_counter()
    AboImport.import_abofile(Reporter(filepath), bpy.context)
    elapsed("populate_scene_collections", t0)

    scene = bpy.context.scene
    total_counts = {"atoms": 0, "models": 0, "vertices": 0, "normals": 0, "faces": 0}
    for frame in scene.abo_frames:
        counts = frame_counts(frame)
        for key in total_counts:
            total_counts[key] += counts[key]
        print(f"PROFILE frame {frame.index}: {counts}")
    print(f"PROFILE stored_totals: {total_counts}")

    active_index = max(
        range(len(scene.abo_frames)),
        key=lambda i: frame_counts(scene.abo_frames[i])["vertices"],
    )
    scene.abo_active_frame_index = active_index
    active_frame_metadata = scene.abo_frames[active_index]
    print(f"PROFILE selected_frame={active_frame_metadata.index} counts={frame_counts(active_frame_metadata)}")
    active_frame = PyAboReader().read_frame(filepath, active_index)

    reporter = Reporter(filepath)

    for label, func in (
        ("clear_orbitals", lambda: ABO_OT_CreateMeshesFromFrame.clear_orbitals(reporter, bpy.context)),
        ("generate_molecule", lambda: ABO_OT_CreateMeshesFromFrame.generate_molecule(reporter, bpy.context, active_frame)),
        ("validate_data", lambda: ABO_OT_CreateMeshesFromFrame.validate_data(reporter, bpy.context, active_frame)),
        ("generate_orbitals", lambda: ABO_OT_CreateMeshesFromFrame.generate_orbitals(reporter, bpy.context, active_frame)),
    ):
        t0 = time.perf_counter()
        func()
        elapsed(label, t0)
        print(f"PROFILE scene_after_{label}: {scene_counts()}")

    t0 = time.perf_counter()
    result = ABO_OT_EditMaterialColors.invoke(reporter, bpy.context, None)
    elapsed("edit_colors_setup", t0)
    print(f"PROFILE edit_colors_result={result} entries={len(scene.abo_color_entries)}")


if __name__ == "__main__":
    main()
