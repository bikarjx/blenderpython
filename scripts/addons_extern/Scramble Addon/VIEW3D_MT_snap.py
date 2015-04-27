# 3Dビュー > Shift+S

import bpy

################
# オペレーター #
################

class SnapMesh3DCursor(bpy.types.Operator):
	bl_idname = "view3d.snap_mesh_3d_cursor"
	bl_label = "Snap the 3D cursor to mesh"
	bl_description = "On the mesh surface under the mouse to move the cursor 3D (please use registered in the shortcut)"
	bl_options = {'REGISTER'}
	
	mouse_co = bpy.props.IntVectorProperty(name="Mouse position", size=2)
	
	def execute(self, context):
		preGp = context.scene.grease_pencil
		preGpSource = context.scene.tool_settings.grease_pencil_source
		context.scene.tool_settings.grease_pencil_source = 'SCENE'
		if (preGp):
			tempGp = preGp
		else:
			try:
				tempGp = bpy.data.grease_pencil["temp"]
			except KeyError:
				tempGp = bpy.data.grease_pencil.new("temp")
		context.scene.grease_pencil = tempGp
		tempLayer = tempGp.layers.new("temp", set_active=True)
		tempGp.draw_mode = 'SURFACE'
		bpy.ops.gpencil.draw(mode='DRAW_POLY', stroke=[{"name":"", "pen_flip":False, "is_start":True, "location":(0, 0, 0),"mouse":self.mouse_co, "pressure":1, "time":0, "size":0}, {"name":"", "pen_flip":False, "is_start":True, "location":(0, 0, 0),"mouse":(0, 0), "pressure":1, "time":0, "size":0}])
		bpy.context.space_data.cursor_location = tempLayer.frames[-1].strokes[-1].points[0].co
		tempGp.layers.remove(tempLayer)
		context.scene.grease_pencil = preGp
		context.scene.tool_settings.grease_pencil_source = preGpSource
		return {'FINISHED'}
	def invoke(self, context, event):
		self.mouse_co[0] = event.mouse_region_x
		self.mouse_co[1] = event.mouse_region_y
		return self.execute(context)

class Move3DCursorToViewLocation(bpy.types.Operator):
	bl_idname = "view3d.move_3d_cursor_to_view_location"
	bl_label = "The 3D cursor moves to the viewpoint position"
	bl_description = "I will move the 3D cursor to the center position of the viewpoint"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		bpy.context.space_data.cursor_location = context.region_data.view_location[:]
		return {'FINISHED'}

class Move3DCursorFar(bpy.types.Operator):
	bl_idname = "view3d.move_3d_cursor_far"
	bl_label = "To hide the 3D cursor (far far) to be"
	bl_description = "You look like hidden can be moved to far away the 3D cursor"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		bpy.context.space_data.cursor_location = (24210, 102260, 38750)
		return {'FINISHED'}

################
# メニュー追加 #
################

# メニューのオン/オフの判定
def IsMenuEnable(self_id):
	for id in bpy.context.user_preferences.addons["Scramble Addon"].preferences.disabled_menu.split(','):
		if (id == self_id):
			return False
	else:
		return True

# メニューを登録する関数
def menu(self, context):
	if (IsMenuEnable(__name__.split('.')[-1])):
		self.layout.separator()
		self.layout.operator(Move3DCursorToViewLocation.bl_idname, text="Cursor to viewpoint position", icon="PLUGIN")
		self.layout.operator(Move3DCursorFar.bl_idname, text="Cursor = hide (to far)", icon="PLUGIN")
		self.layout.operator(SnapMesh3DCursor.bl_idname, text="Cursor to mesh surface", icon="PLUGIN")
	if (context.user_preferences.addons["Scramble Addon"].preferences.use_disabled_menu):
		self.layout.separator()
		self.layout.operator('wm.toggle_menu_enable', icon='CANCEL').id = __name__.split('.')[-1]
