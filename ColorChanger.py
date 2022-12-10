import maya.cmds as cmds


def ColorChanger(color):
    if color < 1 or color >= 32:
        cmds.error("INVALID INPUT: Color Value must be between 1 and 31")
    else:
        objSelected = cmds.ls(selection=True)
        shape = cmds.listRelatives(objSelected, shapes=True)

        for object in objSelected:
            cmds.setAttr(object + '.overrideEnabled', 1)
            cmds.setAttr(object + '.overrideColor', color)


ColorChanger(0)