"""
Tools to get the center of a single or list of objects selected in Maya.
Select the objects you want to get the center for and provide them as an argument to get_obj_center, and it
will determine the centers.
"""
import maya.cmds as cmds
import ast


def _calculate_object_center(obj):
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


def _average_centers(obj_lyst):
    """
    :param obj_lyst:
    :return: a single average xyz value for all the provided objects
    """
    total_x, total_y, total_z = 0, 0, 0
    num_objs = len(obj_lyst)

    for obj in obj_lyst:
        total_x += obj[0]
        total_y += obj[1]
        total_z += obj[2]

    return [total_x / num_objs, total_y / num_objs, total_z / num_objs]


def _get_selection_centers(obj_lyst):
    """
    :param obj_lyst:
    :return: a list of xyz values
    """
    centers_lyst = []
    for obj in obj_lyst:
        centers_lyst.append(_calculate_object_center(obj))
    center = _average_centers(centers_lyst)
    return center


def get_center(_input=None):
    """
    finds the selection(s) center of mass.
    Returns: (center x, center y, center z)
    """
    # Check if the input is a string representation of a list
    if isinstance(_input, str) and _input.startswith('[') and _input.endswith(']'):
        try:
            _input = ast.literal_eval(_input)
        except (ValueError, SyntaxError):
            pass

    # Check if _input is a list or a single object
    if isinstance(_input, list):
        return _get_selection_centers(_input)
    elif isinstance(_input, str):
        return _calculate_object_center(_input)
    else:
        cmds.warning("input must be a selected object or a list of selected objects.")
        return
