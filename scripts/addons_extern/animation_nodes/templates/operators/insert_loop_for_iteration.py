import bpy
from bpy.props import *
from mathutils import Vector
from ... sockets.info import isList
from ... base_types.template import Template
from ... tree_info import getNodeByIdentifier


class InsertLoopForIteration(bpy.types.Operator, Template):
    bl_idname = "an.insert_loop_for_iteration_template"
    bl_label = "Insert Loop for Iteration"

    nodeIdentifier = StringProperty()
    socketIndex = IntProperty()

    def insert(self):
        try:
            sourceNode = getNodeByIdentifier(self.nodeIdentifier)
            socket = sourceNode.outputs[self.socketIndex]
        except:
            return
        if not isList(socket.bl_idname):
            return

        loopInputNode = self.newNode("an_LoopInputNode")
        loopInputNode.newIterator(socket.dataType)
        invokeNode = self.newNode("an_InvokeSubprogramNode", x=200, move=False, mouseOffset=False)
        invokeNode.location = sourceNode.location + Vector((250, 0))

        invokeNode.subprogramIdentifier = loopInputNode.identifier
        self.updateSubprograms()

        socket.linkWith(invokeNode.inputs[0])
