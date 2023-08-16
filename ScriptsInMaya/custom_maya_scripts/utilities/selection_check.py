import maya.cmds as cmds
from 


def check_selection(_selection=None):
    # if _selection is None, get the selected objects from Maya
    if _selection is None:
        _selection = cmds.ls(selection=True)
        if not _selection:
            raise util.CustomException("No objects selected in Maya!")
    return _selection
