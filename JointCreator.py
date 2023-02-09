import maya.cmds as cmds
from functools import partial


def create_ui():
    """
    Creates UI
    Returns:
    """
    selections = cmds.ls(sl=True)

    schema_list = ['finger_01_knuckle_##', 'finger_02_knuckle_##', 'finger_03_knuckle_##', 'finger_04_knuckle_##',
                   'finger_05_knuckle_##', 'finger_06_knuckle_##', 'finger_07_knuckle_##', 'finger_08_knuckle_##',
                   'finger_09_knuckle_##', 'finger_10_knuckle_##']

    ui_window = 'ui_window'

    if cmds.window(ui_window, exists=True):
        cmds.deleteUI(ui_window)

    ui_window = cmds.window(title='Joint Creator',
                            widthHeight=(400, 300),
                            maximizeButton=False,
                            resizeToFitChildren=True)
    cmds.columnLayout('first_column', adjustableColumn=True, rowSpacing=10)
    cmds.frameLayout(label='Description')
    cmds.text('...')
    cmds.frameLayout(label='Settings')

    cmds.columnLayout(adjustableColumn=True)

    sequence_bool = cmds.checkBox(label='Sequence Selected Objects Names', value=False)

    def sequencing_check():
        return cmds.checkBox(sequence_bool, query=True)

    cmds.rowColumnLayout('sequence_columns', enable=True, numberOfColumns=2,
                         columnAttach=(1, 'right', 0),
                         columnWidth=[(1, 100), (2, 250)],
                         adjustableColumn=True)
    cmds.text(label='Naming Scheme Input')
    name_input = cmds.textField()
    cmds.text(label='Optional Quick Selection')
    cmds.optionMenu()
    cmds.menuItem(label='User Input')

    cmds.columnLayout(adjustableColumn=True, parent='first_column')
    checkbox_center = cmds.checkBox(label='Create at Center of Mass', value=False)
    checkbox_parent = cmds.checkBox(label='SParent Objects on Creation', value=False)
    checkbox_freeze = cmds.checkBox(label='Freeze Transforms on Completion', value=False)

    cmds.rowColumnLayout('creation_order_columns', enable=True, numberOfColumns=2,
                         columnAttach=(1, 'right', 0),
                         columnWidth=[(1, 100), (2, 250)],
                         adjustableColumn=True)
    cmds.text(label='Creation Order')
    cmds.columnLayout('order_column', adjustableColumn=True, parent='creation_order_columns')
    order_control = cmds.radioCollection()
    rb1 = cmds.radioButton(label='First Object Selected to Last')
    rb2 = cmds.radioButton(label='Last Object Selected to First')

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


def pass_values(select_list, scheme_input, center_bool, parent_bool, freeze_bool, order_control):
    selections = select_list
    scheme_input = cmds.textField(scheme_input, query=True, text=True)
    center_bool = cmds.checkBox(center_bool, query=True, value=True)
    parent_bool = cmds.checkBox(parent_bool, query=True, value=True)
    freeze_bool = cmds.checkBox(freeze_bool, query=True, value=True)
    creation_order = cmds.radioCollection(order_control, query=True, select=True)
    tool_manager(selections, scheme_input, center_bool, parent_bool, freeze_bool, creation_order)


def tool_manager(selections, naming_scheme, center_bool, parent_bool, freeze_bool, creation_order):
    def create_joints():
        """
        Creates a joint at each selection(s) transform.
        Returns: [joints]
        """
        new_joints = []

        if center_bool:
            for selection in selections:
                position = cmds.xform(selection, query=True, translation=True, worldSpace=True)
                cmds.select(clear=True)

                jnt = cmds.joint()
                new_joints.append(jnt)
                cmds.xform(jnt, worldSpace=True, translation=position)

            cmds.select(new_joints, replace=True)
    
            return new_joints


create_ui()
