from maya_scripts.gui import joint_ui, control_ui, color_change_ui, utilities_ui
from maya_scripts.components.window_base import WindowBase as Window
from maya_scripts.components.tabLayout_base import TabLayoutBase as TabLayout


def create_ui_window(manual_run=False):
    win = Window('toolbox_ui_window', t="All Tools", wh=(100, 50), mxb=False, mnb=True, rtf=True, nde=True)
    tabs_ui = TabLayout('tabs_ui', innerMarginWidth=5, innerMarginHeight=5)

    joint_tab = joint_ui._ui_setup(tabs_ui, 'joint')
    control_tab = control_ui._ui_setup(tabs_ui, 'control')
    color_tab = color_change_ui._ui_setup(tabs_ui, 'color')
    util_tab = utilities_ui._setup_ui(tabs_ui)
    tabs_ui.edit(tl=((joint_tab, "Joint Creator"),
                     (control_tab, "Control Creator"),
                     (color_tab, "Color Changer"),
                     (util_tab, "Util Tools")))

    win.initialize()


if __name__ == "__main__":
    create_ui_window()
