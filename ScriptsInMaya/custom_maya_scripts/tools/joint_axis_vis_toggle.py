import maya.cmds as cmds


def toggle_visibility(*args):
    selection = cmds.ls(selection=True, type="joint")

    for joint_name in selection:
        display_local_axis = cmds.getAttr(joint_name + ".displayLocalAxis")
        cmds.setAttr(joint_name + ".displayLocalAxis", not display_local_axis)
