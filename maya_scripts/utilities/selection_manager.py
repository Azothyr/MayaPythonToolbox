import maya.cmds as cmds
from core.components.validate_cmds.maya_exist_cmds import Exists as exists


class SelectBase:
    def __init__(self, selection=None):
        self.selection = selection if selection is not None else cmds.ls(selection=True)


class SelectAdvanced(SelectBase):
    def __init__(self, selection=None):
        super().__init__(selection)
        self.selection = None
        self.options = {
            'controls': self.filter_controls,
            'control': self.filter_controls,
            'ctrls': self.filter_controls,
            'ctrl': self.filter_controls,
            'c': self.filter_controls,
            'joints': self.filter_joints,
            'joint': self.filter_joints,
            'jnts': self.filter_joints,
            'jnt': self.filter_joints,
            'j': self.filter_joints,
        }

    def update_selection(self, _selection=None):
        if not self.selection:
            raise ValueError("No objects selected in Maya!")

    def filter_selection(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if value:
                    self.selection = self.options[key](self.selection)
        return self.selection

    @staticmethod
    def _is_joint(obj):
        if not exists.joint(obj):
            cmds.warning(f"{obj} is not a joint.")
            return False
        return True

    @staticmethod
    def _is_control(obj):
        if not exists.control(obj):
            cmds.warning(f"{obj} is not a control.")
            return False
        return True

    def filter_joints(self, objs=None):
        self.update_selection(objs)
        joints = [obj for obj in self.selection if self._is_joint(obj)]
        if not joints:
            cmds.warning("No joints selected")
        return joints

    def filter_controls(self, objs=None):
        self.update_selection(objs)
        controls = [obj for obj in self.selection if self._is_control(obj)]
        if not controls:
            cmds.warning("No controls provided.")
        return controls



class Select(SelectAdvanced):
    def __init__(self, selection=None):
        super().__init__(selection)
