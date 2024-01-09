from core.components.control_cmds import Create as cr
from core.components.validate_cmds.maya_existence import Exists as exists
from core.components.control_cmds import check_and_fix as control_name
from core.components.xform_handler import XformHandler as xform


class ControlManager:
    def __init__(self, name: str, **kwargs):
        self.name = None
        self.control = None
        self.group = None
        self.shape = None
        self.ctrl_xform = None
        self.group_xform = None
        self.shape_xform = None
        self.radius = kwargs.get("radius", 1.0)
        self.pos = None
        self.rot = None
        self.exists = False

        if exists.control(name):
            self.__setup(name, **kwargs)
        else:
            self.create(name, **kwargs)

    def __setup(self, name: str, **kwargs):
        self.exists = True
        self.name = control_name(name)
        self.control = self.name
        self.group = control_name(name, "_Ctrl_Grp")
        self.shape = control_name(name, "_CtrlShape")
        self.ctrl_xform = xform(self.control)
        self.group_xform = xform(self.group)
        self.shape_xform = xform(self.shape)
        self.pos = self.group_xform.get_world_space_position()
        self.rot = self.group_xform.get_world_space_rotation()

    def get_control_and_group(self):
        return self.control, self.group

    def create(self, *args, **kwargs):
        if not kwargs.get("create", False):
            kwargs["create"] = True

        return cr(self.name, self.radius, **kwargs)

    def set_xform(self, match_obj: str = None, translate: tuple[float, float, float] = None,
                  rotate: tuple[float, float, float] = None):
        if match_obj:
            self.group_xform.match_xform(match_obj, ["translate", "rotate"])
            self.ctrl_xform.match_xform(match_obj, ["translate", "rotate"])
        elif translate and rotate:
            translate if translate is not None else self.pos if self.pos is not None else (0, 0, 0)
            rotate if rotate is not None else self.rot if self.rot is not None else (1, 0, 0)
            self.group_xform.set_world_space_position(self.pos)
            self.group_xform.set_world_space_rotation(self.rot)
            self.ctrl_xform.set_world_space_position(self.pos)
            self.ctrl_xform.set_world_space_rotation(self.rot)

