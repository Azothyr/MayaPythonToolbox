import maya.cmds as cmds
from functools import partial
from custom_maya_scripts.tools import (joint_creator, selection_renamer, parent_selection, center_locator,
                                       joint_axis_vis_toggle)

if 'center_location' not in globals():
    center_location = []


def create_joint_ui():
    """
    Returns: Joint Creator UI
    """

    def add_to_list(*args):
        """
        Calls get_center function and adds the center to the list.
        """
        global center_location
        sel = cmds.ls(sl=True)
        center = center_locator.get_obj_center(sel)
        center_location.append(center)
        center_txt = str(center)
        cmds.textScrollList('position_list', edit=True, append=f'{len(center_location)}: {center_txt}')
        cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_location)}):")

    def move_item_up(*args):
        global center_location
        selected_items = cmds.textScrollList('position_list', query=True, selectIndexedItem=True)
        if selected_items:
            index = selected_items[0]
            if index > 1:
                center_location[index - 2], center_location[index - 1] = center_location[index - 1], center_location[
                    index - 2]
                cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_location)}):")
                cmds.textScrollList('position_list', edit=True, removeAll=True)
                for i, item in enumerate(center_location):
                    cmds.textScrollList('position_list', edit=True,
                                        append=f'{i + 1}: {str(item)}')
                cmds.textScrollList('position_list', edit=True, selectIndexedItem=index - 1)

    def move_item_down(*args):
        global center_location
        selected_items = cmds.textScrollList('position_list', query=True, selectIndexedItem=True)
        if selected_items:
            index = selected_items[0]
            if index < len(center_location) - 1:
                center_location[index], center_location[index + 1] = center_location[index + 1], center_location[index]
                cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_location)}):")
                cmds.textScrollList('position_list', edit=True, removeAll=True)
                for i, item in enumerate(center_location):
                    cmds.textScrollList('position_list', edit=True, append=f'{i + 1}: {str(item)}')
                cmds.textScrollList('position_list', edit=True, selectIndexedItem=index + 2)

    def remove_item(*args):
        global center_location
        selected_items = cmds.textScrollList('position_list', query=True, selectIndexedItem=True)
        if selected_items:
            index = selected_items[0]
            cmds.textScrollList('position_list', edit=True, removeIndexedItem=index)
            center_location.pop(index - 1)
            cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_location)}):")
            cmds.textScrollList('position_list', edit=True, removeAll=True)
            for i, item in enumerate(center_location):
                cmds.textScrollList('position_list', edit=True,
                                    append=f'{i + 1}: {str(item)}')
            cmds.textScrollList('position_list', edit=True, deselectAll=True)

    def clear_list(*args):
        """
        Clears the center list.
        """
        global center_location
        center_location.clear()
        cmds.textScrollList('position_list', edit=True, removeAll=True)
        cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_location)}):")

    def grey_field(enabler, dependant, *args):
        def update_input_enable():
            return cmds.checkBox(enabler, query=True, value=True)

        cmds.rowColumnLayout(dependant, edit=True,
                             enable=update_input_enable(), noBackground=update_input_enable())

    def update_window_size(*args):
        cmds.dockControl(joint_ui_control, edit=True, height=400, width=400)

    joint_ui_window = 'joint_ui_window'
    joint_ui_control = 'joint_ui_control'
    if cmds.window(joint_ui_window, exists=True):
        cmds.deleteUI(joint_ui_window)
    cmds.window(joint_ui_window,
                title='Joint Creator',
                widthHeight=(400, 300),
                maximizeButton=False,
                minimizeButton=False,
                backgroundColor=[.3, .5, .55],
                resizeToFitChildren=True)
    if cmds.dockControl(joint_ui_control, exists=True):
        cmds.deleteUI(joint_ui_control)
    cmds.columnLayout('window_base', adjustableColumn=True)
    cmds.frameLayout('description_frame', label='Description', collapsable=True, parent='window_base')
    cmds.text('This tool allows you to Create, Name, parent Joints ',
              parent='description_frame', font='smallPlainLabelFont', backgroundColor=[0, 0, 0])
    cmds.frameLayout('settings_frame', label='Tool Settings', collapsable=True, parent='window_base')
    cmds.columnLayout('base_column', adjustableColumn=True, parent='settings_frame')
    cmds.columnLayout('list_column', adjustableColumn=True, parent='base_column')
    cmds.rowColumnLayout('list_button_columns', numberOfColumns=3,
                         columnWidth=[(1, 125), (2, 125), (3, 125)],
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

    cmds.button(label='Add Joint Position', command=add_to_list,
                backgroundColor=[0, 0, 0], parent='list_button_columns')
    cmds.button(label='Remove Entry', command=remove_item,
                backgroundColor=[0, 0, 0], parent='list_button_columns')
    cmds.button(label='Clear', command=clear_list,
                backgroundColor=[0, 0, 0], parent='list_button_columns')
    center_label = cmds.text(label='Joint Positions (0):', align='center', parent='list_column')
    cmds.textScrollList('position_list', numberOfRows=6, parent='list_column')
    cmds.button(label='Move Up', command=move_item_up,
                backgroundColor=[0, 0, 0], parent='list_column')
    cmds.button(label='Move Down', command=move_item_down,
                backgroundColor=[0, 0, 0], parent='list_column')

    def update_name_field(selection):
        if selection == "User Input":
            cmds.textField('name_input_field', edit=True, enable=True)
        else:
            cmds.textField('name_input_field', edit=True, enable=False)

    rename_bool = cmds.checkBox('name_bool', label='Name Joints', value=False,
                                changeCommand=partial(grey_field, 'name_bool', 'name_columns'),
                                parent='name_column_upper')
    cmds.text(label='Naming Scheme Input', parent='name_columns')
    name_input = cmds.textField('name_input_field', parent='name_columns')
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

    def update_joint_list(*args):
        cmds.optionMenu('parent_menu', edit=True, deleteAllItems=True)
        cmds.menuItem(label='None', parent='parent_menu')
        joints = cmds.ls(type='joint')
        for joint in joints:
            cmds.menuItem(label=joint, parent='parent_menu')

    checkbox_parent = cmds.checkBox('parent_bool', label='Parent Objects on Creation', value=False,
                                    changeCommand=partial(grey_field, 'parent_bool', 'parent_columns'),
                                    parent='parent_column_group')
    joints = cmds.ls(type='joint')
    parent_option: None = cmds.optionMenu('parent_menu', label='Optional Parent Joint', parent='parent_columns')
    cmds.menuItem(label='None', parent='parent_menu')
    for joint in joints:
        cmds.menuItem(label=joint, parent='parent_menu')
    cmds.button(label='Update List', command=update_joint_list,
                backgroundColor=[.2, 1, .2], parent='parent_columns')

    def on_execute(*args):
        partial(pass_values, rename_bool, name_input, naming_option, checkbox_parent, parent_option)()
        update_joint_list()

    cmds.button(label='Execute', command=on_execute,
                backgroundColor=[1, 0, 0], parent='lower_column')

    cmds.dockControl(joint_ui_control,
                     label='Joint Creator',
                     dockStation='viewPanes',
                     area='right',
                     floatChangeCommand=update_window_size,
                     content=joint_ui_window)
    clear_list()


def pass_values(rename, naming_input, name_choice, parent_bool, parent_name, *args):
    global center_location
    rename = cmds.checkBox(rename, query=True, value=True)
    naming_input = cmds.textField(naming_input, query=True, text=True)
    name_choice = cmds.optionMenu(name_choice, query=True, value=True)
    parent_bool = cmds.checkBox(parent_bool, query=True, value=True)
    parent_name = cmds.optionMenu(parent_name, query=True, value=True)

    joints = joint_creator.create_joints_xyz(center_location)
    joint_axis_vis_toggle.toggle_visibility(joints)

    if rename:
        if name_choice == 'User Input':
            name_schema = naming_input
        else:
            name_schema = name_choice
        if name_schema[0].isdigit() or name_schema.startswith('_'):
            cmds.error('Naming Schema starts with an invalid character.')
            cmds.delete(cmds.ls(sl=True))
        joints = selection_renamer.rename_selection(name_schema, joints)

    if parent_bool:
        joints.reverse()
        if parent_name != 'None':
            joints.append(str(parent_name))
        parent_selection.parent_selected(joints)
