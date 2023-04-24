from functools import partial
import maya.cmds as cmds


def create_joints_xyz(xyz_list):
    """
    Creates a joint at each XYZ value from a list.
    Returns: [joints]
    """
    new_joints = []

    if not cmds.objExists('Jnt_layer'):
        cmds.createDisplayLayer(name='Jnt_layer', number=1)

    joint_orient_attrs = ['jointOrientX', 'jointOrientY', 'jointOrientZ', 'displayLocalAxis']
    for xyz in xyz_list:
        center_position = xyz
        cmds.select(clear=True)
        jnt = cmds.joint()
        new_joints.append(jnt)
        for attr_name in joint_orient_attrs:
            cmds.setAttr(f"{jnt}.{attr_name}", keyable=False, channelBox=True)
        cmds.xform(jnt, worldSpace=True, translation=center_position)
        cmds.editDisplayLayerMembers('Jnt_layer', jnt)
    cmds.select(new_joints, replace=True)
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
    count = txt.count('#')
    scheme_parts = txt.partition(count * "#")
    objects_changed = 0

    new_names = []
    for i in range(len(data)):
        new_name = scheme_parts[0] + str(i + 1).zfill(count) + scheme_parts[2]
        new_names.append(cmds.rename(data[i], new_name))
        objects_changed += 1
    cmds.select(clear=True)
    cmds.select(new_names, replace=True)
    return new_names


def single_renamer(new_name, data):
    """
    Renames selected object
    """
    new_names = []
    for i in range(len(data)):
        new_names.append(cmds.rename(data[i], new_name))
    cmds.select(clear=True)
    cmds.select(new_names, replace=True)
    return new_names


def add_to_layer(layer_name, data):
    if not cmds.objExists(layer_name):
        cmds.createDisplayLayer(n=layer_name, num=1, nr=True)

    cmds.editDisplayLayerMembers(layer_name, data, noRecurse=True)


def orient_joints(data):
    last_joint = len(data) - 1

    for index in range(len(data)):
        if index == last_joint:
            parent_orientation = cmds.joint(data[index - 1], query=True, orientation=True)
            cmds.joint(data[index], edit=True, orientation=parent_orientation)
            break
        cmds.joint(data[index], edit=True, orientJoint='xyz', secondaryAxisOrient='zup', children=True,
                   zeroScaleOrient=True)


def joint_axis_visibility_toggle(*args):
    selection = cmds.ls(selection=True, type="joint")

    for joint_name in selection:
        display_local_axis = cmds.getAttr(joint_name + ".displayLocalAxis")
        cmds.setAttr(joint_name + ".displayLocalAxis", not display_local_axis)


def freeze_transformations(data):
    """
    Freezes the transformations of the specified objects.
    """
    for obj in data:
        cmds.makeIdentity(obj, apply=True, translate=1, rotate=1, scale=1, n=0)


def delete_history(data):
    """
    Deletes the history of the specified objects.
    """
    for obj in data:
        cmds.delete(obj, ch=True)


