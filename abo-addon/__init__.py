bl_info = {
    # Information for the Blender add-on module
    "name": "ORBIBLEND",
    "author": "Roy Wink",
    "version": (0, 2, 0),
    "blender": (4, 5),
    "python":  (3, 11, 11),
    "location": "View3d > UI",
    "warning": "",
    "wiki_url": "",
    "category": "User Interface",
}

from .abo_render_addon import register, unregister
