import maya.cmds as cmds
from script_tools.components.custom_exception import CustomException


def check_selection(_selection=None, **kwargs):
    if _selection is None:
        _selection = cmds.ls(selection=True)
    options = {
        'controls': filter_controls,
        'joints': filter_joints
    }
    
    if not _selection:
        raise CustomException("No objects selected in Maya!")
    if kwargs:
        for key, value in kwargs.items():
            if value:
                _selection = options[key](_selection)
    return _selection


def _is_joint(obj):
    if cmds.objectType(obj) != 'joint':
        cmds.warning(f"{obj} is not a joint.")
        return False
    return True


def _is_control(obj):
    if cmds.objectType(obj) != 'shape':
        cmds.warning(f"{obj} is not a control.")
        return False
    return True


def filter_joints(objs=None):
    objs = check_selection(objs)

    joints = [obj for obj in objs if _is_joint(obj)]

    if not joints:
        cmds.warning("No joints selected")
    return joints


def filter_controls(objs=None):
    objs = check_selection(objs)

    controls = [obj for obj in objs if _is_control(obj)]

    if not controls:
        cmds.warning("No controls selected")
    return controls
