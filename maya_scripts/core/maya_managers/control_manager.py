import maya.cmds as cmds
from core.components.control_cmds import Create
from core.components.validate_cmds.maya_existence import Exists
from core.components.control_cmds import check_and_fix
from core.components.xform_handler import XformHandler as xform


class ControlManager:
    def __init__(self, name: str, **kwargs):
        self.name: str
        self.group: str
        self.shape: str
        self.nurb: str
        self.ctrl_xform: xform
        self.group_xform: xform
        self.shape_xform: xform
        self.__match_xform: bool = kwargs.get("match", kwargs.get("mat", kwargs.get("m", False)))
        self.name = name

        self.radius = kwargs.get("radius", 1.0)
        self.rotation_axis = kwargs.get("rotation_axis", kwargs.get("rot_axis", "z"))
        if Exists.control(name):
            print(f"{name} already exists in the scene.")
            self.control = name
            self._already_exists_setup()
        else:
            self.control = self.create(name, **kwargs)
            if Exists.control(self.control.name):
                self._doesnt_exist_setup()
            else:
                raise ValueError(name, " does not exist in the scene.".upper())

        self.pos = self.group_xform.get_world_space_position()
        self.rot = self.group_xform.get_world_space_rotation()

    def __str__(self):
        return f"Name: {self.name!s}\nControl: {self.control!s}\nGroup: {self.group!s}\nShape: {self.shape!s}\n" \
               f"Radius: {self.radius!s}"

    def __repr__(self):
        return self.control

    def get_control_and_group(self):
        return self.control, self.group

    def _already_exists_setup(self):
        self.name = check_and_fix(self.control, "_Ctrl")
        self.group = check_and_fix(self.control, "_Grp")
        self.shape = self._fetch_shape()
        self.nurb = self._fetch_nurb()
        if self._is_nurbs_circle():
            current_radius = self._fetch_radius()
            if current_radius != self.radius:
                cmds.setAttr(f"{self.nurb}.radius", self.radius)
        self.ctrl_xform = xform(self.name)
        self.group_xform = xform(self.group)
        self.shape_xform = xform(self.shape)

    def _doesnt_exist_setup(self):
        self.name = self.control.name
        self.group = self.control.group
        self.shape = self._fetch_shape()
        self.ctrl_xform = xform(self.name)
        self.group_xform = xform(self.group)
        self.shape_xform = xform(self.shape)

        if self.__match_xform:
            self.set_xform(match_obj=self.control.orig_name)

    def create(self, name, **kwargs):
        kwargs["create"] = True
        self.control = Create(name, **kwargs)
        kwargs.pop("create")
        return self.control

    def _is_nurbs_circle(self):
        form = cmds.getAttr(f"{self.shape}.form")
        if form == 2:
            return True
        return False

    def _fetch_shape(self):
        """
        Fetch the shape node of the control that is a NURBS curve.
        :return: The shape node if it is a NURBS curve, None otherwise.
        """
        shapes = cmds.listRelatives(self.name, shapes=True) or []
        for shape in shapes:
            if cmds.objectType(shape) == 'nurbsCurve':
                return shape
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
    # cmds.scriptEditorInfo(clearHistory=True)

    selection = cmds.ls(sl=True)

    # controls = ControlFactory(radius=5)a
    # created_ctrls = controls()

    for obj in selection:
        ctrl = ControlManager(obj, radius=10, match=True)
