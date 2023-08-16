"""
Tools to get the center of a single or list of objects selected in Maya.
Select the objects you want to get the center for and provide them as an argument to get_obj_center, and it
will determine the centers.
"""
import maya.cmds as cmds


def _calculate_center(obj):
    """
    :param obj: Object name in Maya
    :return: center xyz of provided obj
    """
    if cmds.objectType(obj) == 'joint':
        obj_center = cmds.xform(obj, q=True, ws=True, t=True)
    else:
        bbox = cmds.exactWorldBoundingBox(obj)
        obj_center = (
            (bbox[0] + bbox[3]) / 2,
            (bbox[1] + bbox[4]) / 2,
            (bbox[2] + bbox[5]) / 2
        )
    return obj_center


def _get_selection_centers(obj_lyst):
    """
    :param obj_lyst:
    :return: a list of xyz values
    """
    centers_lyst = []
    for obj in obj_lyst:
        centers_lyst.append(_calculate_center(obj))
    return centers_lyst


def get_obj_center(_input=None):
    """
    finds the selection(s) center of mass.
    Returns: (center x, center y, center z)
    """
    # if _input is None, get the selected objects from Maya
    if _input is None:
        _input = cmds.ls(selection=True)
        if not _input:
            raise ValueError("No objects selected in Maya!")

    # Check if _input is a list or a single object
    if isinstance(_input, list):
        return _get_selection_centers(_input)
    elif isinstance(_input, str):  # Maya object names are typically strings
        return _calculate_center(_input)
    else:
        raise ValueError("input must be a selected object or a list of selected objects.")
