from core.maya_managers.control_manager import ControlManager as control_tool
from core.components import color_changer as color_tool
from core.components.color_library import ColorIndex as ColorLib
from ui.components.window_base import WindowBase as Window
from ui.components.button_base import ButtonBase as Button
from ui.components.optionMenu_base import OptionMenuBase as OptionMenu
from ui.components.menuItem_base import MenuItemBase as MenuItem
from ui.components.rowColumnLayout_base import RowColumnLayoutBase as RowColLayout
from ui.components.tabLayout_base import TabLayoutBase as TabLayout
from ui.components.text_base import TextBase as Text
from ui.components.textField_base import TextFieldBase as TextField
from ui.components.columnLayout_base import ColumnLayoutBase as ColLayout


def _ui_setup(parent_ui, tool):
    """
    Returns: Control Creator UI
    """
    control_tab = ColLayout(f'{tool}_base', adj=True, bgc=[.3, .35, .3], p=parent_ui)

    color_options = ColorLib().get_color_order()
    select_row = RowColLayout(f'{tool}_selection_row', p=f'{tool}_base', adj=True, nc=2,
                              cal=[(1, 'center'), (2, 'left')],
                              bgc=[.5, .5, .5])
    radius_row = RowColLayout(f'{tool}_radius_row', p=f'{tool}_base', adj=True, nc=2,
                              cal=[(1, 'center'), (2, 'left')],
                              bgc=[.3, .3, .3])
    sel_col_1 = ColLayout(f'{tool}_select_col_1', p=select_row)
    sel_col_2 = ColLayout(f'{tool}_select_col_2', p=select_row)
    rad_col_1 = ColLayout(f'{tool}_radius_col_1', p=radius_row)
    rad_col_2 = ColLayout(f'{tool}_radius_col_2', p=radius_row)
    button_col = ColLayout(f'{tool}_bot_button', p=control_tab, adj=True, w=200)
    sel_txt = Text("Select a color:", p=sel_col_1)
    color_option_menu = OptionMenu('control_color_opt_menu', p=sel_col_2, bgc=[.5, .2, .2])
    color_m_items = MenuItem.create_menu_items_from_iter(color_options, color_option_menu)
    scale_txt = Text('scale_txt', l='Control Scale:', bgc=[.7, .7, .7], p=rad_col_1)
    radius_input = TextField('radius_input', tx='10', bgc=[.1, .1, .1], p=rad_col_2)

    def on_execute(*_):
        controls = control_tool(radius=radius_input.query('text'))
        color_tool.change_color(color_option_menu.query('value'), controls)

    exec_button = Button(f'{tool}_button', l="Create Control", p=button_col,
                         c=on_execute,
                         bgc=[0, 0, 0])
    return control_tab


def create_ui_window(manual_run=False):
    win = Window('Control Tools',
                 widthHeight=(200, 100),
                 maximizeButton=True,
                 minimizeButton=True,
                 backgroundColor=[.35, .3, .3],
                 resizeToFitChildren=True)

    tabs_ui = TabLayout('tabs_ui', innerMarginWidth=5, innerMarginHeight=5)

    control_tab = _ui_setup(tabs_ui, 'control')
    tabs_ui.edit(tl=[(control_tab, "control creator")])

    win.initialize()


if __name__ == "__main__":
    create_ui_window()
