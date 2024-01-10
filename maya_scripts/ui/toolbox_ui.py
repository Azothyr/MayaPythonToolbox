import maya.cmds as cmds
from ui.components.control import control_ui
from ui.components.utils import utilities_ui, color_change_ui
from ui.components.joint.joint_ui import JointUI
from ui.components.modular_blocks.advanced_mod.window_adv import MainUI as Window


def create_ui_window(manual_run=False):
    win = Window(None, "Toolbox", "All", "default")
    tabs_ui = cmds.tabLayout("tabs_ui", innerMarginWidth=5, innerMarginHeight=5)

    joint_tab = JointUI("Joint Creator", "joint", "tab", p=tabs_ui)
    control_tab = control_ui._ui_setup(tabs_ui, "control")
    color_tab = color_change_ui._ui_setup(tabs_ui, "color")
    util_tab = utilities_ui._setup_ui(tabs_ui)
    cmds.tabLayout(tabs_ui, e=True, tl=((joint_tab, "Joint Creator"), (control_tab, "Control Creator"), (color_tab, "Color Changer"), (util_tab, "Util Tools")))

    win.create()


if __name__ == "__main__":
    create_ui_window()
