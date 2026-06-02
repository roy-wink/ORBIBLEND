import importlib.util
import os
import sys
import time

import bpy


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADDON_DIR = os.path.join(ROOT, "abo-addon")
ADDON_INIT = os.path.join(ADDON_DIR, "__init__.py")
STARTED = time.perf_counter()
COUNTS = {
    "depsgraph_pre": 0,
    "depsgraph_post": 0,
    "render_init": 0,
    "render_pre": 0,
    "render_post": 0,
    "render_complete": 0,
    "render_cancel": 0,
}
DRAW_COUNTS = {}
LAST_DRAW_COUNTS = {}
FORCE_SOLID = os.environ.get("ORBIBLEND_PROBE_FORCE_SOLID") == "1"
HIDE_MESHES = os.environ.get("ORBIBLEND_PROBE_HIDE_MESHES") == "1"
JOB_NAMES = (
    "RENDER",
    "RENDER_PREVIEW",
    "OBJECT_BAKE",
    "COMPOSITE",
    "SHADER_COMPILATION",
)


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


def count_scene():
    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    return {
        "objects": len(bpy.data.objects),
        "meshes": len(meshes),
        "materials": len(bpy.data.materials),
        "polygons": sum(len(obj.data.polygons) for obj in meshes),
        "vertices": sum(len(obj.data.vertices) for obj in meshes),
    }


def active_jobs():
    if not hasattr(bpy.app, "is_job_running"):
        return "unavailable"

    running = []
    for job_name in JOB_NAMES:
        try:
            if bpy.app.is_job_running(job_name):
                running.append(job_name)
        except TypeError:
            pass
    return running


def shading_type():
    area = next((area for area in bpy.context.screen.areas if area.type == "VIEW_3D"), None)
    if not area:
        return "no_view3d"
    for space in area.spaces:
        if space.type == "VIEW_3D":
            return space.shading.type
    return "no_view3d_space"


def force_viewport_solid():
    for area in bpy.context.screen.areas:
        if area.type != "VIEW_3D":
            continue
        for space in area.spaces:
            if space.type == "VIEW_3D":
                space.shading.type = "SOLID"


def set_mesh_visibility(hidden):
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.hide_viewport = hidden


def wrap_panel_draws(addon):
    for class_name in (
        "ABO_PT_Initialize_workspace",
        "ABO_PT_Import_abofile",
        "ABO_PT_Frames",
        "ABO_PT_Tweak_view",
        "ABO_PT_Render",
    ):
        cls = getattr(addon.abo_render_addon, class_name, None)
        if cls is None or not hasattr(cls, "draw"):
            continue

        original_draw = cls.draw
        DRAW_COUNTS[class_name] = 0
        LAST_DRAW_COUNTS[class_name] = 0

        def wrapped_draw(self, context, _original_draw=original_draw, _class_name=class_name):
            DRAW_COUNTS[_class_name] += 1
            return _original_draw(self, context)

        cls.draw = wrapped_draw


def draw_count_delta():
    deltas = {}
    for key, value in DRAW_COUNTS.items():
        deltas[key] = value - LAST_DRAW_COUNTS.get(key, 0)
        LAST_DRAW_COUNTS[key] = value
    return deltas


def status_timer():
    scene = bpy.context.scene
    if FORCE_SOLID:
        force_viewport_solid()
    if HIDE_MESHES:
        set_mesh_visibility(True)
    print(
        "PROBE_STATUS",
        f"t={time.perf_counter() - STARTED:.1f}",
        f"jobs={active_jobs()}",
        f"shading={shading_type()}",
        f"color_editing={getattr(scene, 'abo_color_editing', None)}",
        f"color_entries={len(getattr(scene, 'abo_color_entries', [])) if hasattr(scene, 'abo_color_entries') else 'n/a'}",
        f"counts={COUNTS}",
        f"draw_delta={draw_count_delta()}",
        f"force_solid={FORCE_SOLID}",
        f"hide_meshes={HIDE_MESHES}",
        f"scene={count_scene()}",
        flush=True,
    )
    return 1.0


def add_count_handler(handler_name, counter_name):
    def handler(*_args):
        COUNTS[counter_name] += 1
        print(
            "PROBE_HANDLER",
            counter_name,
            f"count={COUNTS[counter_name]}",
            f"t={time.perf_counter() - STARTED:.1f}",
            flush=True,
        )

    handler.__name__ = f"orbiblend_probe_{counter_name}"
    getattr(bpy.app.handlers, handler_name).append(handler)


addon = load_addon()
wrap_panel_draws(addon)
add_count_handler("depsgraph_update_pre", "depsgraph_pre")
add_count_handler("depsgraph_update_post", "depsgraph_post")
add_count_handler("render_init", "render_init")
add_count_handler("render_pre", "render_pre")
add_count_handler("render_post", "render_post")
add_count_handler("render_complete", "render_complete")
add_count_handler("render_cancel", "render_cancel")
bpy.app.timers.register(status_timer, first_interval=1.0, persistent=True)

print("ORBIBLEND probe loaded from", ADDON_INIT)
print("ABO files:")
for name in sorted(os.listdir(os.path.join(ROOT, "abo-files"))):
    if name.endswith(".abo"):
        print(" ", os.path.join(ROOT, "abo-files", name))
