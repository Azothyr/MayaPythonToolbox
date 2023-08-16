import maya.cmds as cmds


def create_joints_xyz(xyz_list, radius_input=None):
    """
    Creates a joint at each XYZ value from a list.
    Returns: [joints]
    """
    new_joints = []

    joint_orient_attrs = ['jointOrientX', 'jointOrientY', 'jointOrientZ', 'displayLocalAxis']
    for xyz in xyz_list:
        center_position = xyz
        cmds.select(clear=True)
        if radius_input is not None:
            jnt = cmds.joint(rad=radius_input)
        else:
            jnt = cmds.joint(rad=1)
        new_joints.append(jnt)
        for attr_name in joint_orient_attrs:
            cmds.setAttr(f"{jnt}.{attr_name}", keyable=False, channelBox=True)
        cmds.xform(jnt, worldSpace=True, translation=center_position)
    cmds.select(new_joints, replace=True)
    return new_joints


def create_joints_selection(lyst):
    """
    Creates a joint at each selection(s) transform.
    Returns: [joints]
    """
    new_joints = []

    for value in lyst:
        position = cmds.xform(value, query=True, rotatePivot=True, worldSpace=True)
        cmds.select(clear=True)
        jnt = cmds.joint()
        new_joints.append(jnt)
        cmds.xform(jnt, worldSpace=True, translation=position)
    cmds.select(new_joints, replace=True)
    return new_joints
