from maya import cmds


class RemoveBase:
    def __init__(self, obj: str, attr: list[str] | str = None):
        self.obj = obj
        self.attr = attr if isinstance(attr, list) else [attr]

    def remove_attrs(self, obj, attrs: list[str] = None):
        for attr in attrs:
            if self.attr_exists(obj, attr):
                cmds.deleteAttr(f'{obj}.{attr}')
            else:
                print(f'Attribute {attr} does not exist on {obj}.')

    @staticmethod
    def attr_exists(obj, attr: str = None):
        if cmds.attributeQuery(attr, node=obj, exists=True):
            return True
        return False


class RemoveAdvanced(RemoveBase):
    def __init__(self, obj: str, attr: list | str = None):
        super().__init__(obj, attr)


class Remove(RemoveAdvanced):
    def __init__(self, obj: str, attr: list | str = None):
        super().__init__(obj, attr)
