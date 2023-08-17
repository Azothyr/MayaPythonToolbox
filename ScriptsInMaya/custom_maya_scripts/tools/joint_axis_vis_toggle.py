import maya.cmds as cmds
from custom_maya_scripts.utilities import selection_check


def toggle_visibility(*args):
    selection = selection_check.filter_joints()

    for joint_name in selection:
        display_local_axis = cmds.getAttr(joint_name + ".displayLocalAxis")
        cmds.setAttr(joint_name + ".displayLocalAxis", not display_local_axis)
