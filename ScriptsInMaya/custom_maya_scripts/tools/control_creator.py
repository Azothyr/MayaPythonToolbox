import maya.cmds as cmds
from custom_maya_scripts.utilities import selection_check


def create_at_joint(radius):
    selected_joints = selection_check.filter_joints()
    joints_to_process = selected_joints if len(selected_joints) > 1 else cmds.ls(sl=True)[0:1]

    control_lyst = []
    for joint in joints_to_process:
        joint_position = cmds.xform(joint, q=True, ws=True, t=True)
        joint_rotation = cmds.xform(joint, q=True, ws=True, ro=True)
        circle = cmds.circle(nr=[1, 0, 0], r=radius)[0]

        circle_rename = joint.replace("Jnt", "Ctrl")
        circle = cmds.rename(circle, circle_rename)

        control_lyst.append(circle)

        null_group = cmds.group(em=True)
        null_group_rename = joint.replace("Jnt", "Ctrl_Grp")
        null_group = cmds.rename(null_group, null_group_rename)

        cmds.parent(circle, null_group)

        cmds.xform(null_group, ws=True, t=joint_position)
        cmds.xform(null_group, ws=True, ro=joint_rotation)

    return control_lyst
