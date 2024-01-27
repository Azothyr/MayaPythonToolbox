import maya.cmds as cmds
from core.components import center_locator
from core.maya_managers.selection_manager import Select as sl
from ui.components.modular_blocks.advanced_mod.visual_list import MainUI as AdvUI


class MainUI(AdvUI):
    def __init__(self, parent_ui: str, name: str, width: int = None, **kwargs):
        mode_callbacks = {
            "All Selected": self._add_mode_any_or_all,
            "Each Selected": self._add_mode_iter,
        }
        text_format = "({:.3f}, {:.3f}, {:.3f})"

        if not width:
            width = 300

        super_args = [parent_ui, name, width, mode_callbacks, text_format]
        super_kwargs = {"collapsed": False, "collapsable": False}
        super().__init__(*super_args, **super_kwargs)

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
            self._create_ui()

    def insert(self, index, value):
        if not isinstance(value, (tuple, list)):
            if isinstance(value, str):
                value = center_locator.get_center(value)
        self.list.insert(index, value)

    def _add_mode_any_or_all(self, passed_objs=None, *_):
        passed_objs = passed_objs if passed_objs else sl()()
        center = center_locator.get_center(passed_objs)
        text = "({:.3f}, {:.3f}, {:.3f})".format(*center)
        self.list.append(center)
        self.count = "(%i):" % len(self.list)
        cmds.textScrollList(self.list_name, edit=True, append=f"{self.count} {text}")
        cmds.text(self.list_label, edit=True, label=f"{self.list_label} {self.count}")

    def _add_mode_iter(self, *_):
        for item in sl():
            self._add_mode_any_or_all(item)


if __name__ == "__main__":
    # Example usage:
    if cmds.window("main_window", exists=True):
        cmds.deleteUI("main_window")
    cmds.window("main_window")
    cmds.showWindow("main_window")
    MainUI("main_window", "test", create=True)
    cmds.showWindow()
    print("DUNDER COMPLETED")
