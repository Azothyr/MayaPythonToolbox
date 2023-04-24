import maya.cmds as cmds


def create_color_change_ui(*args):
    color_menu_order = ["Black", "White", "Light Grey", "Mid Grey", "Grey", "Red", "Dark Red", "Light Pink", "Mid Pink",
                        "Pink", "Light Yellow", "Yellow", "Dark Yellow", "Light Green", "Green", "Dark Green",
                        "Light Neon Green", "Neon Green", "Dark Neon Green", "Neon Blue", "Light Navy Blue",
                        "Navy Blue", "Light Blue", "Dark Blue", "Light Purple", "Dark Purple", "Light Brown", "Brown",
                        "Orange Brown", "Golden Brown"]

    def change_shape_color(*args):
        selection = cmds.ls(sl=True)
        color_options = ["Mid Grey", "Black", "Grey", "Light Grey", "Dark Red", "Dark Blue", "Dark Green",
                               "Dark Purple", "Pink", "Light Brown", "Brown", "Orange Brown", "Red", "Neon Green",
                               "Navy Blue", "White", "Yellow", "Neon Blue", "Light Neon Green", "Light Pink",
                               "Light Yellow", "Green", "Golden Brown", "Dark Yellow", "Dark Neon Green",
                               "Light Green", "Light Navy Blue", "Light Blue", "Light Purple", "Mid Pink"]
        if not selection:
            cmds.warning("Please select a shape.")
            return

        menu_index = cmds.optionMenu(color_option_menu, query=True, select=True)
        color_name = color_options[menu_index]

        if color_name in color_options:
            color_index = int(color_options.index(color_name))
        else:
            print('color not found in list.')
        
        for sel in selection:
            shapes = cmds.listRelatives(sel, children=True, shapes=True)
            for shape in shapes:
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