import maya.cmds as cmds


def orient_joints(jnt_lyst, oreint=None, secondary_axis=None):

    for jnt in jnt_lyst:
        cmds.joint(jnt, edit=True, orientJoint='xyz', secondaryAxisOrient='yup', children=True,
                   zeroScaleOrient=True)
        if cmds.listRelatives(jnt, children=True) is None:
            cmds.setAttr(f"{jnt}.jointOrientX", 0)
            cmds.setAttr(f"{jnt}.jointOrientY", 0)
            cmds.setAttr(f"{jnt}.jointOrientZ", 0)


if __name__ == "__main__":
    orient_joints(cmds.ls(selection=True, type='joint'))
