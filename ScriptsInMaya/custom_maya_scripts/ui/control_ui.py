import maya.cmds as cmds
from custom_maya_scripts.tools import color_changer, control_creator


def _ui_setup(parent_ui, tool):
    """
    Returns: Control Creator UI
    """
    control_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.3, .35, .3], p=parent_ui)

    color_options = color_changer.get_color_order()
    cmds.rowColumnLayout(f'{tool}_selection_row', p=f'{tool}_base', adj=True, nc=2,
                         cal=[(1, 'center'), (2, 'left')],
                         bgc=[.5, .5, .5])
    cmds.rowColumnLayout(f'{tool}_radius_row', p=f'{tool}_base', adj=True, nc=2,
                         cal=[(1, 'center'), (2, 'left')],
                         bgc=[.3, .3, .3])
    cmds.columnLayout(f'{tool}_select_col_1', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_select_col_2', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_radius_col_1', p=f'{tool}_radius_row')
    cmds.columnLayout(f'{tool}_radius_col_2', p=f'{tool}_radius_row')
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Select a color:", p=f'{tool}_select_col_1')
    color_option_menu = cmds.optionMenu(p=f'{tool}_select_col_2', bgc=[.5, .2, .2])
    for color in color_options:
        cmds.menuItem(l=color, p=color_option_menu)
    cmds.text(l='Control Scale:', bgc=[.7, .7, .7], p=f'{tool}_radius_col_1')
    radius_input = cmds.textField('radius_input', tx='10', bgc=[.1, .1, .1], p=f'{tool}_radius_col_2')

    def on_execute(*args):
        radius = cmds.textField(radius_input, q=True, text=True)
        selected_color = cmds.optionMenu(color_option_menu, query=True, value=True)

        controls = control_creator.create_at_joint(radius)
        color_changer.change_color(selected_color, controls)

    cmds.button(f'{tool}_button', l="Create Control", p=f'{tool}_bot_button',
                c=on_execute,
                bgc=[0, 0, 0])
    return control_tab


def create_ui_window():
    control_ui_window = 'control_ui_window'
    if cmds.window(control_ui_window, exists=True):
        cmds.deleteUI(control_ui_window)
    cmds.window(control_ui_window,
                title="Control Creator",
                widthHeight=(200, 100),
                maximizeButton=False,
                minimizeButton=True,
                backgroundColor=[.35, .3, .3],
                resizeToFitChildren=True,
                nde=True)
    tabs_ui = cmds.tabLayout('tabs_ui', innerMarginWidth=5, innerMarginHeight=5)

    control_tab = _ui_setup(tabs_ui, 'control')
    cmds.tabLayout(tabs_ui, e=True, tl=[(control_tab, "Control Creator")])

    cmds.showWindow(control_ui_window)


if __name__ == "__main__":
    create_ui_window()

