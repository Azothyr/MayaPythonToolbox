import maya.cmds as cmds


def parent_selected(lyst):
    """
    Takes order of selected object and parents them (Last object is parent of all children,
    first is the lowest step)
    Returns: top of hierarchy selected
    """
    for value in range(len(lyst)):
        cmds.select(clear=True)
        cmds.select(lyst[value])
        if (len(lyst) - 1) > value:
            cmds.select(lyst[value + 1], add=True)
            cmds.parent()
