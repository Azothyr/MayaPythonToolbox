import maya.cmds as cmds


def create_joints_xyz(xyz_lyst):
    """
    Creates a joint at each XYZ value from a list.
    Returns: [joints]
    """
    new_joints = []

    if not cmds.objExists('Jnt_layer'):
        cmds.createDisplayLayer(name='Jnt_layer', number=1)

    joint_orient_attrs = ['jointOrientX', 'jointOrientY', 'jointOrientZ', 'displayLocalAxis']
    for xyz in xyz_lyst:
        center_position = xyz
        cmds.select(clear=True)
        jnt = cmds.joint()
        new_joints.append(jnt)
        for attr_name in joint_orient_attrs:
            cmds.setAttr(f"{jnt}.{attr_name}", keyable=False, channelBox=True)
        cmds.xform(jnt, worldSpace=True, translation=center_position)
        cmds.editDisplayLayerMembers('Jnt_layer', jnt)
    cmds.select(new_joints, replace=True)
    return new_joints