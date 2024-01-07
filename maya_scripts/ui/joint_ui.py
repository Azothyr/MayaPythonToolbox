import maya.cmds as cmds
from functools import partial
from core.components import selection_renamer
from core.components.joint_cmds import orient as orientation
from core.components.joint_cmds import create as creation
from core.components.joint_cmds import display_axis
from ui.components.utils.enable_handler import toggle_state
from ui.components.joint.creation_list_frame import MainUI as JointList
from ui.components.option_menu_frame import MainUI as ParentMenu


def _ui_setup(parent_ui: str, tool: str) -> str:
    def update_name_field(selection):
        if selection == "User Input":
            cmds.textField("name_input_field", edit=True, enable=True)
        else:
            cmds.textField("name_input_field", edit=True, enable=False)

    _tab = cmds.columnLayout(f"{tool}_base", adj=True, bgc=[.3, .5, .55], p=parent_ui)

    cmds.frameLayout("description_frame", label="Description", collapsable=True,
                     collapse=True, parent=f"{tool}_base")
    cmds.text("This tool allows you to Create, Name, parent Joints", parent="description_frame",
              font="smallPlainLabelFont", backgroundColor=[0, 0, 0])
    cmds.frameLayout("settings_frame", label="Tool Settings", collapsable=True, parent=f"{tool}_base")
    cmds.columnLayout("ui_base", adjustableColumn=True, parent="settings_frame")
    cmds.columnLayout("pos_list_block", adjustableColumn=True, p="ui_base")
    cmds.columnLayout("radius_block", adjustableColumn=True, p="ui_base")
    cmds.columnLayout("naming_block", adjustableColumn=True, p="ui_base")
    cmds.columnLayout("parent_block", adjustableColumn=True, p="ui_base")
    cmds.columnLayout("execute_block", adjustableColumn=True, parent="ui_base")
    cmds.columnLayout("naming_block_group", adjustableColumn=True, p="naming_block")
    cmds.columnLayout("naming_block_upper", adjustableColumn=True, p="naming_block")
    cmds.columnLayout("naming_block_lower", adjustableColumn=True, p="naming_block")
    cmds.rowColumnLayout("name_input_section", numberOfColumns=2, columnAttach=(1, "both", 20),
                         columnWidth=[(1, 125), (2, 175)], adjustableColumn=True, bgc=[0, 0, 0],
                         enable=False, parent="naming_block_lower")
    parent_options = ParentMenu("parent_block", "parent_opt_menu", create=True)
    loc_list = JointList("pos_list_block", "Creation_List", create=True)
    cmds.text(l="Joint Radius:", bgc=[.7, .7, .7], p="radius_block")
    radius_input = cmds.textField("joint_radius", tx="1", bgc=[.1, .1, .1], p="radius_block", width=100)

    rename_bool = cmds.checkBox("name_bool", label="Name Joints", value=False,
                                changeCommand=partial(toggle_state, "name_bool", "name_input_section"),
                                parent="naming_block_upper")
    cmds.text(label="Naming Scheme Input", parent="name_input_section")
    name_input = cmds.textField("name_input_field", parent="name_input_section", bgc=[.1, .1, .1])
    cmds.text(label="Naming Presets:", parent="name_input_section")
    naming_option = cmds.optionMenu("NamingOpMenu", changeCommand=update_name_field,
                                    backgroundColor=[.5, .5, .5], parent="name_input_section")
    cmds.menuItem(label="User Input", parent="NamingOpMenu")
    sequential_schemas = ["Spine", "Arm", "L_Arm", "R-Arm", "L_Clav", "R_Clav", "Finger_##",
                          "L_Finger_##", "R_Finger_##", "Leg", "L_Leg", "R_Leg", "L_FT_Leg",
                          "R_FT_Leg", "L_BK_Leg", "R_BK_Leg", "L_Toe", "R_Toe", "Head", "Neck", "Tail", "L_Tail",
                          "R_Tail", "Eye", "L_Eye", "R_Eye"]
    single_schemas = ["ROOT_JNT", "COG_Jnt", "Hip_Jnt"]
    for name in sequential_schemas:
        cmds.menuItem(label=f"{name}_##_Jnt", parent="NamingOpMenu")
    for name in single_schemas:
        cmds.menuItem(label=f"{name}", parent="NamingOpMenu")

    def on_execute(*_):
        # add a checkbox for clearing list on execute
        rename = cmds.checkBox(rename_bool, query=True, value=True)
        naming_input = cmds.textField(name_input, query=True, text=True)
        name_choice = cmds.optionMenu(naming_option, query=True, value=True)
        parent_bool = bool(parent_options)
        parent_name = parent_options.get()
        radius = float(cmds.textField(radius_input, query=True, text=True))

        if parent_name != "None" and parent_name is not None:
            loc_list.insert(0, parent_name)
            print(loc_list)
        created_joints = creation(loc_list, radius, parent_bool)
        if parent_bool:
            orientation(created_joints)
        display_axis(created_joints)

        if rename:
            if name_choice == "User Input":
                name_schema = naming_input
            else:
                name_schema = name_choice
            if name_schema[0].isdigit() or name_schema.startswith("_"):
                cmds.error("Naming Schema starts with an invalid character.")
                cmds.delete(cmds.ls(sl=True))
            selection_renamer.perform_rename(name_schema, created_joints)

        parent_options.update()

    cmds.button(label="Execute", command=on_execute, backgroundColor=[1, 0, 0], parent="execute_block")
    loc_list.clear()
    parent_options.update()
    return _tab


def create_ui_window(*_):
    joint_ui_window = "joint_ui_window"
    if cmds.window(joint_ui_window, ex=True):
        cmds.deleteUI(joint_ui_window)
    cmds.window(joint_ui_window, t="Joint Tools", wh=(100, 50), mxb=False, mnb=True, rtf=True, nde=True)
    tabs_ui = cmds.tabLayout("tabs_ui", innerMarginWidth=5, innerMarginHeight=5)

    joint_tab = _ui_setup(tabs_ui, "joint")
    cmds.tabLayout(tabs_ui, e=True, tl=(joint_tab, "Joint Creator"))

    cmds.showWindow(joint_ui_window)


def main():
    create_ui_window()


if __name__ == "__main__":
    main()
