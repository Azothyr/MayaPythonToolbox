import maya.cmds as cmds
from functools import partial


def create_joints_xyz(xyz_list):
    """
    Creates a joint at each XYZ value from a list.
    Returns: [joints]
    """
    new_joints = []

    for xyz in xyz_list:
        center_position = xyz
        cmds.select(clear=True)
        jnt = cmds.joint()
        new_joints.append(jnt)
        cmds.xform(jnt, worldSpace=True, translation=center_position)
    cmds.select(new_joints, replace=True)
    new_joints.reverse()
    return new_joints


def parent_selected(data):
    for value in range(len(data)):
        cmds.select(clear=True)
        cmds.select(data[value])
        if (len(data) - 1) > value:
            cmds.select(data[value + 1], add=True)
            cmds.parent()


def sequential_renamer(txt, data):
    """
    Renames selected objects sequentially.
    Returns:
    """
    data.reverse()
    count = txt.count('#')
    scheme_parts = txt.partition(count * "#")
    objects_changed = 0

    for i in range(len(data)):
        new_name = scheme_parts[0] + str(i + 1).zfill(count) + scheme_parts[2]
        cmds.rename(data[i], new_name)
        objects_changed += 1

    print("Number of Objects renamed: " + str(objects_changed))


def single_renamer(new_name, obj):
    """
    Renames selected object
    """
    name = cmds.rename(obj, new_name)


def add_to_layer(layer_name, data):
    if not cmds.objExists(layer_name):
        cmds.createDisplayLayer(name=layer_name)

    cmds.editDisplayLayerMembers(layer_name, data, noRecurse=True)


def orient_joints(data):
    last_joint = len(data) - 1

    for index in range(len(data)):
        if index == last_joint:
            parent_orientation = cmds.joint(data[index - 1], query=True, orientation=True)
            cmds.joint(data[index], edit=True, orientation=parent_orientation)
            break
        cmds.joint(data[index], edit=True, orientJoint='xyz', secondaryAxisOrient='yup', children=True,
                   zeroScaleOrient=True)


