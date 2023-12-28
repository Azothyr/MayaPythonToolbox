import maya.cmds as cmds


class Exists:
    @staticmethod
    def obj_exists(obj: str) -> bool:
        try:
            return cmds.objExists(obj)
        except RuntimeError:
            return False

    @staticmethod
    def attr_exists(obj: str, attr: str) -> bool:
        return Exists.obj_exists(obj) and cmds.attributeQuery(attr, node=obj, exists=True)

    @staticmethod
    def mesh_exists(mesh: str) -> bool:
        return Exists.obj_exists(mesh) and cmds.nodeType(mesh) == "mesh"

    @staticmethod
    def node_exists(node: str) -> bool:
        return Exists.obj_exists(node) and cmds.nodeType(node) == "transform"

    @staticmethod
    def constraint_exists(constraint: str) -> bool:
        return Exists.obj_exists(constraint) and cmds.objectType(constraint) == "constraint"

    @staticmethod
    def group_exists(group: str) -> bool:
        return Exists.obj_exists(group) and cmds.objectType(group) == "transform"

    @staticmethod
    def joint_exists(joint: str) -> bool:
        return Exists.obj_exists(joint) and cmds.objectType(joint) == "joint"

    @staticmethod
    def control_exists(control: str) -> bool:
        return Exists.obj_exists(control) and cmds.objectType(control) == "transform"

    @staticmethod
    def locator_exists(locator: str) -> bool:
        return Exists.obj_exists(locator) and cmds.objectType(locator) == "locator"
