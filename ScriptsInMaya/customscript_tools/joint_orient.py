import maya.cmds as cmds


def orient_joints(jnt_lyst):
    last_joint = len(jnt_lyst) - 1

    for index in range(len(jnt_lyst)):
        if index == last_joint:
            parent_orientation = cmds.joint(jnt_lyst[index - 1], query=True, orientation=True)
            cmds.joint(jnt_lyst[index], edit=True, orientation=parent_orientation)
            break
        cmds.joint(jnt_lyst[index], edit=True, orientJoint='xyz', secondaryAxisOrient='yup', children=True,
                   zeroScaleOrient=True)
