import maya.cmds as cmds


def create_joint_control():
    selection = cmds.ls(selection=True, type="joint")
    if not selection:
        cmds.warning("Please select a joint.")
        return
    joint_name = selection[0]

    joint_position = cmds.xform(joint_name, query=True, worldSpace=True, translation=True)
    joint_rotation = cmds.xform(joint_name, query=True, worldSpace=True, rotation=True)

    circle_ctrl = cmds.circle(name=joint_name.replace("Jnt", "Ctrl"))[0]

    null_grp = cmds.group(empty=True, name=joint_name.replace("Jnt", "Ctrl_Grp"))

    cmds.parent(circle_ctrl, null_grp)

    cmds.xform(null_grp, worldSpace=True, translation=joint_position)
    cmds.xform(null_grp, worldSpace=True, rotation=joint_rotation)
