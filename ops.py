import bpy, bmesh 
from mathutils import *
from math import *
from .Global import *
from bpy.props import *

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
        
        if self.before_row == len(layout.rows):
          layout.rows.add()
          return {'FINISHED'}

        lrow = layout.rows.add()
        
        i = self.before_row

        while i < len(layout.rows)-1:
          layout.loadRow(i+1, i)
          i += 1

        print("LROW", lrow, self.before_row)
        layout.loadRow(self.before_row, len(layout.rows)-1)
      

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

        print("YAY")

        item = lrow.insert(self.before_item)
        item.bone = context.active_bone.name

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


class SeleteBone(Layout2dOp):
    """Tooltip"""
    bl_idname = "object.layout2d_select_bone"
    bl_label = "Select Bone (rig2dpick)"
    bl_options = {"UNDO"}

    bone : StringProperty()

    def execute(self, context):
        rigob = context.active_object

        posemode = rigob.mode == "POSE"
        bpy.ops.object.mode_set(mode="EDIT")

        arm = rigob.data 
        pose = rigob.pose 
        bpy.ops.armature.select_all(action="DESELECT")

        bone = arm.edit_bones[self.bone]
        bone.select = True
        arm.edit_bones.active = bone
        arm.update_tag()

        if posemode:
          bpy.ops.object.mode_set(mode="POSE")

        return {'FINISHED'}


bpy_exports = [AddLayoutRow, AddLayout, SetActiveLayout, DeleteLayout, DeleteLayoutRow, AddLayoutItem, SeleteBone, DeleteLayoutItem, IncLayoutItemPrePad]
