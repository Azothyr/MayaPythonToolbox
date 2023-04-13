import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds

selections = cmds.ls(sl=True)
positions = []

for selection in selections:
    position = cmds.xform(selection, query=True, rotatePivot=True, worldSpace=True)
    cmds.select(clear=True)
    positions.append(position)

cmds.distanceDimension(sp=(positions[0]), ep=(positions[1]))
