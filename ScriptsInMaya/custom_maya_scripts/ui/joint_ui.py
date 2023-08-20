import maya.cmds as cmds
from functools import partial
from custom_maya_scripts.tools import (joint_creator, selection_renamer, parent_selection, center_locator,
                                       joint_axis_vis_toggle)

if 'center_location' not in globals():
    center_location = []


def _ui_setup(parent_ui, tool):
    """
    Returns: Joint Creator UI
    """
    global center_locations
    if 'center_locations' not in globals():
        center_locations = []

    def add_center_to_list(*_):
        """
        Calls center_locator module and adds the center to the list.
        """
        global center_locations
        center = center_locator.get_obj_center(cmds.ls(sl=True))
        for xyz in center:
            center_locations.append(xyz)
            center_txt = str(xyz)
            cmds.textScrollList('position_list', edit=True, append=f'{len(center_locations)}: {center_txt}')
            cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_locations)}):")

    def move_center_item_up(*_):
        global center_locations
        selected_items = cmds.textScrollList('position_list', query=True, selectIndexedItem=True)
        if selected_items:
            index = selected_items[0]
            if index > 1:
                center_locations[index - 2], center_locations[index - 1] = (center_locations[index - 1],
                                                                            center_locations[index - 2])
                cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_locations)}):")
                cmds.textScrollList('position_list', edit=True, removeAll=True)
                for i, item in enumerate(center_locations):
                    cmds.textScrollList('position_list', edit=True,
                                        append=f'{i + 1}: {str(item)}')
                cmds.textScrollList('position_list', edit=True, selectIndexedItem=index - 1)

    def move_center_item_down(*_):
        global center_locations
        selected_items = cmds.textScrollList('position_list', query=True, selectIndexedItem=True)
        if selected_items:
            index = selected_items[0]
            if index < len(center_locations) - 1:
                center_locations[index], center_locations[index + 1] = (center_locations[index + 1],
                                                                        center_locations[index])
                cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_locations)}):")
                cmds.textScrollList('position_list', edit=True, removeAll=True)
                for i, item in enumerate(center_locations):
                    cmds.textScrollList('position_list', edit=True, append=f'{i + 1}: {str(item)}')
                cmds.textScrollList('position_list', edit=True, selectIndexedItem=index + 2)

    def remove_center_item(*_):
        global center_locations
        selected_items = cmds.textScrollList('position_list', query=True, selectIndexedItem=True)
        if selected_items:
            index = selected_items[0]
            cmds.textScrollList('position_list', edit=True, removeIndexedItem=index)
            center_locations.pop(index - 1)
            cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_locations)}):")
            cmds.textScrollList('position_list', edit=True, removeAll=True)
            for i, item in enumerate(center_locations):
                cmds.textScrollList('position_list', edit=True,
                                    append=f'{i + 1}: {str(item)}')
            cmds.textScrollList('position_list', edit=True, deselectAll=True)

    def clear_center_list(*_):
        """
        Clears the center list.
        """
        global center_locations
        center_locations.clear()
        cmds.textScrollList('position_list', edit=True, removeAll=True)
        cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_locations)}):")

    def grey_field(enabler, dependant, *_):
        def update_input_enable():
            return cmds.checkBox(enabler, query=True, value=True)

        cmds.rowColumnLayout(dependant, edit=True,
                             enable=update_input_enable(), noBackground=update_input_enable())

    _tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.3, .5, .55], p=parent_ui)

    cmds.frameLayout('description_frame', label='Description', collapsable=True,
                     collapse=True, parent=f'{tool}_base')
    cmds.text('This tool allows you to Create, Name, parent Joints ',
              parent='description_frame', font='smallPlainLabelFont', backgroundColor=[0, 0, 0])
    cmds.frameLayout('settings_frame', label='Tool Settings', collapsable=True, parent=f'{tool}_base')
    cmds.columnLayout('base_column', adjustableColumn=True, parent='settings_frame')
    cmds.columnLayout('list_column', adjustableColumn=True, parent='base_column')
    cmds.rowColumnLayout('list_upper_buttons_columns', numberOfColumns=3,
                         columnWidth=[(1, 125), (2, 125), (3, 125)],
                         adjustableColumn=True,
                         enable=True, parent='list_column')
    cmds.columnLayout('list_visualized_column', adjustableColumn=True, parent='list_column')
    cmds.rowColumnLayout('list_lower_buttons_columns', numberOfColumns=2,
                         columnWidth=[(1, 125), (2, 125)],
                         adjustableColumn=True,
                         enable=True, parent='list_column')
    cmds.rowColumnLayout('list_lower_column', numberOfColumns=2,
                         columnWidth=[(1, 25), (2, 25)],
                         adjustableColumn=True,
                         enable=True, parent='list_column')
    cmds.columnLayout('name_column_group', adjustableColumn=True, parent='base_column')
    cmds.columnLayout('name_column_upper', adjustableColumn=True, parent='base_column')
    cmds.columnLayout('name_column_lower', adjustableColumn=True, parent='base_column')
    cmds.rowColumnLayout('name_columns', numberOfColumns=2,
                         columnAttach=(1, 'both', 20),
                         columnWidth=[(1, 125), (2, 175)],
                         adjustableColumn=True,
                         enable=False, parent='name_column_lower')
    cmds.columnLayout('parent_column_group', adjustableColumn=True, parent='base_column')
    cmds.columnLayout('parent_column_lower', adjustableColumn=True, parent='base_column')
    cmds.rowColumnLayout('parent_columns', numberOfColumns=3,
                         columnWidth=[(1, 80), (2, 80), (3, 80)],
                         columnAlign=[1, 'center'],
                         columnSpacing=(30, 0),
                         adjustableColumn=True,
                         enable=False, parent='parent_column_lower')
    cmds.columnLayout('lower_column', adjustableColumn=True, parent='base_column')

    cmds.button(label='Add Joint Position', command=add_center_to_list,
                backgroundColor=[0, 0, 0], parent='list_upper_buttons_columns')
    cmds.button(label='Remove Entry', command=remove_center_item,
                backgroundColor=[0, 0, 0], parent='list_upper_buttons_columns')
    cmds.button(label='Clear', command=clear_center_list,
                backgroundColor=[0, 0, 0], parent='list_upper_buttons_columns')
    center_label = cmds.text(label='Joint Positions (0):', align='center', parent='list_visualized_column')
    cmds.textScrollList('position_list', numberOfRows=6, parent='list_visualized_column')
    cmds.button(label='Move Up', command=move_center_item_up,
                backgroundColor=[0, 0, 0], parent='list_lower_buttons_columns')
    cmds.button(label='Move Down', command=move_center_item_down,
                backgroundColor=[0, 0, 0], parent='list_lower_buttons_columns')
    cmds.text(l='Joint Radius:', bgc=[.7, .7, .7], p='list_lower_column')
    radius_input = cmds.textField('joint_radius', tx='1', bgc=[.1, .1, .1], p='list_lower_column')

    def update_name_field(selection):
        if selection == "User Input":
            cmds.textField('name_input_field', edit=True, enable=True)
        else:
            cmds.textField('name_input_field', edit=True, enable=False)

    rename_bool = cmds.checkBox('name_bool', label='Name Joints', value=False,
                                changeCommand=partial(grey_field, 'name_bool', 'name_columns'),
                                parent='name_column_upper')
    cmds.text(label='Naming Scheme Input', parent='name_columns')
    name_input = cmds.textField('name_input_field', parent='name_columns', bgc=[.1, .1, .1])
    cmds.text(label='Optional Quick Selection', parent='name_columns')
    naming_option = cmds.optionMenu("NamingOpMenu", changeCommand=update_name_field,
                                    backgroundColor=[.5, .5, .5], parent='name_columns')
    cmds.menuItem(label='User Input', parent="NamingOpMenu")
    sequential_schemas = ['Spine', 'Arm', 'L_Arm', 'R-Arm', 'Finger', 'L_Finger', 'R_Finger',
                          'Leg', 'L_Leg', 'R_Leg', 'L_FT_Leg', 'R_FT_Leg', 'L_BK_Leg', 'R_BK_Leg',
                          'L_Toe', 'R_Toe', 'Head']
    single_schemas = ['ROOT_JNT', 'COG_Jnt', 'Hip_Jnt']
    for name in sequential_schemas:
        cmds.menuItem(label=f'{name}_##_Jnt', parent="NamingOpMenu")
    for name in single_schemas:
        cmds.menuItem(label=f'{name}', parent="NamingOpMenu")

    def update_joint_list(*_):
        cmds.optionMenu('parent_menu', edit=True, deleteAllItems=True)
        cmds.menuItem(label='None', parent='parent_menu')
        selected_joints = cmds.ls(type='joint')
        for _ in selected_joints:
            cmds.menuItem(label=_, parent='parent_menu')

    parent_checkbox = cmds.checkBox('parent_bool', label='Parent Objects on Creation', value=False,
                                    changeCommand=partial(grey_field, 'parent_bool', 'parent_columns'),
                                    parent='parent_column_group')
    selected_joints = cmds.ls(type='joint')
    parent_option: None = cmds.optionMenu('parent_menu', label='Optional Parent Joint',
                                          bgc=[.5, .5, .5], parent='parent_columns')
    cmds.menuItem(label='None', parent='parent_menu')
    for joint in selected_joints:
        cmds.menuItem(label=joint, parent='parent_menu')
    cmds.button(label='Update List', command=update_joint_list,
                backgroundColor=[.2, 1, .2], parent='parent_columns')

    def on_execute(*_):
        global center_locations
        rename = cmds.checkBox(rename_bool, query=True, value=True)
        naming_input = cmds.textField(name_input, query=True, text=True)
        name_choice = cmds.optionMenu(naming_option, query=True, value=True)
        parent_bool = cmds.checkBox(parent_checkbox, query=True, value=True)
        parent_name = cmds.optionMenu(parent_option, query=True, value=True)
        radius = float(cmds.textField(radius_input, query=True, text=True))

        selected_joints = joint_creator.create_joints_xyz(center_locations, radius)
        joint_axis_vis_toggle.toggle_visibility(selected_joints)

        if rename:
            if name_choice == 'User Input':
                name_schema = naming_input
            else:
                name_schema = name_choice
            if name_schema[0].isdigit() or name_schema.startswith('_'):
                cmds.error('Naming Schema starts with an invalid character.')
                cmds.delete(cmds.ls(sl=True))
            selected_joints = selection_renamer.perform_rename(name_schema, selected_joints)

        if parent_bool:
            selected_joints.reverse()
            if parent_name != 'None':
                selected_joints.append(str(parent_name))
            parent_selection.parent_selected(selected_joints)

    update_joint_list()

    cmds.button(label='Execute', command=on_execute,
                backgroundColor=[1, 0, 0], parent='lower_column')
    clear_center_list()
    return _tab


def create_ui_window(manual_run=False):
    joint_ui_window = "joint_ui_window"
    if cmds.window(joint_ui_window, ex=True):
        cmds.deleteUI(joint_ui_window)
    cmds.window(joint_ui_window, t="Toolbox", wh=(100, 50), mxb=False, mnb=True, rtf=True, nde=True)
    tabs_ui = cmds.tabLayout('tabs_ui', innerMarginWidth=5, innerMarginHeight=5)

    joint_tab = _ui_setup(tabs_ui, 'joint')
    cmds.tabLayout(tabs_ui, e=True, tl=(joint_tab, "Joint Creator"))

    cmds.showWindow(joint_ui_window)


def main():
    create_ui_window(True)


if __name__ == "__main__":
    main()
