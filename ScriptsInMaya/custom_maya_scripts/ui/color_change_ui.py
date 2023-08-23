import maya.cmds as cmds
from custom_maya_scripts.tools import color_changer
from custom_maya_scripts.utilities import selection_check
from custom_maya_scripts.components import color_library, button_base, optionMenu_base, window_base


def _ui_setup(parent_ui, tool):
    """
    Returns: Color Changer UI
    """
    color_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.35, .3, .3], p=parent_ui)

    color_lib = color_library.ColorIndex()
    color_options = color_lib.get_color_order()
    cmds.rowColumnLayout(f'{tool}_selection_row', p=f'{tool}_base', adj=True, nc=2,
                         cal=[(1, 'center'), (2, 'left')],
                         bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_select_1', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_select_2', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True)
    cmds.text(l="Select a color:", p=f'{tool}_select_1')
    color_option_menu = optionMenu_base.OptionMenuBase('color_option_menu', p=f'{tool}_select_2', bgc=[.5, .2, .2])
    for color in color_options:
        cmds.menuItem(l=color, p=color_option_menu.name)

    def on_execute(*_):
        selected_color = color_option_menu.query('value')
        objects = selection_check.is_selection()
        color_changer.change_color(selected_color, objects)

    button_base.ButtonBase(f'{tool}_button', l="Change Color",
                           p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return color_tab


def create_ui_window():
    win = window_base.WindowBase("color creator",
                                 wh=[200, 100],
                                 maximizeButton=True,
                                 minimizeButton=True,
                                 backgroundColor=[.35, .3, .3],
                                 resizeToFitChildren=True)

    tabs_ui = cmds.tabLayout('tabs_ui', innerMarginWidth=5, innerMarginHeight=5)

    color_tab = _ui_setup(tabs_ui, 'color')

    cmds.tabLayout(tabs_ui, e=True, tl=(color_tab, "color creator"))

    win.initialize()


if __name__ == "__main__":
    create_ui_window()
