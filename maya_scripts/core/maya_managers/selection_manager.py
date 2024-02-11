import maya.cmds as cmds
import re
from core.components.validate_cmds import exists_maya as exists
from utilities.kwarg_option_menu import Menu


class SelectBase:
    def __init__(self, selection: list[str] = None, bypass=False, debug=False):
        if selection is not None:
            self.selection = selection
        else:
            self.selection = cmds.ls(sl=True) or [] if not bypass else cmds.ls()
        self.debug = debug

    def __str__(self):
        return f"{self.__class__.__name__}(SELECTION: {str(self.selection)})"

    def __repr__(self):
        return self.selection

    def __iter__(self):
        return iter(self.selection)

    def __len__(self):
        return len(self.selection)

    def __getitem__(self, item):
        return self.selection[item]

    def __setitem__(self, key, value):
        self.selection[key] = value

    def __delitem__(self, key):
        del self.selection[key]

    def __contains__(self, item):
        return item in self.selection

    @staticmethod
    def _get_all_objects():
        return cmds.ls()


class SelectAdvanced(SelectBase):
    def __init__(self, selection=None, **kwargs):
        super().__init__(selection, **kwargs)
        self.options = Menu({
            "joints": (["joint", "jnts", "jnt", "j"], self._filter_to_joints),
            "controls": (["control", "ctrls", "ctrl", "c"], self._filter_to_controls),
            "shapes": (["shape", "shp", "shps"], self._filter_to_shapes),
            "groups": (["group", "grp", "grps"], self._filter_to_groups),
            "maya_object": (["maya_obj", "maya_objects", "maya_objs"], self._filter_to_maya_objects),
        })

    def __call__(self, *args, **kwargs):
        return self.filter_selection(**kwargs)

    def update_selection(self, _selection=None):
        if not self.selection:
            raise ValueError("No objects selected in Maya!")
        if _selection is not None:
            self.selection = _selection
        elif not self.selection:
            raise ValueError("No objects selected in Maya!")

    def filter_selection(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if value:
                    if isinstance(value, list):
                        self.selection = self.options(key, value)
                    else:
                        self.selection = self.options(key, self.selection)
        return self.selection

    def get(self):
        return self.selection

    @staticmethod
    def _get_shapes(obj):
        return cmds.listRelatives(obj, shapes=True)

    def _is_joint(self, obj):
        if not exists.joint(obj):
            if self.debug:
                cmds.warning(f"{obj} is not a joint.")
            return False
        return True

    def _is_control(self, obj):
        if not exists.control(obj):
            if self.debug:
                cmds.warning(f"{obj} is not a control.")
            return False
        return True

    def _is_shape(self, obj):
        if not exists.shape(obj):
            if self.debug:
                cmds.warning(f"{obj} is not a shape.")
            return False
        return True

    def _is_group(self, obj):
        if not exists.group(obj):
            if self.debug:
                cmds.warning(f"{obj} is not a group.")
            return False
        return True

    def _filter_to_joints(self, objs=None):
        self.update_selection(objs)
        joints = [obj for obj in self.selection if self._is_joint(obj)]
        if not joints:
            cmds.warning("No joints selected")
        return joints

    def _filter_to_controls(self, objs=None):
        self.update_selection(objs)
        controls = [obj for obj in self.selection if self._is_control(obj)]
        if not controls:
            cmds.warning("No controls provided.")
        return controls

    def _filter_to_shapes(self, objs=None):
        self.update_selection(objs)
        controls = [obj for obj in self.selection if self._is_shape(obj)]
        if not controls:
            cmds.warning("No controls provided.")
        return controls

    def filter_to_shapes_from_base_object(self, objs=None):
        self.update_selection(objs)
        shapes = []
        for obj in self.selection:
            shape = self._get_shapes(obj)
            if shape:
                if isinstance(shape, list):
                    if len(shape) > 1:
                        cmds.warning(f"More than one shape found for {obj}: {shape}")
                    shape = shape[0]
                if self._is_shape(shape):
                    shapes.append(shape)
        if not shapes:
            cmds.warning("No shapes found.")
        return shapes

    def _filter_to_groups(self, objs=None):
        self.update_selection(objs)
        controls = [obj for obj in self.selection if self._is_group(obj)]
        if not controls:
            cmds.warning("No controls provided.")
        return controls

    def _filter_to_maya_objects(self, patterns):
        self.update_selection(self._get_all_objects())
        result = []
        for obj in self.selection:
            for pattern in patterns:
                if re.search(pattern, obj, re.IGNORECASE):
                    result.append(obj)
        return result


class Select(SelectAdvanced):
    def __init__(self, selection=None, **kwargs):
        super().__init__(selection, **kwargs)


if __name__ == "__main__":
    selection = Select(bypass=True)
    # print(selection)
    # selection = selection.filter_selection(joints=True)
    # print("\n".join(selection))

    print(selection.filter_selection(maya_object=["transform_ctrl$"]))

    # print(selection.__repr__())
    # selection = Select().filter_selection(joints=True)
    # print(selection)
    # selection = Select().filter_selection(controls=True)
    # print(selection)
    # selection = Select().filter_selection(joints=True, controls=True)
    # print(selection)
    # selection = Select().filter_selection()
    # print(selection)
