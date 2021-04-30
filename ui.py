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
    bl_context = "data"

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

        row = ui.row() 
        row.operator("export.layout2d_layouts")
        row.operator("import.layout2d_layouts")
        
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

        if edit_mode:
          props = row.operator("object.layout2d_delete", icon="TRASH")
          props.layout = layout.name

          row.prop(layout, "name")

        for i, lrow in enumerate(layout.rows):
            if edit_mode:
              row = ui.row(align=True)
              row.alignment = "LEFT"

              props = row.operator("object.layout2d_delete_row", icon="TRASH", text="Delete Row")
              props.layout = layout.name
              props.row = i
              
              #"""
              props = row.operator("object.layout2d_add_row", icon="PLUS", text="Insert Row")
              props.layout = layout.name
              props.before_row = i
              #"""

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
                props = row2.operator("object.layout2d_shift_item", icon="TRIA_LEFT", text="")
                props.layout = layout.name
                props.row = i
                props.item = j
                props.direction = -1

              for k in range(item.prePad):
                row2.label(text=" ")

              props = row2.operator("object.layout2d_select_bone", text=item.bone)
              props.bone = item.bone

              if move_mode:
                props = row2.operator("object.layout2d_shift_item", icon="TRIA_RIGHT", text="")
                props.layout = layout.name
                props.row = i
                props.item = j
                props.direction = 1

                #row2.label(text=" ")


            if edit_mode:
              props = row.operator("object.layout2d_add_item", icon="PLUS", text="")
              props.layout = layout.name
              props.row = i
              props.before_item = len(lrow.items)

        if edit_mode:
          row = ui.row(align=True)
          row.alignment = "LEFT"
          props = row.operator("object.layout2d_add_row", icon="PLUS", text="Add Row")
          props.layout = layout.name
          props.before_row = len(layout.rows)

bpy_exports = [Rig2dPickPanel]