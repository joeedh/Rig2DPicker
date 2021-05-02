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

        ob = context.active_object

        if not ob:
          return

        arm = ob.data
        
        if type(arm) != bpy.types.Armature:
          return
        
        layouts2d = arm.layouts2d 

        row = ui.row() 
        row.operator("export.layout2d_layouts")
        row.operator("import.layout2d_layouts")
        
        move_mode = layouts2d.edit_mode and layouts2d.edit_type == "MOVE"
        labels_mode = layouts2d.edit_mode and layouts2d.edit_type == "LABELS"
        emphasis_mode = layouts2d.edit_mode and layouts2d.edit_type == "EMPHASIS"
        edit_mode = layouts2d.edit_mode and layouts2d.edit_type == "EDIT"

        if edit_mode:
          row = ui.row()
          row.operator("object.layout2d_add")
          row.operator("object.layout2d_duplicate")

        if layouts2d.edit_mode:
          row = ui.row()
          row.prop(layouts2d, "edit_mode")
          row.prop(layouts2d, "edit_type")
        else:
          row = ui.row() 
          row.prop(layouts2d, "edit_mode")
          row.prop(layouts2d, "select_multiple")
        
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

              if item.emphasis:
                box = row2.box()
                box.alignment = "LEFT"
              else:
                box = row2

              bone = item.bone
              if bone in arm.bones and arm.bones[bone].select:
                box = box.box()
                box.alignment = "LEFT"
                box.alert = True

              label = item.bone if item.label == "" else item.label

              if labels_mode:
                box.prop(item, "label", text="")
              elif emphasis_mode:
                props = box.operator("object.layout2d_item_toggle_emphasis", text=label)
                props.layout = layout.name
                props.row = i
                props.item = j
              else:
                props = box.operator("object.layout2d_select_bone", text=label)
                props.bone = item.bone
                props.select_multiple = layouts2d.select_multiple
                pass

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