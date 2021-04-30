import bpy, bmesh 
from mathutils import *
from math import *
from .Global import *
from bpy.props import *

bpy_exports = []

class RigLayoutItem(bpy.types.PropertyGroup):
  bone : StringProperty()
  prePad : IntProperty()

  def load(self, b):
    self.bone = b.bone
    self.prePad = b.prePad

    return self

bpy.utils.register_class(RigLayoutItem)

class RigLayoutRow(bpy.types.PropertyGroup):
  items : CollectionProperty(type=RigLayoutItem)
  
  def insert(self, before_i):
    self.items.add()

    i = len(self.items) - 1

    print("BEFORE_I", before_i)

    while i > before_i:
      self.items[i].load(self.items[i-1])
      i -= 1

    return self.items[before_i]

  def load(self, b):
    if b is self:
      return self

    self.items.clear()
    for item in b.items:
      item2 = self.items.add()
      item2.load(item)

    return self

bpy.utils.register_class(RigLayoutRow)

class RigLayout2d(bpy.types.PropertyGroup):
  name : StringProperty
  rows : CollectionProperty(type=RigLayoutRow)

  def loadRow(self, dst_i, src_i):
    self.rows[dst_i].load(self.rows[src_i])
    return self

bpy.utils.register_class(RigLayout2d)

class RigLayouts(bpy.types.PropertyGroup):
  layouts : CollectionProperty(type=RigLayout2d)
  active_layout : StringProperty()
  edit_mode : BoolProperty()
  edit_type : EnumProperty(items=[("EDIT", "Edit", "", 0), ("MOVE", "Move", "", 1)])

  def getActive(self):
    ret = self.get(self.active_layout)
    if ret:
      return ret
    
    if len(self.layouts) > 0:
      return self.layouts[0]

    return None

  def setActive(self, name):
    self.active_layout = name

  def get(self, name):
    for l in self.layouts:
      if l.name == name:
        return l
    
    return None

  def delete(self, name):
    for i, layout in enumerate(self.layouts):
      if layout.name == name:
        self.layouts.remove(i)
        break

bpy.utils.register_class(RigLayouts)

bpy.types.Armature.layouts2d = PointerProperty(type=RigLayouts)
