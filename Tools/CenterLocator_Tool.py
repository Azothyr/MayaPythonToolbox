import maya.cmds as cmds

selections = cmds.ls(sl=True)


def get_selection_center(obj_selection):
    """
    Creates a locator at each selection(s) center of mass.
    Returns: [center_location] (XYZ of the center as a tuple in a list)
    """
    center_location = []

    for selection in obj_selection:
        cluster = cmds.cluster(selection)
        center = cmds.xform(cluster, query=True, rotatePivot=True, worldSpace=True)
        cmds.delete(cluster)
        center_location.append(center)
    return center_location


get_selection_center(selections)
