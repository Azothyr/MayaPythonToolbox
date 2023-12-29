import maya.cmds as cmds
from core.components import display_layer, joint_axis_vis_toggle, constraint_cmds, history_cmds, parent_cmds
from ui.components.window_base import WindowBase as Window


def layer_cmds_ui(_parent_ui, tool):
    layer_cmds_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.2, .2, .35], p=_parent_ui)
    cmds.rowColumnLayout(f'{tool}_selection_row', p=f'{tool}_base', adj=True,
                         nc=2, cal=[(1, 'center'), (2, 'left')], bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_select_1', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_select_2', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Add selected objects to layer: ", p=f'{tool}_select_1')
    layer_name_input = cmds.textField('layer_input_field', p=f'{tool}_select_2')

    def on_execute(*_):
        add_to = cmds.textField(layer_name_input, query=True, text=True)
        print("CURRENTLY BROKEN")
        # display_layer.add_to_layer(add_to, cmds.ls(sl=True))

    cmds.button(f'{tool}_button', l="Add To Layer", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return layer_cmds_tab


def axis_visibility_ui(_parent_ui, tool):
    axis_visibility_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.1, .1, .3], p=_parent_ui)

    cmds.rowColumnLayout(f'{tool}_top_row', p=f'{tool}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Toggles the axis visibility of the selection (joints)", p=f'{tool}_top_row')

    def on_execute(*_):
        joint_axis_vis_toggle.toggle_visibility()

    cmds.button(f'{tool}_button', l="Toggle", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return axis_visibility_tab


def parent_scale_ui(_parent_ui, tool):
    parent_scale_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.3, .1, .1], p=_parent_ui)

    cmds.rowColumnLayout(f'{tool}_top_row', p=f'{tool}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Parent, Scale constrain between every other selected objects", p=f'{tool}_top_row')

    def on_execute(*_):
        constraint_cmds.parent_scale_constrain(cmds.ls(sl=True))

    cmds.button(f'{tool}_button', l="Parent and Scale", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return parent_scale_tab


def parent_tool_ui(_parent_ui, tool1='parent', tool2='unparent'):
    parent_tab = cmds.columnLayout(f'{tool1}_base', adj=True, bgc=[.3, .1, .1], p=_parent_ui)

    cmds.rowColumnLayout(f'{tool1}_top_row1', p=f'{tool1}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool1}_bot_button1', p=f'{tool1}_base', adj=True, w=200)
    cmds.text(l="Parent selected objects (Last object is parent of all children, first is the lowest step)",
              p=f'{tool1}_top_row1')

    cmds.rowColumnLayout(f'{tool1}_top_row2', p=f'{tool1}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool1}_bot_button2', p=f'{tool1}_base', adj=True, w=200)

    def on_execute1(*_):
        parent_cmds.parent_selected(cmds.ls(sl=True))

    def on_execute2(*_):
        parent_cmds.unparent_selected(cmds.ls(sl=True))

    cmds.button(f'{tool1}_button', l="Parent", p=f'{tool1}_bot_button1', c=on_execute1, bgc=[0, 0, 0])
    cmds.button(f'{tool2}_button', l="Un_Parent", p=f'{tool1}_bot_button2', c=on_execute2, bgc=[0, 0, 0])
    return parent_tab


def freeze_del_history_ui(_parent_ui, tool):
    freeze_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.2, .2, .35], p=_parent_ui)

    cmds.rowColumnLayout(f'{tool}_top_row', p=f'{tool}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Freeze the transformations and delete history of selected objects", p=f'{tool}_top_row')

    def on_execute(*_):
        history_cmds.freeze_delete(cmds.ls(sl=True))

    cmds.button(f'{tool}_button', l="Freeze and Delete History", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return freeze_tab


def _setup_ui(_parent_ui):
    main_layout = cmds.formLayout('util_form', p=_parent_ui)

    # Create each UI for components
    layer_cmd_ui = layer_cmds_ui(main_layout, 'layer_cmds')
    axis_visibility_ui_elem = axis_visibility_ui(main_layout, 'axis_visibility')
    constrain_ui_elem = parent_scale_ui(main_layout, 'constrain')
    parent_tool_ui_elem = parent_tool_ui(main_layout, 'parent', 'un_parent')
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
                        (parent_tool_ui_elem, 'left', 5),
                        (parent_tool_ui_elem, 'right', 5),
                        (freeze_del_history_ui_elem, 'left', 5),
                        (freeze_del_history_ui_elem, 'right', 5),
                    ],
                    attachControl=[
                        (axis_visibility_ui_elem, 'top', 5, layer_cmd_ui),
                        (constrain_ui_elem, 'top', 5, axis_visibility_ui_elem),
                        (parent_tool_ui_elem, 'top', 5, constrain_ui_elem),
                        (freeze_del_history_ui_elem, 'top', 5, parent_tool_ui_elem),
                    ])
    return main_layout


def create_ui_window(manual_run=False):
    win = Window('utility_ui_window',
                 title="utility Tools",
                 widthHeight=(350, 500),
                 maximizeButton=False,
                 minimizeButton=True,
                 backgroundColor=[.35, .3, .3],
                 resizeToFitChildren=True,
                 nde=True)

    main_layout = cmds.formLayout('main_layout')

    # Create each UI for components
    layer_cmd_ui = layer_cmds_ui(main_layout, 'layer_cmds')
    axis_visibility_ui_elem = axis_visibility_ui(main_layout, 'axis_visibility')
    constrain_ui_elem = parent_scale_ui(main_layout, 'constrain')
    parent_tool_ui_elem = parent_tool_ui(main_layout, 'parent', 'un_parent')
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
                        (parent_tool_ui_elem, 'left', 5),
                        (parent_tool_ui_elem, 'right', 5),
                        (freeze_del_history_ui_elem, 'left', 5),
                        (freeze_del_history_ui_elem, 'right', 5),
                    ],
                    attachControl=[
                        (axis_visibility_ui_elem, 'top', 5, layer_cmd_ui),
                        (constrain_ui_elem, 'top', 5, axis_visibility_ui_elem),
                        (parent_tool_ui_elem, 'top', 5, constrain_ui_elem),
                        (freeze_del_history_ui_elem, 'top', 5, parent_tool_ui_elem),
                    ])

    win.initialize()


def main():
    create_ui_window(True)


if __name__ == "__main__":
    main()
