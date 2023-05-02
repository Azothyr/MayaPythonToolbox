import maya.cmds as cmds

selected_obj = cmds.ls(selection=True)[0]

cmds.currentTime(0)
# Get a list of all the attributes for the selected object
attrs = cmds.listAttr(selected_obj)

# For each attribute, check if it has keyframes and remove them if it does
for attr in attrs:
    # Use getAttr to check if the attribute has keyframes
    if cmds.keyframe(selected_obj, attribute=attr, query=True):
        cmds.cutKey(selected_obj, attribute=attr)

# Set all movement attributes to their default values
cmds.setAttr(selected_obj + '.translate', 0, 0, 0)
cmds.setAttr(selected_obj + '.rotate', 0, 0, 0)
cmds.setAttr(selected_obj + '.scale', 1, 1, 1)