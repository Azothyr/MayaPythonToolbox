import maya.cmds as cmds
from functools import partial


def create_ui():
    """
    Creates a UI
    Returns: Joint Creator UI
    """
    selections = cmds.ls(sl=True)

    schema_list = ['finger_01_knuckle_##', 'finger_02_knuckle_##', 'finger_03_knuckle_##', 'finger_04_knuckle_##',
                   'finger_05_knuckle_##', 'finger_06_knuckle_##', 'finger_07_knuckle_##', 'finger_08_knuckle_##',
                   'finger_09_knuckle_##', 'finger_10_knuckle_##']

    ui_window = 'ui_window'
    if cmds.window(ui_window, exists=True):
        cmds.deleteUI(ui_window)
    cmds.window(ui_window,
                title='Joint Creator',
                widthHeight=(400, 300),
                maximizeButton=False,
                resizeToFitChildren=True)
    cmds.columnLayout('first_column', adjustableColumn=True, rowSpacing=10)
    cmds.frameLayout(label='Description')
    cmds.text('...')
    cmds.frameLayout(label='Settings')
    cmds.columnLayout(adjustableColumn=True)
    cmds.checkBox('sequence_bool', label='Rename Selections', value=False,
                  changeCommand=partial(sequencing_checkbox, 'sequence_bool', 'sequence_columns'))
    cmds.rowColumnLayout('sequence_columns', numberOfColumns=2,
                         columnAttach=(1, 'right', 0),
                         columnWidth=[(1, 100), (2, 250)],
                         adjustableColumn=True,
                         enable=False)
    cmds.text(label='Naming Scheme Input')
    name_input = cmds.textField()
    cmds.text(label='Optional Quick Selection')
    cmds.optionMenu()
    cmds.menuItem(label='User Input')

    cmds.columnLayout(adjustableColumn=True, parent='first_column')
    checkbox_center = cmds.checkBox(label='Create at Center of Mass', value=False)
    checkbox_parent = cmds.checkBox(label='Parent Objects on Creation', value=False)
    checkbox_freeze = cmds.checkBox(label='Freeze Transforms on Completion', value=False)

    cmds.rowColumnLayout('creation_order_columns', enable=True, numberOfColumns=2,
                         columnAttach=(1, 'right', 0),
                         columnWidth=[(1, 100), (2, 250)],
                         adjustableColumn=True)
    cmds.text(label='Creation Order')
    cmds.columnLayout('order_column', adjustableColumn=True, parent='creation_order_columns')
    order_control = cmds.radioCollection()
    rb1 = cmds.radioButton('first_to_last', label='First Object Selected to Last')
    rb2 = cmds.radioButton('last_to_first', label='Last Object Selected to First')

    order_control = cmds.radioCollection(order_control, edit=True, select=rb1)

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, parent='first_column')
    cmds.button(label='Execute', command=partial(pass_values,
                                                 selections,
                                                 name_input,
                                                 checkbox_center,
                                                 checkbox_parent,
                                                 checkbox_freeze,
                                                 order_control))

    cmds.showWindow(ui_window)


def sequencing_checkbox(enabler, dependant, *args):
    def update_input_enable():
        return cmds.checkBox(enabler, query=True, value=True)

    cmds.rowColumnLayout(dependant, edit=True, enable=update_input_enable())


def pass_values(select_list, scheme_input, center_bool, parent_bool, freeze_bool, order_control, *args):
    selections = select_list
    scheme_input = cmds.textField(scheme_input, query=True, text=True)
    center_bool = cmds.checkBox(center_bool, query=True, value=True)
    parent_bool = cmds.checkBox(parent_bool, query=True, value=True)
    freeze_bool = cmds.checkBox(freeze_bool, query=True, value=True)
    creation_order = cmds.radioCollection(order_control, query=True, select=True)
    # tool_manager(selections, scheme_input, center_bool, parent_bool, freeze_bool, creation_order)
    print(scheme_input)
    print(center_bool)
    print(parent_bool)
    print(freeze_bool)
    print(creation_order)


def tool_manager(selections, naming_scheme, center_bool, parent_bool, freeze_bool, creation_order):
    def create_joints():
        """
        Creates a joint at each selection(s) transform.
        Returns: [joints]
        """
        new_joints = []

        if not center_bool:
            for selection in selections:
                position = cmds.xform(selection, query=True, translation=True, worldSpace=True)
                cmds.select(clear=True)

                jnt = cmds.joint()
                new_joints.append(jnt)
                cmds.xform(jnt, worldSpace=True, translation=position)

            cmds.select(new_joints, replace=True)

            return new_joints


create_ui()
