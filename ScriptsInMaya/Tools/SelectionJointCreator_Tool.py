import maya.cmds as cmds


def create_joints_select(data):
    """
    Creates a joint at each selection(s) transform.
    Returns: [joints]
    """
    new_joints = []

    for value in data:
        position = cmds.xform(value, query=True, rotatePivot=True, worldSpace=True)
        cmds.select(clear=True)
        jnt = cmds.joint()
        new_joints.append(jnt)
        cmds.xform(jnt, worldSpace=True, translation=position)
    cmds.select(new_joints, replace=True)
    return new_joints
