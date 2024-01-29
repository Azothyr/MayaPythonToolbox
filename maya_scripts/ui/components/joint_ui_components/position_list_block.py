import maya.cmds as cmds
from core.components import center_locator
from core.maya_managers.selection_manager import Select as sl
from ui.components.modular_blocks import VisualList


class MainUI(VisualList):
    def __init__(self, parent_ui: str, name: str, **kwargs):
        mode_callbacks = {
            "All Selected": self._add_mode_any_or_all,
            "Each Selected": self._add_mode_iter,
        }
        kwargs["text_format"] = "({:.3f}, {:.3f}, {:.3f})"
        super_args = [parent_ui, name, mode_callbacks]
        super().__init__(*super_args, **kwargs)

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
    if cmds.window("test_win", exists=True):
        cmds.deleteUI("test_win")
    cmds.window("test_win")

    MainUI(
        "test_win",
        "pos_list",
        label="Bold Test Frame",
        label_visible=False,
        font="boldLabelFont",
        width=300,
        height=100,
        border=True,
        marginWidth=5,
        marginHeight=5,
        visible=True,
        collapsable=False,
        collapsed=False,
        color=[0.6, 0.5, 0.6],
        annotation="This is a test frame.",
        create=True)
    cmds.showWindow()
