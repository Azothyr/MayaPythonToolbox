from maya import cmds
from core.components.validate_cmds.maya_existence import Exists as ex


def remove(obj: str, attrs: str | list[str] = None):
    """
    Remove specified attributes from the given object.

    :param obj: The name of the Maya object.
    :param attrs: List of attributes to remove.
    """
    if attrs is None:
        raise RuntimeError(f"ERROR: Missing required Attribute argument for removal on object: {obj}.")
    if isinstance(attrs, str):
        attrs = [attrs]
    for attr in attrs:
        if ex(obj, a=attr):
            cmds.deleteAttr(f'{obj}.{attr}')
        else:
            print(f'Attribute {attr} does not exist on {obj}.')
