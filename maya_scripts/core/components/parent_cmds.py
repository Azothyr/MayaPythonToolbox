import maya.cmds as cmds


def parent_selected(lyst, mode=None):
    """
    Takes order of selected object and parents them (Last object is parent of all children,
    first is the lowest step)
    Returns: top of hierarchy selected
    """
    match mode.lower():
        case "ftol":
            lyst.reverse()
        case "ltof":
            pass
        case _:
            pass

    if isinstance(lyst, str):
        lyst = [lyst]
    cmds.select(clear=True)
    for i, value in enumerate(lyst):
        cmds.select(value)
        if (len(lyst) - 1) > i:
            cmds.select(lyst[i + 1], add=True)
            cmds.parent()
    cmds.select(lyst[0])


def unparent_selected(lyst):
    """
    Takes order of selected object and un-parents them (Last object is parent of all children,
    first is the lowest step)
    Returns: top of hierarchy selected
    """
    if isinstance(lyst, str):
        lyst = [lyst]
    for obj in lyst:
        cmds.select(clear=True)
        parent = cmds.listRelatives(obj, parent=True)
        print(f'Actual Parent: {parent}')

        if parent is None:
            children = cmds.listRelatives(obj, allDescendents=True)
            cmds.parent(children, w=True)



if __name__ == "__main__":
    # unparent_selected(cmds.ls(selection=True))
    parent_selected(cmds.ls(selection=True), mode='ftol')