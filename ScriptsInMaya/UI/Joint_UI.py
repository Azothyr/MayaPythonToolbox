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
        center = get_center(cmds.ls(sl=True))
        if not center:
            return
        center_location.append(center)
        center_txt = str(center)
        cmds.textScrollList('position_list', edit=True, append=f'{len(center_location)}: {center_txt}')
        cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_location)}):")

    def remove_center_item(*args):
        global center_location
        selected_items = cmds.textScrollList('position_list', query=True, selectIndexedItem=True)
        if selected_items:
            index = selected_items[0]
            cmds.textScrollList('position_list', edit=True, removeIndexedItem=index)
            center_location.pop(index - 1)
            cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_location)}):")

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
    cmds.columnLayout('base_column', adjustableColumn=True)
    cmds.frameLayout(label='Description', parent='base_column')
    cmds.text('...', parent='base_column')
    cmds.frameLayout(label='Settings', parent='base_column')
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
    cmds.columnLayout('lower_column', adjustableColumn=True, parent='base_column')

    cmds.button(label='Add Joint Position', command=add_center_to_list, parent='list_button_columns')
    cmds.button(label='Remove Entry', command=remove_center_item, parent='list_button_columns')
    cmds.button(label='Clear', command=clear_center_list, parent='list_button_columns')
    center_label = cmds.text(label='Joint Positions (0):', align='center', parent='list_column')
    cmds.textScrollList('position_list', numberOfRows=6, parent='list_column')

    def update_name_field(selection):
        if selection == "User Input":
            cmds.textField('name_input_field', edit=True, enable=True)
        else:
            cmds.textField('name_input_field', edit=True, enable=False)

    rename_bool = cmds.checkBox('name_bool', label='Name Joints', value=False,
                  changeCommand=partial(grey_field, 'name_bool', 'name_columns'), parent='name_column_upper')
    cmds.text(label='Naming Scheme Input', parent='name_columns')
    name_input = cmds.textField('name_input_field', parent='name_columns')
    cmds.text(label='Optional Quick Selection', parent='name_columns')
    naming_option = cmds.optionMenu("NamingOpMenu", changeCommand=update_name_field, parent='name_columns')
    cmds.menuItem(label='User Input', parent="NamingOpMenu")
    schema_list = ['Finger', 'Arm', 'Leg', 'Head']
    for name in schema_list:
        cmds.menuItem(label=f'{name}_##_Jnt', parent="NamingOpMenu")

    checkbox_parent = cmds.checkBox(label='Parent Objects on Creation', value=False, parent='lower_column')

    cmds.button(label='Execute', command=partial(pass_values,
                                                 rename_bool,
                                                 name_input,
                                                 naming_option,
                                                 checkbox_parent), parent='lower_column')

    cmds.showWindow(ui_window)
    clear_center_list()


def pass_values(rename, naming_input, name_choice, parent_bool, *args):
    global center_location
    rename = cmds.checkBox(rename, query=True, value=True)
    naming_input = cmds.textField(naming_input, query=True, text=True)
    name_choice = cmds.optionMenu(name_choice, query=True, value=True)
    parent_bool = cmds.checkBox(parent_bool, query=True, value=True)

    joints = create_joints_xyz(center_location)

    if parent_bool:
        parent_selected(joints)

    if rename:
        if name_choice == 'User Input':
            name_schema = naming_input
        else:
            name_schema = name_choice
        sequential_renamer(name_schema, joints)


create_ui()
