import maya.cmds as cmds
from core.components.validate_cmds import exists_maya as exists
from utilities.kwarg_option_menu import Menu


class SelectBase:
    def __init__(self, selection: list[str] = None, default: str = "none"):
        if default == "none":
            default = []
        self.selection = selection if selection is not None else\
            cmds.ls(selection=True) if cmds.ls(selection=True) else default

    def __str__(self):
        if self.selection is None:
            self.selection = []
        return f"{self.selection!s}"

    def __repr__(self):
        if self.selection is None:
            self.selection = []
        return f"{self.__class__.__name__}(SELECTION: {self.selection!r})"


class SelectAdvanced(SelectBase):
    def __init__(self, selection=None, **kwargs):
        super().__init__(selection, **kwargs)
        self.options = Menu({
            'controls': (['control', 'ctrls', 'ctrl', 'c'], self._filter_controls),
            "joints": (['joint', 'jnts', 'jnt', 'j'], self._filter_joints)})

    def update_selection(self, _selection=None):
        if not self.selection:
            raise ValueError("No objects selected in Maya!")

    def filter_selection(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if value:
                    self.selection = self.options(key, self.selection)
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

    def _filter_joints(self, objs=None):
        self.update_selection(objs)
        joints = [obj for obj in self.selection if self._is_joint(obj)]
        if not joints:
            cmds.warning("No joints selected")
        return joints

    def _filter_controls(self, objs=None):
        self.update_selection(objs)
        controls = [obj for obj in self.selection if self._is_control(obj)]
        if not controls:
            cmds.warning("No controls provided.")
        return controls


class Select(SelectAdvanced):
    def __init__(self, selection=None, **kwargs):
        super().__init__(selection, **kwargs)


if __name__ == "__main__":
    # selection = Select()
    # print(selection)
    # print(selection.__repr__())
    selection = Select().filter_selection(joints=True)
    print(selection)
    # selection = Select().filter_selection(controls=True)
    # print(selection)
    # selection = Select().filter_selection(joints=True, controls=True)
    # print(selection)
    # selection = Select().filter_selection()
    # print(selection)
