import bpy, bmesh
from mathutils import *
from math import *
import json

JSON_VERSION = 0

def exportLayouts(layouts):
  global JSON_VERSION

  data = layouts.toJSON()
  data["VERSION"] = JSON_VERSION

  return json.dumps(data)

def importLayouts(ob, data, merge=True):
  global JSON_VERSION

  ob.data.layouts2d.loadJSON(data, merge)


