import maya.cmds as cmds


def create_joints():
    """
    Creates a joint at each selection(s) transform.
    Returns: [joints]
    """
    selections = cmds.ls(select=True)
    new_joints = []

    for selection in selections:
        position = cmds.xform(selection, query=True, translation=True, worldSpace=True)
        cmds.select(clear=True)

        jnt = cmds.joint()
        new_joints.append(jnt)
        cmds.xform(jnt, worldSpace=True, translation=position)

    cmds.select(new_joints, replace=True)

    return new_joints


create_joints()
