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


def toggle_layouts(conditions: dict[str, bool]):
    """
    Toggles visibility between layouts based on specified conditions.

    :param conditions: A dictionary where keys are layout names and values are booleans
                       indicating whether the layout should be managed/visible.

    :return str: The name of the currently active layout.
    """
    active_layout = None
    for layout, activated_bool in conditions.items():
        cmds.layout(layout, edit=True, manage=activated_bool)
        if activated_bool:
            active_layout = layout

    return active_layout

# # Example checkbox UI setup
# if cmds.window("toggleWindow", exists=True):
#     cmds.deleteUI("toggleWindow", window=True)
# cmds.window("toggleWindow", title="Dynamic Toggle Layouts Example")
#
# mainLayout = cmds.columnLayout(adjustableColumn=True)
# checkBox = cmds.checkBox(label="Toggle Layouts", value=False)
#
# # Define layouts to toggle
# layout1 = cmds.rowColumnLayout(numberOfColumns=2, parent=mainLayout)
# cmds.button(label="Button A1")
# cmds.button(label="Button A2")
#
# layout2 = cmds.rowColumnLayout(numberOfColumns=2, parent=mainLayout, manage=False)
# cmds.button(label="Button B1")
# cmds.button(label="Button B2")
#
# cmds.showWindow("toggleWindow")
#
# # Function to update layouts based on checkbox
# def update_layouts(*_):
#     state = cmds.checkBox(checkBox, query=True, value=True)
#     # Define conditions for layout visibility
#     conditions = {
#         layout1: not state,
#         layout2: state,
#     }
#     active_layout = toggle_layouts(conditions)
#     print(f"Active layout: {active_layout}")
#
# # Attach update_layouts function to checkbox
# cmds.checkBox(checkBox, edit=True, changeCommand=update_layouts)

# Initial update to set correct layout visibility
# update_layouts()


# # Example multiple layouts UI setup
# if cmds.window("toggleMultiLayoutWindow", exists=True):
#     cmds.deleteUI("toggleMultiLayoutWindow", window=True)
# cmds.window("toggleMultiLayoutWindow", title="Dynamic Toggle Multiple Layouts Example")
#
# mainLayout = cmds.columnLayout(adjustableColumn=True)
# optionMenu = cmds.optionMenu(label="Choose Layout", changeCommand=lambda *_: update_layouts())
#
# # Add menu items dynamically and create corresponding layouts
# layouts = {}  # Store layout names for reference
# for i in range(1, 5):  # Example for 4 layouts
#     # Add option to optionMenu for each layout
#     cmds.menuItem(label=f"Layout {i}")
#     # Create each layout and store it in the dictionary, initially not managed
#     layout = cmds.rowColumnLayout(numberOfColumns=2, parent=mainLayout, manage=False)
#     # Populate the layout with example content
#     cmds.button(label=f"Button {i}A")
#     cmds.button(label=f"Button {i}B")
#     layouts[f"Layout {i}"] = layout
#
# cmds.showWindow("toggleMultiLayoutWindow")
#
# # Function to update layouts based on optionMenu
# def update_layouts(*_):
#     selected = cmds.optionMenu(optionMenu, query=True, value=True)
#     conditions = {layout: (label == selected) for label, layout in layouts.items()}
#     active_layout = toggle_layouts(conditions)
#     print(f"Active layout: {active_layout}")
#
# # Initial update to set correct layout visibility based on default optionMenu selection
# update_layouts()
