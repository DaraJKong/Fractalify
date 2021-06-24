import bpy

class OBJECT_OT_fractalify(bpy.types.Operator):
	"""Repeats the selected pattern"""
	bl_idname = "object.fractalify"
	bl_label = "Fractalify"
	bl_options = {"REGISTER", "UNDO"}
	
	iterations_number: bpy.props.IntProperty(
		name = "Iterations Number",
		description = "Number of repetitions",
		default = 1,
		min = 0,
		soft_max = 10
	)
	
	include_source: bpy.props.BoolProperty(
		name = "Include Active",
		description = "If true, the source object will be included in the pattern repetition",
		default = True
	)
	
	@classmethod
	def poll(cls, context):
		return context.area.type == "VIEW_3D"
	
	def execute(self, context):
		if len(context.selected_objects) > 1 and context.active_object.select_get():
			for i in range(self.iterations_number):
				fractalify_selection(self, context)
		else:
			return {"CANCELLED"}
		
		return {"FINISHED"}

def fractalify_selection(self, context):
	pattern = context.selected_objects
	source = context.active_object
	
	current_collection = source.users_collection[0]
	
	pattern_origin = None
	
	bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False)
	
	for obj in pattern:
		obj.select_set(False)
		
		copy = obj.copy()
		
		current_collection.objects.link(copy)
		copy.select_set(True)
		
		if obj == source:
			pattern_origin = copy
			context.view_layer.objects.active = copy
	
	bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False)
	
	if not self.include_source:
		pattern_origin.data.clear_geometry()
	
	bpy.ops.object.join()
	
	for obj in pattern:
		if obj != source:
			obj.select_set(True)
	
	bpy.ops.object.make_links_data(type="OBDATA")
	bpy.data.objects.remove(context.active_object, do_unlink=True)
	
	source.select_set(True)
	context.view_layer.objects.active = source
	
	if not self.include_source:
		source.display_type = "WIRE"
