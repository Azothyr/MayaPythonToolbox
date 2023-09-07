import maya.cmds as cmds
from maya_scripts.utilities import custom_exception as util


def is_selection(_selection=None):
    if _selection is None:
        _selection = cmds.ls(selection=True)

    if not _selection:
        raise util.CustomException("No objects selected in Maya!")
    return _selection


def _is_joint(obj):
    if cmds.objectType(obj) != 'joint':
        cmds.warning(f"{obj} is not a joint.")
        return False
    return True


def filter_joints(objs=None):
    if objs is None:
        objs = cmds.ls(selection=True)

    joints = [obj for obj in objs if _is_joint(obj)]

    if not joints:
        cmds.warning("No joints selected")
    return joints
