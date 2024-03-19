import maya.cmds as cmds
from core.components.control_cmds import Create
from core.components.validate_cmds.maya_existence import Exists
from core.components.control_cmds import check_and_fix
from core.components.xform_handler import XformHandler as xform


class ControlManager:
    def __init__(self, name: str, **kwargs):
        self.name: str = name
        self.group: str
        self.shape: str
        self.nurb: str
        self.ctrl_xform: xform
        self.group_xform: xform
        self.shape_xform: xform
        self.__match_xform: bool = kwargs.get("match", kwargs.get("mat", kwargs.get("m", False)))

        self.radius = kwargs.get("radius", 1.0)
        self.rotation_axis = kwargs.get("rotation_axis", kwargs.get("rot_axis", "z"))
        if Exists.control(name):
            cmds.warning(f"{name} already exists in the scene.")
            self.control = self
            self._already_exists_setup()
        else:
            if kwargs.get("create", False):
                self.control = self.create(name, **kwargs)
                self._doesnt_exist_setup()
        try:
            if self.group:
                self.pos = self.group_xform.get_world_space_position()
                self.rot = self.group_xform.get_world_space_rotation()
        except (AttributeError, TypeError, ValueError, RuntimeError):
            self.pos = None
            self.rot = None

    def __str__(self):
        return f"Name: {self.name!s}\nControl: {self.control!s}\nGroup: {self.group!s}\nShape: {self.shape!s}\n" \
               f"Radius: {self.radius!s}"

    def __repr__(self):
        return self.control.name

    def _already_exists_setup(self):
        self.name = check_and_fix(self.control, "_Ctrl")
        self.group = check_and_fix(self.control, "_Grp")
        if not Exists.obj(self.group):
            self.group = None
        self.shape = self._fetch_shape()
        self.nurb = self._fetch_nurb()
        if self._is_nurbs_circle():
            if self.shape:
                current_radius = self._fetch_radius()
                if current_radius != self.radius:
                    cmds.setAttr(f"{self.nurb}.radius", self.radius)
        if not self.ctrl_xform:
            self.ctrl_xform = xform(self.name)
        if not self.group_xform and self.group:
            self.group_xform = xform(self.group)

    def _doesnt_exist_setup(self):
        self.name = self.control.name
        self.group = self.control.group
        if not Exists.obj(self.group):
            self.group = None
        self.shape = self._fetch_shape()
        self.ctrl_xform = xform(self.name, allow_loc=False)
        if self.group:
            self.group_xform = xform(self.group, allow_loc=False)

        if self.__match_xform:
            if isinstance(self.__match_xform, bool):
                self.set_xform(match_obj=self.control.orig_name)
            else:
                self.set_xform(match_obj=self.__match_xform)  # noqa

    def create(self, name, **kwargs):
        kwargs["create"] = True
        self.control = Create(name, **kwargs)
        kwargs.pop("create")
        return self.control

    def _is_nurbs_circle(self):
        try:
            form = cmds.getAttr(f"{self.shape}.form")
            if form == 2:
                return True
            return False
        except (AttributeError, TypeError, ValueError):
            return False

    def _fetch_shape(self):
        """
        Fetch the shape node of the control that is a NURBS curve.
        :return: The shape node if it is a NURBS curve, None otherwise.
        """
        try:
            shapes = cmds.listRelatives(self.name, shapes=True) or []
            for shape in shapes:
                if cmds.objectType(shape) == 'nurbsCurve':
                    return shape
            self.shape = None
            return None
        except (AttributeError, TypeError, ValueError):
            self.shape = None
            return None

    def _fetch_nurb(self):
        """
        Fetch the NURBS curve of the control.
        :return: The NURBS curve if it exists, None otherwise.
        """
        if self.shape:
            if cmds.objectType(self.shape) == 'nurbsCurve':
                nurb = [node for node in cmds.listConnections(self.shape) if "circle" in node.lower()][0]
                return nurb
        self.nurb = None
        return None

    def _fetch_radius(self):
        """
        Fetch the radius attribute of the NURBS curve shape of the control.
        :return: The radius value if the shape is a NURBS curve, None otherwise.
        """
        if self.nurb:
            if 'radius' in cmds.listAttr(self.nurb):
                return cmds.getAttr(f"{self.nurb}.radius")
        return None

    def set_xform(self, match_obj: str = None, translate: tuple[float, float, float] = None,
                  rotate: tuple[float, float, float] = None):
        is_joint = cmds.objectType(match_obj) == "joint"
        print("IS JOINT: ", is_joint)

        if match_obj:
            if not isinstance(match_obj, xform):
                match_obj = xform(match_obj)
            if is_joint:
                self.group_xform.match_xform(match_obj, ["translate", "rotate"])
                self.ctrl_xform.match_xform(match_obj, ["translate", "rotate"])
                self.group_xform.add_in_local("rotate", **{self.rotation_axis: 90})
            else:
                self.group_xform.match_xform(match_obj, ["translate", "rotate"])
                self.ctrl_xform.match_xform(match_obj, ["translate", "rotate"])
        elif translate and rotate:
            translate if translate is not None else self.pos if self.pos is not None else (0, 0, 0)
            rotate if rotate is not None else self.rot if self.rot is not None else (1, 0, 0)
            self.group_xform.set_world_space_position(self.pos)
            self.group_xform.set_world_space_rotation(self.rot)
            self.ctrl_xform.set_world_space_position(self.pos)
            self.ctrl_xform.set_world_space_rotation(self.rot)


if __name__ == "__main__":
    selection = cmds.ls(sl=True)
    print(selection)

    for obj in selection:
        print(obj)
        ctrl = ControlManager(obj, radius=10, match=True, create=True)
        print(ctrl)
