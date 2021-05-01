import bpy, bmesh 
from mathutils import *
from math import *
from .Global import *
from bpy.props import *

bpy_exports = []

class RigLayoutItem(bpy.types.PropertyGroup):
  bone : StringProperty()
  label : StringProperty() #if empty string, bone name will be used
  prePad : IntProperty()
  emphasis : BoolProperty()

  def load(self, b):
    self.bone = b.bone
    self.prePad = b.prePad
    self.label = b.label
    self.emphasis = b.emphasis

    return self
      
  def toJSON(self):
    return {
      "bone" : self.bone,
      "prePad" : self.prePad,
      "label" : self.label,
      "emphasis" : self.emphasis
    }
  
  def loadJSON(self, json):
    self.bone = json["bone"]
    self.prePad = json["prePad"]

    if "emphasis" in json:
      self.emphasis = json["emphasis"]

    self.label = json["label"]

    return self

bpy.utils.register_class(RigLayoutItem)

class RigLayoutRow(bpy.types.PropertyGroup):
  items : CollectionProperty(type=RigLayoutItem)
  
  def swap(self, i1, i2):
    item = self.items.add()
    item.load(self.items[i1])
    
    self.items[i1].load(self.items[i2])
    self.items[i2].load(item)
    self.items.remove(len(self.items)-1)
    return self

  def toJSON(self):
    jitems = []
    for item in self.items:
      jitems.append(item.toJSON())
    
    return {
      "items" : jitems
    }

  def loadJSON(self, json):
    self.items.clear()

    for jitem in json["items"]:
      item = self.items.add()
      item.loadJSON(jitem)

    return self

  def insert(self, before_i):
    self.items.add()

    i = len(self.items) - 1

    print("BEFORE_I", before_i)

    while i > before_i:
      self.items[i].load(self.items[i-1])
      i -= 1

    return self.items[before_i]

  def clear(self):
    self.items.clear()
    return self

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
  
  def clear(self):
    self.rows.clear()
    return self

  def toJSON(self):
    jrows = []
    for row in self.rows:
      jrows.append(row.toJSON())

    return {
      "rows" : jrows,
      "name" : self.name
    }
  
  def loadJSON(self, json):
    self.name = json["name"]
    self.rows.clear()

    for jrow in json["rows"]:
      row = self.rows.add()
      row.loadJSON(jrow)
      
    return self

  def swap(self, i1, i2):
    row = self.rows.add()
    row.load(self.rows[i1])
    self.rows[i1].load(self.rows[i2])
    self.rows[i2].load(row)
    self.rows.remove(len(self.rows))
    return self

  def insert(self, before_i):
    self.rows.add()

    i = len(self.rows) - 1

    while i > before_i:
      self.rows[i].load(self.rows[i-1])
      i -= 1

    self.rows[before_i].clear()
    return self.rows[before_i]

bpy.utils.register_class(RigLayout2d)

ADDON_VERSION = 1

class RigLayouts(bpy.types.PropertyGroup):
  layouts : CollectionProperty(type=RigLayout2d)
  version : IntProperty(default=ADDON_VERSION)

  active_layout : StringProperty()
  edit_mode : BoolProperty()
  edit_type : EnumProperty(items=[
    ("EDIT", "Edit", "", 0), 
    ("MOVE", "Move", "", 1),
    ("LABELS", "Labels", "", 2),
    ("EMPHASIS", "Emphasis", "", 3)
  ])
  select_multiple : BoolProperty()

  def handleVersionChanges(self):
    if self.version < 1:
      for layout in self.layouts:
        for row in layout.rows:
          for item in row.items:
            item.label = item.bone

  def toJSON(self):
    layouts = []

    for layout in self.layouts:
      layouts.append(layout.toJSON())

    return {
      "active_layout" : self.active_layout,
      "layouts" : layouts
    }

  def loadJSON(self, json, merge=True):
    if not merge:
      self.clear()
    
    self.active_layout = json["active_layout"]
    for jlayout in json["layouts"]:
      layout = self.get(jlayout["name"])
      if not layout:
        layout = self.layouts.add()
      
      layout.loadJSON(jlayout)

    return self

  def clear(self):
    self.active_layout = ""
    self.layouts.clear()
    return self

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
