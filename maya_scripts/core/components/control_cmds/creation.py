import maya.cmds as cmds
from core.maya_managers.selection_manager import Select as sl
from core.components.validate_cmds.maya_exist_cmds import Exists as exists
from core.components.xform_handler import XformHandler as xform


class CreateBase:
    def __init__(self, name: str = None, radius: float = 1):
        self.radius = radius
        self.name, self.shape, self.group = self._setup(name)
        self.control = self.name

    def __str__(self):
        return f"{self.control!s}"

    def __repr__(self):
        return f"{self.__class__.__name__}(CONTROL: {self.control!r}, SHAPE: {self.shape!r}, GROUP: {self.group!r}, " \
                  f"RADIUS: {self.radius!r})"

    def __call__(self, name: str = None, radius: float = None):
        self.name = name if name is not None else self.name if self.name is not None else None
        self.radius = radius if radius is not None else self.radius if self.radius is not None else 1
        if self.name is None:
            self.name, self.shape, self.group = self._setup()
        self.create()

    def _setup(self, name: str = None) -> tuple[str, str, str] or tuple[None, None, None]:
        try:
            if self.name is None:
                objects = cmds.ls(type="nurbsCurve")
                count = str(sum("ctrl" in obj.lower() for obj in objects) + 1).zfill(2)
                name = f"{count}_ctrl"
            if exists.control(name):
                raise ValueError(f"CONTROL: {name} already exists. Please choose a different name.")
            shape = f"{name}Shape"
            group = cmds.group(f"{name}_Grp", empty=True)
        except ValueError as e:
            cmds.warning(e)
            return None, None, None
        return name, shape, group

    def _create_control(self):
        self.control = cmds.circle(self.name, normal=[1, 0, 0], radius=self.radius)[0]
        self.shape = cmds.listRelatives(self.control, shapes=True, type="nurbsCurve")[0]

    def _create_group(self):
        self.group = cmds.group(self.control, name=f"{self.name}_Grp")

    def create_type(self, mode: str = "all"):
        match mode.lower():
            case opt if opt in ["all", "a"]:
                self._create_control()
                self._create_group()
            case opt if opt in ["control", "ctrl", "c"]:
                self._create_control()
            case opt if opt in ["group", "grp", "g"]:
                self._create_group()
            case _:
                self._create_control()
                self._create_group()


class CreateAdvanced:
    def __init__(self, *args, radius: float = 1, **kwargs):
        self.radius = radius
        self.names = []
        if args:
            for arg in args:
                if isinstance(arg, str):
                    self.names.append(arg)
                elif isinstance(arg, (list, tuple)):
                    for item in arg:
                        if isinstance(item, str):
                            self.names.append(item)
                        else:
                            print(f"ERROR: {item} is not a valid argument type.")
                            continue
                else:
                    print(f"ERROR: {arg} is not a valid argument type.")
                    continue
        else:
            self.names = sl()

    def __call__(self, mode: str = "all"):
        self._at_selection(mode)

    def _at_selection(self, selction_type: str = None):
        match selction_type.lower():
            case opt if opt in ["any", "all", "a", "sel", "selection", "s"]:
                typ = sl(self.names)
            case opt if opt in ["joint", "jnt", "j"]:
                typ = sl().filter_selection(joint=True)
            case _:
                typ = sl()
        return self.create(typ)

    def _match_rotation(self, obj: str, target: str):
        pass

    def create(self):
        selected_joints = sl().filter_selection(joint=True)
        joints_to_process = selected_joints if len(selected_joints) > 1 else cmds.ls(sl=True)[0:1]

        control_lyst = []
        for joint in joints_to_process:
            joint_name = joint
            control_name = joint_name.replace("Jnt", "Ctrl")
            group_name = joint_name.replace("Jnt", "Ctrl_Grp")

            joint_position = cmds.xform(joint, q=True, ws=True, t=True)
            joint_rotation = cmds.xform(joint, q=True, ws=True, ro=True)

            control = cmds.circle(normal=[1, 0, 0], radius=self.radius)[0]
            cmds.rotate(joint_rotation[0], joint_rotation[1], joint_rotation[2], self.control, ws=True)
            control = cmds.rename(control, control_name)

            control_lyst.append(control)

            control_group = cmds.rename(null_group, group_name)

            cmds.parent(control, control_group)

            cmds.xform(null_group, ws=True, t=joint_position)
            cmds.xform(null_group, ws=True, ro=joint_rotation)

        return control_lyst


class Create(CreateAdvanced):
    def __init__(self):
        super().__init__()
