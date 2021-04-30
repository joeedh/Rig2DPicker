import bpy, imp

__all__ = [
  "global", "layout", "props", "ui"
]

from . import layout, props, ui, ops

imp.reload(props)
imp.reload(ops)
imp.reload(layout)
imp.reload(ui)

registered = False

bpy_exports = props.bpy_exports + ui.bpy_exports + ops.bpy_exports

def register():
  global registered

  if registered:
    return

  registered = True
  for cls in bpy_exports:
    bpy.utils.register_class(cls)

def unregister():
  global registered

  if not registered:
    return 
  
  registered = False
  for cls in bpy_exports:
    try:
      bpy.utils.unregister_class(cls)
    except:
      print("Failed to unregister a cls:", cls);
