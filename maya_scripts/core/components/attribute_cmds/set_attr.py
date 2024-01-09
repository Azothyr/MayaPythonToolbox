from maya import cmds
from core.components.validate_cmds.maya_existence import Exists as ex


def set_(obj, attr=None, value=None, **kwargs):
    if not ex(obj, a=attr):
        raise RuntimeError(f"Attribute {attr} does not exist on {obj}")

        # Handle when value is a dictionary of attributes.
    if isinstance(value, dict):
        for key, val in value.items():
            cmds.setAttr(f"{obj}.{key}", val)
        # Handle when value is provided directly.
    elif value is not None:
        cmds.setAttr(f"{obj}.{attr}", value)

        # Handle additional keyword arguments, such as lock=True.
    for key, val in kwargs.items():
        cmds.setAttr(f"{obj}.{attr}", **{key: val})
