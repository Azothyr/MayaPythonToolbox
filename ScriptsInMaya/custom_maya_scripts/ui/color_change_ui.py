import maya.cmds as cmds
from custom_maya_scripts.tools import color_changer as color_tool
from custom_maya_scripts.utilities import selection_check
from custom_maya_scripts.components.color_library import ColorIndex as ColorLib
from custom_maya_scripts.components.window_base import WindowBase as Window
from custom_maya_scripts.components.button_base import ButtonBase as Button
from custom_maya_scripts.components.optionMenu_base import OptionMenuBase as OptionMenu
from custom_maya_scripts.components.menuItem_base import MenuItemBase as MenuItem
from custom_maya_scripts.components.rowColumnLayout_base import RowColumnLayoutBase as RowColLayout
from custom_maya_scripts.components.tabLayout_base import TabLayoutBase as TabLayout
from custom_maya_scripts.components.text_base import TextBase as Text
from custom_maya_scripts.components.columnLayout_base import ColumnLayoutBase as ColLayout


def _ui_setup(parent_ui, tool):
    """
    Returns: Color Changer UI
    """
    color_tab = ColLayout(f'{tool}_base', adj=True, bgc=[.35, .3, .3], p=parent_ui)

    color_lib = ColorLib()
    color_options = color_lib.get_color_order()
    selection_row = RowColLayout(f'{tool}_selection_row', p=f'{tool}_base', adj=True, nc=2,
                                 cal=[(1, 'center'), (2, 'left')],
                                 bgc=[.5, .5, .5])
    left_col = ColLayout(f'{tool}_select_1', p=selection_row)
    right_col = ColLayout(f'{tool}_select_2', p=selection_row)
    cmds.columnLayout(f'{tool}_bot_button', p=color_tab, adj=True)
    select_txt = Text('selection_txt', l="Select a color:", p=left_col)
    color_option_menu = OptionMenu('color_opt_menu', p=right_col, bgc=[.5, .2, .2])
    color_m_items = MenuItem('color_menu').create_menu_items_from_iter(color_options, color_option_menu)

    def on_execute(*_):
        selected_color = color_option_menu.query('value')
        objects = selection_check.is_selection()
        color_tool.change_color(selected_color, objects)

    exec_button = Button(f'{tool}_button', l="Change Color",
                         p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return color_tab


def create_ui_window():
    win = Window("color creator",
                 wh=[200, 100],
                 maximizeButton=True,
                 minimizeButton=True,
                 backgroundColor=[.35, .3, .3],
                 resizeToFitChildren=True)

    tabs_ui = TabLayout('tabs_ui', innerMarginWidth=5, innerMarginHeight=5)

    color_tab = _ui_setup(tabs_ui, 'color')

    tabs_ui.edit(tl=(color_tab, "color creator"))

    win.initialize()


if __name__ == "__main__":
    create_ui_window()
