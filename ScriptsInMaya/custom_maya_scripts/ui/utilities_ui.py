import maya.cmds as cmds
from custom_maya_scripts.tools import layer_control, joint_axis_vis_toggle, constrain_commands, modify_history


def layer_cmds_ui(parent_ui, tool):
    layer_cmds_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.2, .2, .35], p=parent_ui)
    cmds.rowColumnLayout(f'{tool}_selection_row', p=f'{tool}_base', adj=True,
                         nc=2, cal=[(1, 'center'), (2, 'left')], bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_select_1', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_select_2', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Add selected objects to layer: ", p=f'{tool}_select_1')
    layer_name_input = cmds.textField('layer_input_field', p=f'{tool}_select_2')

    def on_execute(*_):
        add_to = cmds.textField(layer_name_input, query=True, text=True)
        layer_control.add_to_layer(add_to, cmds.ls(sl=True))

    cmds.button(f'{tool}_button', l="Add To Layer", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return layer_cmds_tab


def axis_visibility_ui(parent_ui, tool):
    axis_visibility_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.1, .1, .3], p=parent_ui)

    cmds.rowColumnLayout(f'{tool}_top_row', p=f'{tool}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Toggles the axis visibility of the selection (joints)", p=f'{tool}_top_row')

    def on_execute(*_):
        joint_axis_vis_toggle.toggle_visibility()

    cmds.button(f'{tool}_button', l="Toggle", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return axis_visibility_tab


def constrain_ui(parent_ui, tool):
    parent_scale_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.3, .1, .1], p=parent_ui)

    cmds.rowColumnLayout(f'{tool}_top_row', p=f'{tool}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Parent, Scale constrain between every other selected objects", p=f'{tool}_top_row')

    def on_execute(*_):
        constrain_commands.parent_scale_constrain(cmds.ls(sl=True))

    cmds.button(f'{tool}_button', l="Parent and Scale", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return parent_scale_tab


def freeze_del_history_ui(parent_ui, tool):
    freeze_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.2, .2, .35], p=parent_ui)

    cmds.rowColumnLayout(f'{tool}_top_row', p=f'{tool}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Freeze the transformations and delete history of selected objects", p=f'{tool}_top_row')

    def on_execute(*_):
        modify_history.perform_freeze_delete(cmds.ls(sl=True))

    cmds.button(f'{tool}_button', l="Freeze and Delete History", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return freeze_tab


def create_ui_window(manual_run=False):
    utility_ui_window = 'utility_ui_window'
    if cmds.window(utility_ui_window, exists=True):
        cmds.deleteUI(utility_ui_window)
    cmds.window(utility_ui_window,
                title="utility Creator",
                widthHeight=(350, 500),
                maximizeButton=False,
                minimizeButton=True,
                backgroundColor=[.35, .3, .3],
                resizeToFitChildren=True,
                nde=True)

    main_layout = cmds.formLayout()

    # Create each UI for tools
    layer_cmd_ui = layer_cmds_ui(main_layout, 'layer_cmds')
    axis_visibility_ui_elem = axis_visibility_ui(main_layout, 'axis_visibility')
    constrain_ui_elem = constrain_ui(main_layout, 'constrain')
    freeze_del_history_ui_elem = freeze_del_history_ui(main_layout, 'freeze_del_history')

    # Attach elements in form layout
    cmds.formLayout(main_layout, edit=True,
                    attachForm=[
                        (layer_cmd_ui, 'top', 5),
                        (layer_cmd_ui, 'left', 5),
                        (layer_cmd_ui, 'right', 5),
                        (axis_visibility_ui_elem, 'left', 5),
                        (axis_visibility_ui_elem, 'right', 5),
                        (constrain_ui_elem, 'left', 5),
                        (constrain_ui_elem, 'right', 5),
                        (freeze_del_history_ui_elem, 'left', 5),
                        (freeze_del_history_ui_elem, 'right', 5),
                    ],
                    attachControl=[
                        (axis_visibility_ui_elem, 'top', 5, layer_cmd_ui),
                        (constrain_ui_elem, 'top', 5, axis_visibility_ui_elem),
                        (freeze_del_history_ui_elem, 'top', 5, constrain_ui_elem),
                    ])

    cmds.showWindow(utility_ui_window)


def main():
    create_ui_window(True)


if __name__ == "__main__":
    main()