def add_to_layer_ui(parent_ui, tool):
    add_to_layer_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.2, .2, .35], p=parent_ui)
    cmds.rowColumnLayout(f'{tool}_selection_row', p=f'{tool}_base', adj=True, nc=2, cal=[(1, 'center'), (2, 'left')],
                         bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_select_1', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_select_2', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Add selected objects to layer: ", p=f'{tool}_select_1')
    layer_name_input = cmds.textField('layer_input_field', p=f'{tool}_select_2')

    def on_execute(*args):
        add_to = cmds.textField(layer_name_input, query=True, text=True)
        partial(add_to_layer, add_to, cmds.ls(sl=True))()

    cmds.button(f'{tool}_button', l="Add To Layer", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return add_to_layer_tab


def parent_scale_constrain(data):
    # Check that there is an even number of objects selected
    if len(data) % 2 != 0:
        cmds.warning("Please select an even number of objects")
        return

    # Cut the selection list in half
    half = int(len(data) / 2)
    parent_objs = data[:half]
    child_objs = data[half:]

    # Create parent and scale constraints for each pair of objects
    for i in range(half):
        cmds.select(child_objs[i], add=True)
        cmds.select(parent_objs[i], toggle=True)

        parent_const = cmds.parentConstraint(mo=True, weight=1)
        cmds.rename(parent_const[0], "{}_parentConstraint".format(child_objs[i]))

        scale_const = cmds.scaleConstraint(offset=(1, 1, 1), weight=1)
        cmds.rename(scale_const[0], "{}_scaleConstraint".format(child_objs[i]))

        # Set override display on constraints
        attrs = ["targetWeight{}".format(j) for j in range(1, len(parent_objs) + 1)]
        for attr in attrs:
            cmds.setAttr("{}.{}".format(parent_const[0], attr), l=False)
            cmds.setAttr("{}.{}".format(parent_const[0], attr), 2)
            cmds.setAttr("{}.{}".format(scale_const[0], attr), l=False)
            cmds.setAttr("{}.{}".format(scale_const[0], attr), 2)


def parent_scale_constrain_ui(parent_ui, tool):
    parent_scale_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.3, .1, .1], p=parent_ui)

    cmds.rowColumnLayout(f'{tool}_top_row', p=f'{tool}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Parent, Scale constrain between every other selected objects", p=f'{tool}_top_row')

    def on_execute(*args):
        partial(parent_scale_constrain, cmds.ls(sl=True))()

    cmds.button(f'{tool}_button', l="Parent and Scale", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return parent_scale_tab


def freeze_del_history_ui(parent_ui, tool):
    freeze_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.2, .2, .35], p=parent_ui)

    cmds.rowColumnLayout(f'{tool}_top_row', p=f'{tool}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Freeze the transformations and delete history of selected objects", p=f'{tool}_top_row')

    def on_execute(*args):
        partial(freeze_transformations, cmds.ls(sl=True))()
        partial(delete_history, cmds.ls(sl=True))()

    cmds.button(f'{tool}_button', l="Freeze and Delete History", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])
    return freeze_tab


