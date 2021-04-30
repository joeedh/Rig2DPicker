import bpy, bmesh
from mathutils import *
from math import *
import json
from .props import ADDON_VERSION

JSON_VERSION = 1
JSON_VERSION_MAP = {
  0 : 0
} #everything else maps to ADDON_VERSION 

def getVersion(jsonversion):
  if jsonversion in JSON_VERSION_MAP:
    return JSON_VERSION_MAP[jsonversion]
  return ADDON_VERSION

def exportLayouts(layouts):
  global JSON_VERSION

  data = layouts.toJSON()
  data["VERSION"] = JSON_VERSION

  return json.dumps(data)

def importLayouts(ob, data, merge=True):
  global JSON_VERSION

  ob.data.layouts2d.loadJSON(data, merge)
  ob.data.layouts2d.version = getVersion(data["VERSION"])
  ob.data.layouts2d.handleVersionChanges()



