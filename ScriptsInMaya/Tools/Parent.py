import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds


def parent_selected(data):
    """
    Takes order of selected object and parents them (Last object is parent of all children,
    first is the lowest step)
    Returns: top of hierarchy selected
    """
    for value in range(len(data)):
        cmds.select(clear=True)
        cmds.select(data[value])
        if (len(data) - 1) > value:
            cmds.select(data[value + 1], add=True)
            cmds.parent()