def create_control_ui(parent_ui, tool):
    color_menu_order = ["Maya Default Blue", "Black", "White", "Light Grey", "Dark Grey", "Red", "Dark Red",
                        "Light Pink", "Mid Pink", "Pink", "Light Yellow", "Yellow", "Dark Yellow", 'Light Orange',
                        "Orange", "Light Green", "Green", "Dark Green", "Light Neon Green", "Neon Green",
                        "Dark Neon Green", "Neon Blue", "Light Navy Blue", "Navy Blue", "Light Blue", 'Blue',
                        "Dark Blue", "Light Purple", "Dark Purple", "Light Brown", "Brown", "Golden Brown"]

    def create_joint_control(*arg):
        selected_joint = cmds.ls(sl=True)[0]
        color_options = ["Maya Default Blue", "Black", "Dark Grey", "Light Grey", "Dark Red", "Dark Blue", 'Blue',
                         "Dark Green", "Dark Purple", "Pink", "Light Brown", "Brown", "Dark Orange", "Red",
                         "Neon Green", "Navy Blue", "White", "Yellow", "Neon Blue", "Light Neon Green", "Light Pink",
                         'Light Orange', "Light Yellow", "Green", "Golden Brown", "Dark Yellow", "Dark Neon Green",
                         "Light Green", "Light Navy Blue", "Light Blue", "Light Purple", "Mid Pink"]

        if cmds.objectType(selected_joint) != 'joint':
            return cmds.warning("Please select a joint.")
        joint_name = selected_joint
        joint_position = cmds.xform(joint_name, q=True, ws=True, t=True)
        joint_rotation = cmds.xform(joint_name, q=True, ws=True, ro=True)

        menu_index = cmds.optionMenu(color_option_menu, q=True, sl=True) - 1
        color_name = color_menu_order[menu_index]

        if color_name in color_options:
            color_index = int(color_options.index(color_name))
        else:
            print('color not found in list.')

        circle = cmds.circle(nr=[1, 0, 0], r=1)[0]

        circle_rename = joint_name.replace("Jnt", "Ctrl")
        circle = cmds.rename(circle, circle_rename)

        cmds.setAttr("%s.overrideEnabled" % circle, 1)
        cmds.setAttr("%s.overrideColor" % circle, color_index)

        null_group = cmds.group(em=True)
        null_group_rename = joint_name.replace("Jnt", "Ctrl_Grp")
        null_group = cmds.rename(null_group, null_group_rename)

        cmds.parent(circle, null_group)

        cmds.xform(null_group, ws=True, t=joint_position)
        cmds.xform(null_group, ws=True, ro=joint_rotation)

    control_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.3, .35, .3], p=parent_ui)

    cmds.rowColumnLayout(f'{tool}_selection_row', p=f'{tool}_base', adj=True, nc=2,
                         cal=[(1, 'center'), (2, 'left')],
                         bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_select_1', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_select_2', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Select a color:", p=f'{tool}_select_1')
    color_option_menu = cmds.optionMenu(p=f'{tool}_select_2', bgc=[.5, .2, .2])
    for color in color_menu_order:
        cmds.menuItem(l=color, p=color_option_menu)

    cmds.button(f'{tool}_button', l="Create Control", p=f'{tool}_bot_button', c=create_joint_control, bgc=[0, 0, 0])
    return control_tab


def create_color_change_ui(parent_ui, tool):
    color_menu_order = ["Maya Default Blue", "Black", "White", "Light Grey", "Dark Grey", "Red", "Dark Red",
                        "Light Pink", "Mid Pink", "Pink", "Light Yellow", "Yellow", "Dark Yellow", 'Light Orange',
                        "Orange", "Light Green", "Green", "Dark Green", "Light Neon Green", "Neon Green",
                        "Dark Neon Green", "Neon Blue", "Light Navy Blue", "Navy Blue", "Light Blue", 'Blue',
                        "Dark Blue", "Light Purple", "Dark Purple", "Light Brown", "Brown", "Golden Brown"]

    def change_shape_color(*args):
        color_options = ["Maya Default Blue", "Black", "Dark Grey", "Light Grey", "Dark Red", "Dark Blue", 'Blue',
                         "Dark Green", "Dark Purple", "Pink", "Light Brown", "Brown", "Dark Orange", "Red",
                         "Neon Green", "Navy Blue", "White", "Yellow", "Neon Blue", "Light Neon Green", "Light Pink",
                         'Light Orange', "Light Yellow", "Green", "Golden Brown", "Dark Yellow", "Dark Neon Green",
                         "Light Green", "Light Navy Blue", "Light Blue", "Light Purple", "Mid Pink"]
        selection = cmds.ls(sl=True)
        if not selection:
            return cmds.warning("Please select a shape.")

        menu_index = cmds.optionMenu(color_option_menu, q=True, sl=True) - 1
        color_name = color_menu_order[menu_index]

        if color_name in color_options:
            color_index = int(color_options.index(color_name))
        else:
            print('color not found in list.')

        for sel in selection:
            shapes = cmds.listRelatives(sel, c=True, s=True)
            for shape in shapes:
                cmds.setAttr("%s.overrideEnabled" % shape, 1)
                cmds.setAttr("%s.overrideColor" % shape, color_index)

    color_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.35, .3, .3], p=parent_ui)

    cmds.rowColumnLayout(f'{tool}_selection_row', p=f'{tool}_base', adj=True, nc=2,
                         cal=[(1, 'center'), (2, 'left')],
                         bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_select_1', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_select_2', p=f'{tool}_selection_row')
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True)
    cmds.text(l="Select a color:", p=f'{tool}_select_1')
    color_option_menu = cmds.optionMenu(p=f'{tool}_select_2', bgc=[.5, .2, .2])
    for color in color_menu_order:
        cmds.menuItem(l=color, p=color_option_menu)

    cmds.button(f'{tool}_button', l="Change Color", p=f'{tool}_bot_button', c=change_shape_color, bgc=[0, 0, 0])
    return color_tab


