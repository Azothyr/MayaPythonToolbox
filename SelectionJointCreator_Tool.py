import maya.cmds as cmds

selections = cmds.ls(sl=True)


def create_joints_select(obj_selection):
    """
    Creates a joint at each selection(s) transform.
    Returns: [joints]
    """
    new_joints = []

    for selection in obj_selection:
        position = cmds.xform(selection, query=True, rotatePivot=True, worldSpace=True)
        cmds.select(clear=True)
        jnt = cmds.joint()
        new_joints.append(jnt)
        cmds.xform(jnt, worldSpace=True, translation=position)
    cmds.select(new_joints, replace=True)
    return new_joints


create_joints_select(selections)
