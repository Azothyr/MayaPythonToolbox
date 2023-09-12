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
    cmds.select(lyst[0])


def unparent_selected(lyst):
    """
    Takes order of selected object and un-parents them (Last object is parent of all children,
    first is the lowest step)
    Returns: top of hierarchy selected
    """
    for obj in lyst:
        cmds.select(clear=True)
        parent = cmds.listRelatives(obj, parent=True)
        print(f'Actual Parent: {parent}')

        if parent is None:
            children = cmds.listRelatives(obj, allDescendents=True)
            cmds.parent(children, w=True)
