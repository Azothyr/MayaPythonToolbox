import maya.cmds as cmds
# selection = cmds.ls(sl=True)


def parent_selected(obj_selection):
    """
    Takes order of selected object and parents them (Last object is parent of all children,
    first is the lowest step)
    Returns: top of hierarchy selected
    """
    for selection in range(len(obj_selection)):
        cmds.select(clear=True)
        cmds.select(obj_selection[selection])
        if (len(obj_selection) - 1) > selection:
            cmds.select(obj_selection[selection + 1], add=True)
            cmds.parent()

# parent_selected(selection)