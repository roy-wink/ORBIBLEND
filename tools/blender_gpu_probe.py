import bpy
import gpu


print("GPU_PROBE renderer", gpu.platform.renderer_get())
print("GPU_PROBE vendor", gpu.platform.vendor_get())
print("GPU_PROBE version", gpu.platform.version_get())
print("GPU_PROBE device_type", gpu.platform.device_type_get())
print("GPU_PROBE render_engine", bpy.context.scene.render.engine)
