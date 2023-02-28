import maya.cmds as cmds


def color_changer(color):
    if color < 1 or color >= 32:
        cmds.error("INVALID INPUT: Color Value must be between 1 and 31")
    else:
        selection = cmds.ls(selection=True)
        shape = cmds.listRelatives(selection, shapes=True)

        for i in selection:
            cmds.setAttr(i + '.overrideEnabled', 1)
            cmds.setAttr(i + '.overrideColor', color)


color_changer(0)
