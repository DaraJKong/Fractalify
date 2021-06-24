"""
Copyright (C) 2021 Dara J. Kong
daraetkong@gmail.com

Created by Dara Kong

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

bl_info = {
	"name": "Fractalify",
	"author": "Dara J. Kong <daraetkong@gmail.com>",
	"version": (1, 0),
	"blender": (2, 93, 0),
	"location": "View3D > Object > Quick Effects > Fractalify",
	"description": "Iterates a pattern to create a fractal easily",
	"warning": "MAY CREATE A LOT OF GEOMETRY!",
	"doc_url": "",
	"category": "Object",
}

import bpy

from . import operator

class VIEW3D_PT_fractalify(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Fractalify"
	bl_label = "Simple Pattern"
	
	def draw(self, context):
		col = self.layout.column()
		
		col.prop(context.scene, "iterations_number")
		col.prop(context.scene, "include_source")
		
		if len(context.selected_objects) > 1:
			if context.active_object.select_get():
				props = self.layout.operator(OBJECT_OT_fractalify.bl_idname, text="Fractalify Selection", icon="PLAY")
				
				props.iterations_number = context.scene.iterations_number
				props.include_source = context.scene.include_source
			else:
				self.layout.label(text="The active object must be selected", icon="ERROR")
		elif context.selected_objects:
			self.layout.label(text="Select at least two objects", icon="ERROR")
		else:
			self.layout.label(text="No pattern selected", icon="ERROR")

def quick_effects_menu_draw(self, context):
	self.layout.operator(OBJECT_OT_fractalify.bl_idname)

def register():
	bpy.types.Scene.iterations_number = bpy.props.IntProperty(
		name = "Iterations Number",
		default = 1,
		min = 1,
		soft_max = 10
	)
	
	bpy.types.Scene.include_source = bpy.props.BoolProperty(
		name = "Include Source",
		default = True
	)
	
	bpy.utils.register_class(VIEW3D_PT_fractalify)
	bpy.types.VIEW3D_MT_object_quick_effects.append(quick_effects_menu_draw)

def unregister():
	del bpy.types.Scene.iterations_number
	del bpy.types.Scene.include_source
	
	bpy.utils.unregister_class(VIEW3D_PT_fractalify)
	bpy.types.VIEW3D_MT_object_quick_effects.remove(quick_effects_menu_draw)
