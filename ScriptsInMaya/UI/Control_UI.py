import maya.cmds as cmds


def create_control_ui():
    def create_joint_control(*arg):
        selected_joint = cmds.ls(selection=True)[0]

        joint_name = selected_joint
        joint_position = cmds.xform(selected_joint, query=True, worldSpace=True, translation=True)
        joint_rotation = cmds.xform(selected_joint, query=True, worldSpace=True, rotation=True)

        circle = cmds.circle(normal=[1, 0, 0], radius=1)[0]

        circle_name = joint_name.replace("Jnt", "Ctrl")
        cmds.rename(circle, circle_name)

        null_group = cmds.group(empty=True)
        null_group_name = joint_name.replace("Jnt", "Ctrl_Grp")
        null_group = cmds.rename(null_group, null_group_name)

        cmds.xform(null_group, worldSpace=True, translation=joint_position)
        cmds.xform(null_group, worldSpace=True, rotation=joint_rotation)

        cmds.parent(circle_name, null_group_name)

        selected_color_option = cmds.optionMenu(color_option_menu, query=True, value=True)
        color_map = {
            "Red": [1, 0, 0],
            "Green": [0, 1, 0],
            "Blue": [0, 0, 1],
            "Yellow": [1, 1, 0],
            "Orange": [1, 0.5, 0],
            "Purple": [0.5, 0, 1],
            "Pink": [1, 0, 1],
            "Turquoise": [0, 1, 1],
            "White": [1, 1, 1],
            "Black": [0, 0, 0]
        }
        cmds.setAttr(circle_name + ".overrideEnabled", 1)
        cmds.setAttr(circle_name + ".overrideColor",
                     color_map[selected_color_option][0] * 5 + color_map[selected_color_option][1] * 5 * 256 +
                     color_map[selected_color_option][2] * 5 * 256 * 256)

    control_ui_window = 'control_ui_window'
    if cmds.window(control_ui_window, exists=True):
        cmds.deleteUI(control_ui_window)
    cmds.window(control_ui_window,
                title="Control Creator",
                widthHeight=(200, 100),
                maximizeButton=False,
                minimizeButton=False,
                backgroundColor=[.35, .3, .3],
                resizeToFitChildren=True)

    layout = cmds.columnLayout(adjustableColumn=True)

    color_options = ["Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Pink", "Turquoise", "White", "Black"]
    cmds.text(label="Select a color:")
    color_option_menu = cmds.optionMenu()
    for color in color_options:
        cmds.menuItem(label=color)

    cmds.button(label="Create Joint Control", command=create_joint_control)

    cmds.showWindow(control_ui_window)
