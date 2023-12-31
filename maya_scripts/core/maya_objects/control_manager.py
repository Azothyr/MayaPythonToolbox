import maya.cmds as cmds
from core.components.validate_cmds.maya_exist_cmds import Exists as exists


class Control:
    def __init__(self, name: str = None):
        self.control, self.shape, self.group = self._split_to_control_and_group(name)

    @staticmethod
    def _fetch_control(obj):
        if "shape" in obj.lower():
            return cmds.listRelatives(obj, parent=True, type="transform")[0]
        if exists.control(obj):
            return obj
        return obj


    def _split_to_control_and_group(self, obj):
        if not exists.control(obj):
            raise ValueError(
                f"ERROR: Incorrect object type for {obj}. Expected 'transform', got {cmds.objectType(obj)}.")

        if obj.lower().endswith("_ctrl"):
            return obj, cmds.listRelatives(obj, shapes=True, type="nurbsCurve")[0], \
                   cmds.listRelatives(obj, parent=True, type="transform")[0]
        elif obj.lower().endswith("_grp"):
            return cmds.listRelatives(obj, children=True, type="nurbsCurve")[0], \
                   cmds.listRelatives(obj, shapes=True, type="nurbsCurve")[0], obj
        elif obj.lower().endswith("Shape"):
            return cmds.listRelatives(obj, parent=True, type="transform")[0], obj, \
                   cmds.listRelatives(obj, parent=True, type="transform")[0]

        raise ValueError(f"ERROR: {obj} does not end with '_Ctrl' or '_Grp'.")
