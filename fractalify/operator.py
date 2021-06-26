import bpy
import mathutils

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
		description = "If true, the source object will be included in the pattern repetition. Only the last iteration will be shown when false.",
		default = True
	)
	
	hide_source: bpy.props.BoolProperty(
		name = "Hide Source",
		description = "Hides the source object in the viewport when it's excluded",
		default = True
	)
	
	separate_objects: bpy.props.BoolProperty(
		name = "Separate Objects",
		description = "Creates individual objects instead of modifying the geometry of the pattern",
		default = True
	)
	
	@classmethod
	def poll(cls, context):
		return context.area.type == "VIEW_3D"
	
	def execute(self, context):
		if len(context.selected_objects) > 1 and context.active_object.select_get():
			if self.separate_objects:
				fractalify_simple_separate(self, context)
			else:
				for i in range(self.iterations_number):
					fractalify_simple(self, context)
			
			if (not self.include_source) and self.hide_source:
				context.view_layer.objects.active.display_type = "WIRE"
		else:
			return {"CANCELLED"}
		
		return {"FINISHED"}

def fractalify_simple(self, context):
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

def fractalify_simple_separate(self, context):
	source = context.active_object
	pattern = [obj for obj in context.selected_objects if not obj == source]
	
	current_collection = source.users_collection[0]
	
	step_collections = []
	offsets = []
	
	# Make sure all the objects in the pattern share the same data
	bpy.ops.object.make_links_data(type="OBDATA")
	
	source_matrix = mathutils.Matrix(source.matrix_basis)
	source_matrix_inverted = source_matrix.inverted()
	
	# Calculate all the matrices for the offsets
	for object in pattern:
		offsets.append(source_matrix_inverted @ object.matrix_basis)
	
	# Create a collection for each iteration
	for i in range(self.iterations_number + 1):
		step_collections.append(
			bpy.data.collections.new("iteration " + str(i))
		)
		
		# Only show the last iteration if 
		if self.include_source or i == self.iterations_number:
			current_collection.children.link(step_collections[i])
	
	# Move the objects of the pattern in the first collection and deselect them
	for object in pattern:
		object.users_collection[0].objects.unlink(object)
		step_collections[0].objects.link(object)
		
		object.select_set(False)
	
	# Create all the copies recursively
	for i in range(self.iterations_number):
		for object in step_collections[i].objects:
			for offset in offsets:
				copy = object.copy()
				
				copy.matrix_basis @= offset
				
				step_collections[i + 1].objects.link(copy)
