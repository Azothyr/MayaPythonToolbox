from maya import cmds
from managers.maya_exist_manager import Main as ex


class RemoveBase:
    def __init__(self, obj: str, attr: list[str] | str = None):
        self.obj = obj
        self.attr = attr if isinstance(attr, list) else [attr]

    @staticmethod
    def remove_attrs(obj, attrs: list[str] = None):
        for attr in attrs:
            if ex(obj, a=attr):
                cmds.deleteAttr(f'{obj}.{attr}')
            else:
                print(f'Attribute {attr} does not exist on {obj}.')


class RemoveAdvanced(RemoveBase):
    def __init__(self, obj: str, attr: list | str = None):
        super().__init__(obj, attr)


class Remove(RemoveAdvanced):
    def __init__(self, obj: str, attr: list | str = None):
        super().__init__(obj, attr)
