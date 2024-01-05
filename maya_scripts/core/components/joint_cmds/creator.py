import maya.cmds as cmds


def create_joints_xyz(xyz_list, radius=None, parent=None):
    """
    Creates a joint at each XYZ value from a list.
    Returns: [joints]
    """
    new_joints = []

    joint_orient_attrs = ['jointOrientX', 'jointOrientY', 'jointOrientZ', 'displayLocalAxis']
    cmds.select(clear=True)
    for position in xyz_list:
        if not parent:
            cmds.select(clear=True)
        if radius is None:
            radius = 1
        jnt = cmds.joint(rad=radius)
        new_joints.append(jnt)
        for attr_name in joint_orient_attrs:
            cmds.setAttr(f"{jnt}.{attr_name}", keyable=False, channelBox=True)
        cmds.xform(jnt, worldSpace=True, translation=position)
    cmds.select(new_joints, replace=True)
    return new_joints
