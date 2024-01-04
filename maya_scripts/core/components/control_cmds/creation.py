import maya.cmds as cmds
from core.components.validate_cmds.maya_exist_cmds import Exists as exists
from core.components.xform_handler import XformHandler as xform


class CreateBase:
    def __init__(self, name=None, radius=1.0, position=(0, 0, 0), rotation=(1, 0, 0), **kwargs):
        if name is None:
            name = self._generate_unique_name()
        self.name, self.shape, self.group = self._setup(name)

        self.control = self.name
        self.radius = radius

        self.pos = position
        self.rot = rotation
        self.ctrl_xform = None
        self.group_xform = None
        self.shape_xform = None

        if kwargs.get("run", kwargs.get("create", False)):
            self.create_type(kwargs.get("mode", "all"))

    def __str__(self):
        return f"{self.control!s}"

    def __repr__(self):
        return f"{self.__class__.__name__}(CONTROL: {self.control!r}, SHAPE: {self.shape!r}, GROUP: {self.group!r}, " \
                  f"RADIUS: {self.radius!r})"

    def __call__(self, name: str = None, radius: float = None):
        self.name = name if name is not None else self.name if self.name is not None else None
        self.radius = radius if radius is not None else self.radius if self.radius is not None else 1
        if name is None:
            raise ValueError("Name must be provided for the control to be created.")
        self.create_type()

    def _setup(self, name: str) -> tuple[str, str, str]:
        if name is None or exists.control(name):
            name = self._generate_unique_name()
        if "_Ctrl" not in name:
            name = f"{name}_Ctrl"
        shape = f"{name}Shape".replace("_ctrl", "")
        group = f"{name}_Grp"
        return name, shape, group

    def _create_control(self):
        control = cmds.circle(normal=(0, 1, 0), radius=self.radius)[0]
        self.control = cmds.rename(control, self.name)
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        self.shape = cmds.rename(shape, self.shape)
        self.ctrl_xform = xform(self.control)
        self.shape_xform = xform(self.shape)

    def _create_group(self, create: bool = True):
        if create:
            cmds.group(empty=True, name=self.group)
            cmds.parent(self.control, self.group)
            self.group_xform = xform(self.group)
        else:
            self.group = None

    def set_xform(self, match_obj: str = None, translate: tuple[float, float, float] = None,
                  rotate: tuple[float, float, float] = None):
        if match_obj:
            self.group_xform.match_xform(match_obj, ["translate", "rotate"])
            self.ctrl_xform.match_xform(match_obj, ["translate", "rotate"])
        elif translate and rotate:
            self.pos = translate if translate is not None else self.pos if self.pos is not None else (0, 0, 0)
            self.rot = rotate if rotate is not None else self.rot if self.rot is not None else (1, 0, 0)
            self.group_xform.set_world_space_position(self.pos)
            self.group_xform.set_world_space_rotation(self.rot)
            self.ctrl_xform.set_world_space_position(self.pos)
            self.ctrl_xform.set_world_space_rotation(self.rot)

    @staticmethod
    def _generate_unique_name():
        objects = cmds.ls(type="nurbsCurve")
        count = str(sum("ctrl" in obj.lower() for obj in objects) + 1).zfill(2)
        return f"Control_{count}_Ctrl"

    def create_type(self, mode="all"):
        self._create_control()
        self._create_group(mode in ["all", "a"])


class Create(CreateBase):
    def __init__(self, *args, radius: float = 1.0, **kwargs):
        super().__init__(*args, radius=radius, **kwargs)


if __name__ == "__main__":
    selection = cmds.ls(sl=True)
    for obj in selection:
        Create(obj, create=True)
