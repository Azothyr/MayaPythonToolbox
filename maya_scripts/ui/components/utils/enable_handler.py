import maya.cmds as cmds


def toggle_state(enabler, dependant, *_):
    ui_type = cmds.objectTypeUI(enabler)

    query_mapping = {
        "checkBox": (cmds.checkBox, "value"),
        "radioButtonGrp": (cmds.radioButtonGrp, "select"),
        "textField": (cmds.textField, "text"),
        "floatField": (cmds.floatField, "value"),
        "intField": (cmds.intField, "value"),
        "optionMenu": (cmds.optionMenu, "value"),
        "textScrollList": (cmds.textScrollList, "numberOfItems"),
        "text": (cmds.text, "label"),
    }
    enable_mapping = {
        "rowColumnLayout": cmds.rowColumnLayout,
        "columnLayout": cmds.columnLayout,
        "frameLayout": cmds.frameLayout,
        "tabLayout": cmds.tabLayout,
        "formLayout": cmds.formLayout,
        "shelfLayout": cmds.shelfLayout,
        "scrollLayout": cmds.scrollLayout,
    }

    query_func, query_prop = query_mapping.get(ui_type, (None, None))
    enable_func = enable_mapping.get(cmds.objectTypeUI(dependant), None)

    if query_func and query_prop and enable_func:
        def update_input_enable():
            state = query_func(enabler, query=True, **{query_prop: True})
            enable_func(dependant, edit=True, enable=state)
            try:
                if cmds.attributeQuery('noBackground', node=dependant, exists=True):
                    enable_func(dependant, edit=True, noBackground=state)
            except TypeError:
                pass
        update_input_enable()
    else:
        cmds.warning(f"UI type '{ui_type}' or dependent type '{cmds.objectTypeUI(dependant)}' is not "
                     "supported by grey_field function.")

# Example usage
# toggle_state("myCheckBox", "myRowColumnLayout")
