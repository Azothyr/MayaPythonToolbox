from maya import cmds
from core.components.validate_cmds.maya_exist_cmds import Exists as ex


class RemoveBase:
    """
    Base class for removing attributes from a Maya object.
    """

    def __init__(self, obj: str, attr: list[str] | str = None):
        """
        Initialize the RemoveBase class.

        :param obj: The name of the Maya object.
        :param attr: A single attribute or list of attributes to remove.
        """
        self.obj = obj
        self.attr = attr if isinstance(attr, list) else [attr]

    @staticmethod
    def remove_attrs(obj: str, attrs: list[str] = None):
        """
        Remove specified attributes from the given object.

        :param obj: The name of the Maya object.
        :param attrs: List of attributes to remove.
        """
        for attr in attrs:
            if ex(obj, a=attr):
                cmds.deleteAttr(f'{obj}.{attr}')
            else:
                print(f'Attribute {attr} does not exist on {obj}.')


class RemoveAdvanced(RemoveBase):
    """
    Advanced class for removing attributes with additional functionality.
    """
    def __init__(self, obj: str, attr: list | str = None):
        super().__init__(obj, attr)


class Remove(RemoveAdvanced):
    """
    Main class to be used for removing attributes, extending advanced functionality.
    """
    def __init__(self, obj: str, attr: list | str = None):
        super().__init__(obj, attr)
