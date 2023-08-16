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
        # cmds.editDisplayLayerMembers('Jnt_layer', jnt)
    cmds.select(new_joints, replace=True)
    return new_joints
