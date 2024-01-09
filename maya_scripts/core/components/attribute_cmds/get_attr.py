import maya.cmds as cmds
from core.components.validate_cmds.maya_existence import Exists as ex


def get(obj, attr):
    if ex(obj, a=attr):
        return cmds.getAttr(f"{obj}.{attr}")
    else:
        cmds.warning(f"Attribute {attr} does not exist on {obj}")