def create_ui():
    """
    Returns: Joint Creator UI
    """

    def get_center(_input):
        """
        finds the selection(s) center of mass.
        Returns: (center x, center y, center z)
        """
        bbox = cmds.exactWorldBoundingBox(_input)
        center = (
            (bbox[0] + bbox[3]) / 2,
            (bbox[1] + bbox[4]) / 2,
            (bbox[2] + bbox[5]) / 2
        )
        return center

    def add_center_to_list(*args):
        """
        Calls get_center function and adds the center to the list.
        """
        global center_location
        if 'center_location' not in globals():
            center_location = []
        is_joint = False
        sel = cmds.ls(sl=True)
        if not sel:
            cmds.warning('No objects selected.')
            return
        for obj in sel:
            if cmds.objectType(obj) == 'joint':
                center = cmds.xform(sel, q=True, ws=True, t=True)
                is_joint = True
            else:
                continue
        if not is_joint:
            center = get_center(sel)
        center_location.append(center)
        center_txt = str(center)
        cmds.textScrollList('position_list', edit=True, append=f'{len(center_location)}: {center_txt}')
        cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_location)}):")

    def move_center_item_up(*args):
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

    def move_center_item_down(*args):
        global center_location
        selected_items = cmds.textScrollList('position_list', query=True, selectIndexedItem=True)
        if selected_items:
            index = selected_items[0]
            if index < len(center_location):
                center_location[index - 1], center_location[index] = center_location[index], center_location[index - 1]
                cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_location)}):")
                cmds.textScrollList('position_list', edit=True, removeAll=True)
                for i, item in enumerate(center_location):
                    cmds.textScrollList('position_list', edit=True,
                                        append=f'{i + 1}: {str(item)}')
                cmds.textScrollList('position_list', edit=True, selectIndexedItem=index + 1)

    def remove_center_item(*args):
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

    def clear_center_list(*args):
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

        cmds.rowColumnLayout(dependant, edit=True, enable=update_input_enable())

    ui_window = 'ui_window'
    if cmds.window(ui_window, exists=True):
        cmds.deleteUI(ui_window)
    cmds.window(ui_window,
                title='Joint Creator',
                widthHeight=(400, 300),
                maximizeButton=False,
                resizeToFitChildren=True)
    cmds.frameLayout('description_frame', label='Description')
    cmds.text('...', parent='description_frame')
    cmds.frameLayout('settings_frame', label='Settings')
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
                         columnAttach=(1, 'left', 20),
                         columnWidth=[(1, 125), (2, 175)],
                         adjustableColumn=True,
                         enable=False, parent='name_column_lower')
    cmds.columnLayout('parent_column_group', adjustableColumn=True, parent='base_column')
    cmds.columnLayout('parent_column_lower', adjustableColumn=True, parent='base_column')
    cmds.rowColumnLayout('parent_columns', numberOfColumns=2,
                         columnAttach=(1, 'left', 20),
                         columnWidth=[(1, 125), (2, 175)],
                         adjustableColumn=True,
                         enable=False, parent='parent_column_lower')
    cmds.columnLayout('lower_column', adjustableColumn=True, parent='base_column')

    cmds.button(label='Add Joint Position', command=add_center_to_list, parent='list_button_columns')
    cmds.button(label='Remove Entry', command=remove_center_item, parent='list_button_columns')
    cmds.button(label='Clear', command=clear_center_list, parent='list_button_columns')
    center_label = cmds.text(label='Joint Positions (0):', align='center', parent='list_column')
    cmds.textScrollList('position_list', numberOfRows=6, parent='list_column')
    cmds.button(label='Move Up', command=move_center_item_up, parent='list_column')
    cmds.button(label='Move Down', command=move_center_item_down, parent='list_column')

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
    naming_option = cmds.optionMenu("NamingOpMenu", changeCommand=update_name_field, parent='name_columns')
    cmds.menuItem(label='User Input', parent="NamingOpMenu")
    sequential_schemas = ['Finger', 'Arm', 'L_FT_Leg', 'R_FT_Leg', 'R_BK_Leg', 'R_BK_Leg', 'Leg', 'Head']
    single_schemas = ['ROOT_JNT', 'COG_Jnt']
    for name in sequential_schemas:
        cmds.menuItem(label=f'{name}_##_Jnt', parent="NamingOpMenu")
    for name in single_schemas:
        cmds.menuItem(label=f'{name}', parent="NamingOpMenu")

    checkbox_parent = cmds.checkBox('parent_bool', label='Parent Objects on Creation', value=False,
                                    changeCommand=partial(grey_field, 'parent_bool', 'parent_columns'),
                                    parent='parent_column_group')
    joints = cmds.ls(type='joint')
    parent_option = cmds.optionMenu('parent_menu', label='Optional Parent Joint', parent='parent_columns')
    cmds.menuItem(label='None', parent='parent_menu')
    for joint in joints:
        cmds.menuItem(parent='parent_menu', label=joint)

    cmds.button(label='Execute', command=partial(pass_values,
                                                 rename_bool,
                                                 name_input,
                                                 naming_option,
                                                 single_schemas,
                                                 checkbox_parent,
                                                 parent_option), parent='lower_column')

    cmds.showWindow(ui_window)
    clear_center_list()


def pass_values(rename, naming_input, name_choice, non_sequence_names, parent_bool, parent_name, *args):
    global center_location
    rename = cmds.checkBox(rename, query=True, value=True)
    naming_input = cmds.textField(naming_input, query=True, text=True)
    name_choice = cmds.optionMenu(name_choice, query=True, value=True)
    parent_bool = cmds.checkBox(parent_bool, query=True, value=True)
    parent_name = cmds.optionMenu(parent_name, query=True, value=True)

    joints = create_joints_xyz(center_location)
    if parent_bool:
        if parent_name != 'None':
            joints.append(str(parent_name))
        parent_selected(joints)

    add_to_layer('Jnt_Layer', joints)

    if rename:
        if name_choice == 'User Input':
            name_schema = naming_input
        elif name_choice in non_sequence_names:
            name_schema = name_choice
        else:
            name_schema = name_choice
        if naming_input[0].isdigit() or naming_input.startswith('_'):
            cmds.error('Naming Schema starts with an invalid character.')
            cmds.delete(cmds.ls(sl=True))
        if "#" in naming_input:
            sequential_renamer(name_schema, joints)
        else:
            single_renamer(name_schema, joints)




create_ui()
