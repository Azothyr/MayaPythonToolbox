import maya.cmds as cmds
from utilities import selection_manager


def create_at_joint(radius):
    selected_joints = selection_check.filter_joints()
    joints_to_process = selected_joints if len(selected_joints) > 1 else cmds.ls(sl=True)[0:1]

    control_lyst = []
    for joint in joints_to_process:
        joint_name = joint
        control_name = joint_name.replace("Jnt", "Ctrl")
        group_name = joint_name.replace("Jnt", "Ctrl_Grp")

        joint_position = cmds.xform(joint, q=True, ws=True, t=True)
        joint_rotation = cmds.xform(joint, q=True, ws=True, ro=True)

        control = cmds.circle(normal=[1, 0, 0], radius=radius)[0]
        cmds.rotate(joint_rotation[0], joint_rotation[1], joint_rotation[2], control, ws=True)
        control = cmds.rename(control, control_name)

        control_lyst.append(control)

        null_group = cmds.group(empty=True)
        control_group = cmds.rename(null_group, group_name)

        cmds.parent(control, control_group)

        cmds.xform(null_group, ws=True, t=joint_position)
        cmds.xform(null_group, ws=True, ro=joint_rotation)

    return control_lyst
