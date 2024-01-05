from config.arg_lib_info.menuItem_arg_map import menuItem_arg_map as _map_src
from ui.components.ui_cmds.optionMenu_base import OptionMenuBase as OptionMenu
from ui.components.ui_cmds.maya_cmds_base import CmdsBase


class MenuItemBase(CmdsBase):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def _get_arg_map(self):
        return _map_src

    @staticmethod
    def create_menu_items_from_iter(iterable: list[str], parent):
        for item in iterable:
            _menu_item = MenuItemBase(f'{item}', l=item, p=parent)

            if isinstance(parent, OptionMenu):
                parent.add_item(_menu_item)
