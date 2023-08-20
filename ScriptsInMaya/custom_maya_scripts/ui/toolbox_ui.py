import maya.cmds as cmds
from custom_maya_scripts.ui import joint_ui, control_ui, color_change_ui, utilities_ui


def create_ui_window(manual_run=False):
    toolbox_ui_window = "toolbox_ui_window"
    if cmds.window(toolbox_ui_window, ex=True):
        cmds.deleteUI(toolbox_ui_window)
    cmds.window(toolbox_ui_window, t="Toolbox", wh=(100, 50), mxb=False, mnb=True, rtf=True, nde=True)
    tabs_ui = cmds.tabLayout('tabs_ui', innerMarginWidth=5, innerMarginHeight=5)

    joint_tab = joint_ui._ui_setup(tabs_ui, 'joint')
    control_tab = control_ui._ui_setup(tabs_ui, 'control')
    color_tab = color_change_ui._ui_setup(tabs_ui, 'color')
    axis_visibility_tab = utilities_ui.axis_visibility_ui(tabs_ui, 'axis_visibility')
    freeze_tab = utilities_ui.freeze_del_history_ui(tabs_ui, 'freeze_history')
    add_to_layer_tab = utilities_ui.layer_cmds_ui(tabs_ui, 'add_to_layer')
    constrain_tab = utilities_ui.constrain_ui(tabs_ui, 'parent_scale')
    cmds.tabLayout(tabs_ui, e=True, tl=((joint_tab, "Joint Creator"),
                                        (control_tab, "Control Creator"),
                                        (color_tab, "Color Changer"),
                                        (axis_visibility_tab, "Axis Vis Toggle"),
                                        (freeze_tab, "Freeze, Delete History"),
                                        (add_to_layer_tab, 'Add To Layer'),
                                        (constrain_tab, 'Constrain')))

    cmds.showWindow(toolbox_ui_window)


def main():
    create_ui_window(True)


if __name__ == "__main__":
    main()
