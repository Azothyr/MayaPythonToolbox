from config.arg_lib_info.optionMenu_arg_map import optionMenu_arg_map as _map_src
from ui.components.maya_cmds_base import CmdsBase


class OptionMenuBase(CmdsBase):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.internal_items = []

    def _get_arg_map(self):
        return _map_src

    def add_item(self, item):
        self.internal_items.append(item)

    def show_items(self):
        print(f'{self._name} options:\n')
        for item in self.internal_items:
            print(item)
