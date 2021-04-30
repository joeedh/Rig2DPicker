import bpy, bmesh 
from mathutils import *
from math import *
from .Global import *

class Rig2dPickPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "2D Bone Picker"
    bl_idname = "SCENE_PT_layout2d"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        ui = self.layout

        ui.operator("object.layout2d_add")
        ob = context.active_object

        if not ob:
          return

        arm = ob.data
        
        if type(arm) != bpy.types.Armature:
          return
        
        layouts2d = arm.layouts2d 

        edit_mode = layouts2d.edit_mode
        edit_type = layouts2d.edit_type

        move_mode = edit_mode and edit_type == "MOVE"
        
        if edit_mode:
          row = ui.row()
          row.prop(layouts2d, "edit_mode")
          row.prop(layouts2d, "edit_type")
        else:
          ui.prop(layouts2d, "edit_mode")

        edit_mode = edit_mode and edit_type == "EDIT"
        
        row = ui.row()
        for layout in layouts2d.layouts:
          props = row.operator("object.layout2d_set_active", text=layout.name)
          if props:
            props.layout = layout.name

        layout = layouts2d.getActive()
        
        if not layout:
          return

        row = ui.row()
        row.label(text=layout.name)
        props = row.operator("object.layout2d_delete", icon="TRASH")
        if props:
          props.layout = layout.name

        if edit_mode:
          row = ui.row(align=True)
          row.alignment = "LEFT"
          props = row.operator("object.layout2d_add_row", icon="PLUS", text="Add Row")
          props.layout = layout.name
          props.before_row = 0

        if len(layout.rows) == 0:
          return

        for i, lrow in enumerate(layout.rows):
            if edit_mode:
              row = ui.row(align=True)
              row.alignment = "LEFT"

              props = row.operator("object.layout2d_delete_row", icon="TRASH", text="Delete Row")
              props.layout = layout.name
              props.row = i

              props = row.operator("object.layout2d_add_row", icon="PLUS", text="Insert Row")
              props.layout = layout.name
              props.before_row = i + 1

            row = ui.row(align=True)
            row.alignment = "CENTER"

            for j, item in enumerate(lrow.items):
              row2 = row

              if edit_mode:
                props = row2.operator("object.layout2d_add_item", icon="PLUS", text="")
                props.layout = layout.name
                props.row = i
                props.before_item = j

                props = row2.operator("object.layout2d_delete_item", icon="TRASH", text="")
                props.layout = layout.name
                props.row = i
                props.item = j
              elif move_mode:
                props = row2.operator("object.layout2d_inc_item_prepad", icon="TRIA_LEFT", text="")
                props.layout = layout.name
                props.row = i
                props.item = j
                props.subtract = True

                props = row2.operator("object.layout2d_inc_item_prepad", icon="TRIA_RIGHT", text="")
                props.layout = layout.name
                props.row = i
                props.item = j
                props.subtract = False

              for k in range(item.prePad):
                row2.label(text=" ")

              props = row2.operator("object.layout2d_select_bone", text=item.bone)
              props.bone = item.bone

            if edit_mode:
              props = row.operator("object.layout2d_add_item", icon="PLUS", text="")
              props.layout = layout.name
              props.row = i
              props.before_item = len(lrow.items)

bpy_exports = [Rig2dPickPanel]