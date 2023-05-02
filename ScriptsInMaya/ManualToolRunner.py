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

import maya.cmds as cmds

selected_obj = cmds.ls(selection=True)[0]

# Keyframe 1
cmds.currentTime(0)
cmds.setAttr(selected_obj + '.rz', 35)
cmds.setKeyframe(selected_obj)

# Keyframe 2
cmds.currentTime(15)
cmds.setAttr(selected_obj + '.rz', -35)
cmds.setKeyframe(selected_obj)

# Keyframe 3
cmds.currentTime(30)
cmds.setAttr(selected_obj + '.rz', 0)
cmds.setKeyframe(selected_obj)

# Keyframe 4
cmds.currentTime(45)
cmds.setAttr(selected_obj + '.ry', 35)
cmds.setKeyframe(selected_obj)

# Keyframe 5
cmds.currentTime(60)
cmds.setAttr(selected_obj + '.ry', -35)
cmds.setKeyframe(selected_obj)

# Keyframe 6
cmds.currentTime(75)
cmds.setAttr(selected_obj + '.ry', 0)
cmds.setKeyframe(selected_obj)

# Keyframe 7
cmds.currentTime(90)
cmds.setAttr(selected_obj + '.tx', 2)
cmds.setKeyframe(selected_obj)

# Keyframe 8
cmds.currentTime(105)
cmds.setKeyframe(selected_obj)

cmds.currentTime(0)
