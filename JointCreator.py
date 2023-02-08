import maya.cmds as cmds


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
    cmds.checkBox('checkbox_center', label='Create at Center of Mass', value=False)
    cmds.checkBox('checkbox_parent', label='SParent Objects on Creation', value=False)
    cmds.checkBox('checkbox_freeze', label='Freeze Transforms on Completion', value=False)

    cmds.rowColumnLayout('creation_order_columns', enable=True, numberOfColumns=2,
                         columnAttach=(1, 'right', 0),
                         columnWidth=[(1, 100), (2, 250)],
                         adjustableColumn=True)
    cmds.text(label='Creation Order')
    cmds.columnLayout('order_column', adjustableColumn=True, parent='creation_order_columns')
    cmds.radioCollection('order_collection', parent='order_column')
    rb1 = cmds.radioButton(label='First Object Selected to Last')
    rb2 = cmds.radioButton(label='Last Object Selected to First')

    cmds.radioCollection('order_collection', edit=True, select=rb1)

    scheme_input = cmds.textField(name_input, query=True)
    center_bool = cmds.checkBox('checkbox_center', query=True)
    parent_bool = cmds.checkBox('checkbox_parent', query=True)
    freeze_bool = cmds.checkBox('checkbox_freeze', query=True)
    creation_order = cmds.radioCollection('order_collection', query=True)

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, parent='first_column')
    cmds.button(label='Execute', command=create_joints(selections,
                                                       scheme_input,
                                                       center_bool,
                                                       parent_bool,
                                                       freeze_bool,
                                                       creation_order))

    cmds.showWindow(ui_window)


def create_joints(selections, naming_scheme, center_bool, parent_bool, freeze_bool, creation_order):
    """
    Creates a joint at each selection(s) transform.
    Returns: [joints]
    """
    new_joints = []

    for selection in selections:
        position = cmds.xform(selection, query=True, translation=True, worldSpace=True)
        cmds.select(clear=True)

        jnt = cmds.joint()
        new_joints.append(jnt)
        cmds.xform(jnt, worldSpace=True, translation=position)

    cmds.select(new_joints, replace=True)

    return new_joints


create_ui()
