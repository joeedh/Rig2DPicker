import bpy, bmesh 
from mathutils import *
from math import *
from .Global import *
from bpy.props import *
from bpy_extras.io_utils import ExportHelper, ImportHelper
from .layout import exportLayouts, importLayouts
import json

class ExportLayouts(bpy.types.Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export.layout2d_layouts"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Layouts (rig2dpick)"

    # ExportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        ob = context.active_object

        data = exportLayouts(ob.data.layouts2d)
        print(data)

        file = open(self.filepath, "w")
        file.write(data)
        file.close()

        #return write_some_data(context, self.filepath, self.use_setting)
        return {'FINISHED'}


class ImportLayouts(bpy.types.Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import.layout2d_layouts"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Layouts (rig2dpick)"
    bl_options = {"UNDO"}

    # ExportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    merge : BoolProperty(default=True)
    
    def execute(self, context):
        ob = context.active_object

        data = exportLayouts(ob.data.layouts2d)
        print(data)
        
        file = open(self.filepath, "r")
        buf = file.read()
        file.close()

        data = json.loads(buf)
        importLayouts(ob, data, self.merge)

        #return write_some_data(context, self.filepath, self.use_setting)
        return {'FINISHED'}


class Layout2dOp(bpy.types.Operator):
    @classmethod
    def poll(cls, context):
        ok = context.active_object is not None
        ok = ok and type(context.active_object.data) == bpy.types.Armature
        return ok


class AddLayoutRow(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_add_row"
    bl_label = "Add Layout Row (rig2dpick)"
    bl_options = {"UNDO"}

    layout : StringProperty()
    before_row : IntProperty()

    def execute(self, context):
        arm = context.active_object.data 
        layout = arm.layouts2d.get(self.layout)

        if not layout:
          print("invalid layout '%s'" % (self.layout))
          return {'CANCELLED'}
      
        layout.insert(self.before_row)
      
        return {'FINISHED'}


class ToggleEmphasis(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_item_toggle_emphasis"
    bl_label = "Toggle Layout Item Emphasis (rig2dpick)"
    bl_options = {"UNDO"}

    layout : StringProperty()
    row : IntProperty()
    item : IntProperty()

    def execute(self, context):
        arm = context.active_object.data 
        layout = arm.layouts2d.get(self.layout)

        if not layout:
          print("invalid layout '%s'" % (self.layout))
          return {'CANCELLED'}
      
        lrow = layout.rows[self.row]
        item = lrow.items[self.item]

        item.emphasis ^= True
      
        return {'FINISHED'}

class DeleteLayoutRow(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_delete_row"
    bl_label = "Delete Layout Row (rig2dpick)"
    bl_options = {"UNDO"}

    layout : StringProperty()
    row    : IntProperty()

    def execute(self, context):
        arm = context.active_object.data 
        layout = arm.layouts2d.get(self.layout)

        if not layout:
          print("invalid layout '%s'" % (self.layout))
          return {'CANCELLED'}

        layout.rows.remove(self.row)
        
        return {'FINISHED'}

class AddLayoutItem(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_add_item"
    bl_label = "Add Layout Row (rig2dpick)"
    bl_options = {"UNDO"}

    layout : StringProperty()
    row : IntProperty()
    before_item : IntProperty()

    @classmethod
    def poll(cls, context):
        ok = context.active_object is not None
        ok = ok and type(context.active_object.data) == bpy.types.Armature
        ok = ok and context.active_bone is not None

        return ok

    def execute(self, context):
        arm = context.active_object.data 
        layout = arm.layouts2d.get(self.layout)

        if not layout:
          print("invalid layout '%s'" % (self.layout))
          return {'CANCELLED'}
        
        lrow = layout.rows[self.row]

        item = lrow.insert(self.before_item)
        item.bone = context.active_bone.name
        item.label = item.bone

        return {'FINISHED'}


class ShfitLayoutItem(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_shift_item"
    bl_label = "Shift Layout Item (rig2dpick)"
    bl_options = {"UNDO"}

    layout : StringProperty()
    row : IntProperty()
    item : IntProperty()
    direction : IntProperty()

    def execute(self, context):
        arm = context.active_object.data 
        layout = arm.layouts2d.get(self.layout)

        if not layout:
          print("invalid layout '%s'" % (self.layout))
          return {'CANCELLED'}
        
        lrow = layout.rows[self.row]
        item = lrow.items[self.item]
        dir = self.direction

        i2 = self.item + dir
        if i2 < 0 or i2 >= len(lrow.items):
          return

        lrow.swap(self.item, i2)

        return {'FINISHED'}

class DeleteLayoutItem(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_delete_item"
    bl_label = "Delete Layout Item (rig2dpick)"
    bl_options = {"UNDO"}

    layout : StringProperty()
    row : IntProperty()
    item : IntProperty()

    def execute(self, context):
        arm = context.active_object.data 
        layout = arm.layouts2d.get(self.layout)

        if not layout:
          print("invalid layout '%s'" % (self.layout))
          return {'CANCELLED'}
        
        lrow = layout.rows[self.row]
        lrow.items.remove(self.item)

        return {'FINISHED'}


class IncLayoutItemPrePad(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_inc_item_prepad"
    bl_label = "Increment left item pad (rig2dpick)"
    bl_options = {"UNDO"}

    layout : StringProperty()
    row : IntProperty()
    subtract : BoolProperty()
    item : IntProperty()

    def execute(self, context):
        arm = context.active_object.data 
        layout = arm.layouts2d.get(self.layout)

        if not layout:
          print("invalid layout '%s'" % (self.layout))
          return {'CANCELLED'}
        
        lrow = layout.rows[self.row]
        item = lrow.items[self.item]

        item.prePad += -1 if self.subtract else 1
        
        return {'FINISHED'}

class AddLayout(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_add"
    bl_label = "Add Layout (rig2dpick)"
    bl_options = {"UNDO"}

    def execute(self, context):
        name = "Layout"
        i = 2

        rigob = context.active_object
        arm = rigob.data

        #ensure unique name
        while arm.layouts2d.get(name):
          name = "Layout%i" % (i)
          i += 1

        layout = arm.layouts2d.layouts.add()
        layout.name = name

        return {'FINISHED'}


class SetActiveLayout(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_set_active"
    bl_label = "Set Active Layout (rig2dpick)"
    bl_options = {"UNDO"}

    layout : StringProperty()

    def execute(self, context):
        name = "Layout"
        i = 2

        rigob = context.active_object
        arm = rigob.data

        arm.layouts2d.setActive(self.layout)
        
        return {'FINISHED'}


class SetActiveLayout(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_set_active"
    bl_label = "Set Active Layout (rig2dpick)"
    bl_options = {"UNDO"}

    layout : StringProperty()

    def execute(self, context):
        name = "Layout"
        i = 2

        rigob = context.active_object
        arm = rigob.data

        arm.layouts2d.setActive(self.layout)
        
        return {'FINISHED'}

class DeleteLayout(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_delete"
    bl_label = "Delete Layout (rig2dpick)"
    bl_options = {"UNDO"}

    layout : StringProperty()

    def execute(self, context):
        name = "Layout"
        i = 2

        rigob = context.active_object
        arm = rigob.data

        layout = arm.layouts2d.get(self.layout)
        if not layout:
          print("invalid layout!", self.layout)
          return {'CANCELLED'}

        arm.layouts2d.delete(self.layout)

        return {'FINISHED'}

class SelectBone(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_select_bone"
    bl_label = "Select Bone (rig2dpick)"
    bl_options = {"UNDO"}

    bone : StringProperty()
    select_multiple : BoolProperty()

    def execute(self, context):
        rigob = context.active_object

        posemode = rigob.mode == "POSE"
        #bpy.ops.object.mode_set(mode="EDIT")
        if rigob.mode == "OBJECT":
          bpy.ops.object.mode_set(mode="POSE")

        arm = rigob.data 
        pose = rigob.pose 

        if not self.select_multiple:
          if rigob.mode == "EDIT":
            bpy.ops.armature.select_all(action="DESELECT")
          else:
            bpy.ops.pose.select_all(action="DESELECT")

        bone = arm.bones[self.bone]
        if not bone.select or not self.select_multiple:
          bone.select = True
          arm.bones.active = bone
        else:
          bone.select = False

        #arm.update_tag()

        #if posemode:
        #  bpy.ops.object.mode_set(mode="POSE")

        return {'FINISHED'}


bpy_exports = [AddLayoutRow, AddLayout, SetActiveLayout, DeleteLayout, 
DeleteLayoutRow, AddLayoutItem, SelectBone, DeleteLayoutItem, IncLayoutItemPrePad,
ShfitLayoutItem, ExportLayouts, ImportLayouts, ToggleEmphasis]
