import maya.cmds as cmds

# selections = cmds.ls(sl=True)


def orient_joints(obj_selection):
    last_joint = len(obj_selection) - 1

    for index in range(len(obj_selection)):
        if index == last_joint:
            parent_orientation = cmds.joint(obj_selection[index - 1], query=True, orientation=True)
            cmds.joint(obj_selection[index], edit=True, orientation=parent_orientation)
            break
        cmds.joint(obj_selection[index], edit=True, orientJoint='xyz', secondaryAxisOrient='yup', children=True,
                   zeroScaleOrient=True)


# orient_joints(selections)
