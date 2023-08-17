import maya.cmds as cmds
from custom_maya_scripts.utilities import custom_exception as util


def is_selection(_selection=cmds.ls(selection=True)):
    # if _selection is None, get the selected objects from Maya
    if not _selection:
        raise util.CustomException("No objects selected in Maya!")
    return _selection


def _is_joint(obj):
    if cmds.objectType(obj) != 'joint':
        cmds.warning(f"{obj} is not a joint.")
        return False
    return True


def filter_joints(objs=cmds.ls(selection=True)):
    joints = []
    for obj in objs:
        if _is_joint(obj):
            joints.append(obj)
    if joints is None:
        raise cmds.warning("No joints selected")
    return joints
