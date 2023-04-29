import maya.cmds as cmds


def create_color_change_ui(parent_ui, tool):
    color_menu_order = ["Maya Default Blue", "Black", "White", "Light Grey", "Dark Grey", "Red", "Dark Red",
                        "Light Pink", "Mid Pink", "Pink", "Light Yellow", "Yellow", "Dark Yellow", 'Light Orange',
                        "Orange", "Light Green", "Green", "Dark Green", "Light Neon Green", "Neon Green",
                        "Dark Neon Green", "Neon Blue", "Light Navy Blue", "Navy Blue", "Light Blue", 'Blue',
                        "Dark Blue", "Light Purple", "Dark Purple", "Light Brown", "Brown", "Golden Brown"]

    def change_shape_color(*args):
        color_options = ["Maya Default Blue", "Black", "Dark Grey", "Light Grey", "Dark Red", "Dark Blue", 'Blue',
                         "Dark Green", "Dark Purple", "Pink", "Light Brown", "Brown", "Dark Orange", "Red",
                         "Neon Green", "Navy Blue", "White", "Yellow", "Neon Blue", "Light Neon Green", "Light Pink",
                         'Light Orange', "Light Yellow", "Green", "Golden Brown", "Dark Yellow", "Dark Neon Green",
                         "Light Green", "Light Navy Blue", "Light Blue", "Light Purple", "Mid Pink"]
        selection = cmds.ls(sl=True)
        if not selection:
            return cmds.warning("Please select a shape.")

        menu_index = cmds.optionMenu(color_option_menu, q=True, sl=True) - 1
        color_name = color_menu_order[menu_index]

        if color_name in color_options:
            color_index = int(color_options.index(color_name))
        else:
            print('color not found in list.')

        for sel in selection:
            if cmds.nodeType(sel) == "joint":
                cmds.setAttr("%s.overrideEnabled" % sel, lock=False)
                cmds.setAttr("%s.overrideColor" % sel, lock=False)
                cmds.setAttr("%s.overrideEnabled" % sel, 1)
                cmds.setAttr("%s.overrideColor" % sel, color_index)
            else:
                shapes = cmds.listRelatives(sel, children=True, shapes=True)
                for shape in shapes:
                    cmds.setAttr("%s.overrideEnabled" % shape, lock=False)
                    cmds.setAttr("%s.overrideColor" % shape, lock=False)
                    cmds.setAttr("%s.overrideEnabled" % shape, 1)
                    cmds.setAttr("%s.overrideColor" % shape, color_index)

    color_ui_window = 'color_ui_window'
    if cmds.window(color_ui_window, exists=True):
        cmds.deleteUI(color_ui_window)
    cmds.window(color_ui_window,
                title="Control Creator",
                widthHeight=(200, 100),
                maximizeButton=False,
                minimizeButton=False,
                backgroundColor=[.35, .3, .3],
                resizeToFitChildren=True)

    layout = cmds.columnLayout(adjustableColumn=True)

    cmds.text(label="Select a color:")
    color_option_menu = cmds.optionMenu()
    for color in color_menu_order:
        cmds.menuItem(label=color)

    cmds.button(label="Change Color", command=change_shape_color())

    cmds.showWindow(color_ui_window)


create_color_change_ui()