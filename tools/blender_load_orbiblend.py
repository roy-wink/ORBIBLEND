import importlib.util
import os
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADDON_INIT = os.path.join(ROOT, "abo-addon", "__init__.py")

spec = importlib.util.spec_from_file_location(
    "abo_addon",
    ADDON_INIT,
    submodule_search_locations=[os.path.dirname(ADDON_INIT)],
)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
module.register()

print("ORBIBLEND loaded from", ADDON_INIT)
print("ABO files:")
for name in sorted(os.listdir(os.path.join(ROOT, "abo-files"))):
    if name.endswith(".abo"):
        print(" ", os.path.join(ROOT, "abo-files", name))
