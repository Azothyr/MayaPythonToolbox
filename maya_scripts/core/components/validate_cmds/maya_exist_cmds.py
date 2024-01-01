import maya.cmds as cmds
from maya_scripts.utilities.kwarg_parser import Parser as Parse
from maya_scripts.utilities.kwarg_option_menu import Menu as OptMenu


class Exists:
    """
    Class to check for the existence of different types of entities in Maya and return a boolean value.
    """
    
    def __init__(self, name: str, type: str = None, **kwargs):
        """
        Initializes the Exists class.

        :param name: The name of the entity to check.
        :param type: The type of the entity (e.g., 'obj', 'attr', 'mesh').
        :param kwargs: Additional arguments for specific checks.
        """
        self.name = name
        self.type = type
        self.options = OptMenu({
            "object": (["o", "obj"], self.obj),
            "attribute": (["a", "at", "attr"], lambda name, **kw: self.attr(
                name, Parse(["attribute", "attr", "at", "a"], "MISSING", **kw)())),
            "mesh": (["m", "msh"], self.mesh),
            "node": (["n"], self.node),
            "constraint": (["cst", "cons"], self.constraint),
            "group": (["g", "grp"], self.group),
            "joint": (["j", "jnt"], self.joint),
            "control": (["c", "ctrl"], self.control),
            "locator": (["l", "loc"], self.locator),
            "shape": (["s", "shp"], self.shape),
        })
        self.exists = self._init_check(**kwargs)

    def __repr__(self) -> str:
        """Returns the representation of the Exists class."""
        return f"{self.__class__.__name__}({self.name!r}, {self.type!r})\nOPTIONS: {self.options}"

    def __bool__(self) -> bool:
        """Returns the boolean value of the existence check."""
        return self.exists

    def _init_check(self, **kwargs) -> bool:
        """
        Performs the initial check to determine the existence of an entity based on its type.

        This method uses a mapping system to associate entity types (and their variants) with specific
        check methods. It then calls the appropriate check method based on the type provided.

        :param kwargs: Additional keyword arguments that may be needed for specific checks.
        :return: True if the entity exists and matches the specified type, False otherwise.
        """

    @staticmethod
    def _invalid() -> bool:
        """Returns False as a fallback for invalid types."""
        return False

    @staticmethod
    def _is_type(name: str, node_type: str) -> bool:
        """
        Checks if the given node is of a specific node type.

        :param name: The name of the node.
        :param node_type: The expected node type.
        :return: True if the node is of the specified type, False otherwise.
        """
        return Exists.obj(name) and cmds.objectType(name) == node_type

    @staticmethod
    def _is_type_with_ending(name: str, node_type: str, end: str) -> bool:
        """
        Checks if the node is of a specific type and ends with a specific suffix.

        :param name: Name of the node to check.
        :param node_type: Type of node to check against.
        :param end: Suffix that the node name should end with.
        :return: True if node is of the type and has the specified suffix.
        """
        return Exists._is_type(name, node_type) and name.lower().endswith(end)

    @staticmethod
    def obj(name: str) -> bool:
        try:
            return cmds.objExists(name)
        except RuntimeError:
            return False

    @staticmethod
    def attr(name: str, attr: str) -> bool:
        if attr == "MISSING":
            return False
        return Exists.obj(name) and cmds.attributeQuery(attr, node=name, exists=True)

    @staticmethod
    def mesh(name: str) -> bool:
        return Exists._is_type(name, "mesh")

    @staticmethod
    def node(name: str) -> bool:
        return Exists._is_type(name, "node")

    @staticmethod
    def constraint(name: str) -> bool:
        return Exists._is_type(name, "constraint")

    @staticmethod
    def group(name: str) -> bool:
        return Exists._is_type_with_ending(name, "transform", "_grp")

    @staticmethod
    def joint(name: str) -> bool:
        return Exists._is_type(name, "joint")

    @staticmethod
    def control(name: str) -> bool:
        return Exists._is_type_with_ending(name, "transform", "_ctrl")

    @staticmethod
    def locator(name: str) -> bool:
        return Exists._is_type(name, "locator")

    @staticmethod
    def shape(name: str) -> bool:
        return Exists._is_type(name, "shape")


if __name__ == "__main__":
    print(Exists("pCube1", "object").__repr__())
