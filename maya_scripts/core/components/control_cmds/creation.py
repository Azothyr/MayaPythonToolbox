import maya.cmds as cmds
from core.components.attribute_cmds import set_ as set_attr
import re


class CreateBase:
    def __init__(self, name=None, **kwargs):
        self.__orig_obj = kwargs.get("orig_name", name)
        _name, _shape, _group = self._setup(name)
        self.__name = _name
        self.__shape = _shape
        self.__group = _group
        self.__radius = kwargs.get("radius", 1.0)
        if "radius" in kwargs:
            kwargs.pop("radius")
        self.__group_bool = kwargs.get("group", kwargs.get("grp", kwargs.get("g", True)))
        
        if kwargs.get("run", kwargs.get("create", False)):
            self.create_type(self.__group_bool)

    def __str__(self):
        return f"{self.name!s}"

    def __repr__(self):
        return (f"{self.__class__.__name__}, SHAPE: {self.__shape!r},"
                f" GROUP: {self.__group!r}, RADIUS: {self.__radius!r}), CREATED FROM: {self.__orig_obj!r}")

    def __call__(self, name: str = None, radius: float = None):
        self.__name = name if name is not None else self.__name if self.__name is not None else None
        self.__radius = radius if radius is not None else self.__radius if self.__radius is not None else 1
        if name is None:
            raise ValueError("Name must be provided for the control to be created.")
        self.create_type(self.__group_bool)

    def _setup(self, name: str) -> tuple[str, str, str]:
        original_casing = "mixed"
        if name.islower():
            original_casing = "lower"
        elif name.isupper():
            original_casing = "upper"
        elif name.replace("_", " ").istitle():
            original_casing = "title"

        if name:
            name = re.sub(r"_jnt", "", name, flags=re.IGNORECASE)
            if cmds.objExists(name):
                count = str(len(cmds.ls(name)) + 1).zfill(2)
                name = name + count
        else:
            name = self._generate_unique_name()

        if not re.search(r"_ctrl$", name, re.IGNORECASE):
            name += "_Ctrl"
        shape = name + "Shape"
        group = f"{name}_Grp"

        if original_casing == "lower":
            name, shape, group = [x.lower() for x in [name, shape, group]]
        elif original_casing == "upper":
            name, shape, group = [x.upper() for x in [name, shape, group]]
        elif original_casing == "title":
            name, shape, group = [x.replace("_", " ").title().replace(" ", "_") for x in [name, shape, group]]

        return name, shape, group

    def _create_control(self):
        control = cmds.circle(normal=(0, 1, 0), radius=self.__radius)[0]
        cmds.rename(control, self.__name)
        shape = cmds.listRelatives(self.__name, shapes=True)[0]
        self.__shape = cmds.rename(shape, self.__shape)

    def _create_group(self, create: bool = True):
        if create:
            cmds.group(empty=True, name=self.__group)
            cmds.parent(self.__name, self.__group)
        else:
            self.__group = None

    @staticmethod
    def _generate_unique_name():
        objects = cmds.ls(type="nurbsCurve")
        count = str(sum("ctrl" in obj.lower() for obj in objects) + 1).zfill(2)
        return f"Control_{count}_Ctrl"

    def create_type(self, create_grp: bool):
        self._create_control()
        self._create_group(create_grp)

    @property
    def orig_name(self):
        return self.__orig_obj

    @orig_name.setter
    def orig_name(self, value: str):
        self.__orig_obj = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def shape(self) -> str:
        return self.__shape

    @shape.setter
    def shape(self, value: str):
        self.__shape = value

    @property
    def group(self) -> str:
        return self.__group

    @group.setter
    def group(self, value: str):
        self.__group = value

    @property
    def radius(self) -> float:
        return self.__radius

    @radius.setter
    def radius(self, value: float):
        set_attr(self.__shape, "radius", value)
        self.__radius = value


class Create(CreateBase):
    def __init__(self, *args, **kwargs):
        """
        Required arguments:
        :param name:
        :param radius:

        :param kwargs:
        """
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    selection = cmds.ls(sl=True)
    for obj in selection:
        Create(obj, create=True)
