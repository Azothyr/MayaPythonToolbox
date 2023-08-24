import maya.cmds as cmds
from custom_maya_scripts.info.menuItem_arg_map import menuItem_arg_map as _map_src
from custom_maya_scripts.components.maya_cmds_base import CmdsBase


class MenuItemBase(CmdsBase):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.items = []  # list to store MenuItem instances

    def _get_arg_map(self):
        return _map_src

    def create_menu_items_from_iter(self, iterable, parent):
        for item in iterable:
            _menu_item = MenuItemBase(f'{item}', l=item, p=parent)
            self.items.append(_menu_item)