def create_joint_ui(parent_ui, tool):
    """
    Returns: Joint Creator UI
    """
    global center_location
    if 'center_location' not in globals():
        center_location = []


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
            if index < len(center_location) - 1:
                center_location[index], center_location[index + 1] = center_location[index + 1], center_location[index]
                cmds.text(center_label, edit=True, label=f"Joint Positions ({len(center_location)}):")
                cmds.textScrollList('position_list', edit=True, removeAll=True)
                for i, item in enumerate(center_location):
                    cmds.textScrollList('position_list', edit=True, append=f'{i + 1}: {str(item)}')
                cmds.textScrollList('position_list', edit=True, selectIndexedItem=index + 2)

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

        cmds.rowColumnLayout(dependant, edit=True,
                             enable=update_input_enable(), noBackground=update_input_enable())

    joint_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.3, .5, .55], p=parent_ui)

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
    cmds.textField(tx='1', bgc=[.1, .1, .1], p='list_lower_column')

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

    def update_joint_list(*args):
        cmds.optionMenu('parent_menu', edit=True, deleteAllItems=True)
        cmds.menuItem(label='None', parent='parent_menu')
        selected_joints = cmds.ls(type='joint')
        for joint in selected_joints:
            cmds.menuItem(label=joint, parent='parent_menu')

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

    def on_execute(*args):
        global center_location
        rename = cmds.checkBox(rename_bool, query=True, value=True)
        naming_input = cmds.textField(name_input, query=True, text=True)
        name_choice = cmds.optionMenu(naming_option, query=True, value=True)
        parent_bool = cmds.checkBox(parent_checkbox, query=True, value=True)
        parent_name = cmds.optionMenu(parent_option, query=True, value=True)

        selected_joints = create_joints_xyz(center_location)
        add_to_layer('Jnt_Layer', selected_joints)
        joint_axis_visibility_toggle(selected_joints)

        if rename:
            if name_choice == 'User Input':
                name_schema = naming_input
            else:
                name_schema = name_choice
            if name_schema[0].isdigit() or name_schema.startswith('_'):
                cmds.error('Naming Schema starts with an invalid character.')
                cmds.delete(cmds.ls(sl=True))
            if "#" in name_schema:
                selected_joints = sequential_renamer(name_schema, selected_joints)
            else:
                selected_joints = single_renamer(name_schema, selected_joints)

        if parent_bool:
            selected_joints.reverse()
            if parent_name != 'None':
                selected_joints.append(str(parent_name))
            parent_selected(selected_joints)

    update_joint_list()

    cmds.button(label='Execute', command=on_execute,
                backgroundColor=[1, 0, 0], parent='lower_column')
    clear_center_list()
    return joint_tab


def create_toolbox_ui():
    toolbox_ui_window = "toolbox_ui_window"
    if cmds.window(toolbox_ui_window, ex=True):
        cmds.deleteUI(toolbox_ui_window)
    cmds.window(toolbox_ui_window, t="Toolbox", wh=(100, 50), mxb=False, mnb=False, rtf=True, nde=True)
    tabs_ui = cmds.tabLayout('tabs_ui', innerMarginWidth=5, innerMarginHeight=5)

    joint_tab = create_joint_ui(tabs_ui, 'joint')
    control_tab = create_control_ui(tabs_ui, 'control')
    color_tab = create_color_change_ui(tabs_ui, 'color')
    freeze_tab = freeze_del_history_ui(tabs_ui, 'freeze_history')
    add_to_layer_tab = add_to_layer_ui(tabs_ui, 'add_to_layer')
    parent_scale_tab = parent_scale_constrain_ui(tabs_ui, 'parent_scale')
    cmds.tabLayout(tabs_ui, e=True, tl=((joint_tab, "Joint Creator"),
                                        (control_tab, "Control Creator"),
                                        (color_tab, "Color Changer"),
                                        (freeze_tab, "Freeze, Delete History"),
                                        (add_to_layer_tab, 'Add To Layer'),
                                        (parent_scale_tab, 'Parent Scale')))

    return toolbox_ui_window


def main():
    cmds.showWindow(create_toolbox_ui())


main()
