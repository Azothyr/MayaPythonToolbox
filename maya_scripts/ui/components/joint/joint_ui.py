import maya.cmds as cmds
from functools import partial
from core.components import selection_renamer
from core.components.joint_cmds import orient as orientation
from core.components.joint_cmds import create as creation
from core.components.joint_cmds import display_axis
from ui.components.utils.enable_handler import toggle_state
from ui.components.joint.creation_list_frame import MainUI as JointList
from ui.components.option_menu_frame import MainUI as ParentMenu
from ui.components.modular_blocks.advanced_mod.window_adv import MainUI as Window
from ui.components.modular_blocks.advanced_mod.textfield_mods.labeled_textfield import MainUI as LabeledTextField
from ui.components.modular_blocks.advanced_mod.description_frame import MainUI as Description


class JointUI(Window):
    def __init__(self, name: str, tool_name: str, type: str, width=375, height=450, **kwargs):
        parent_ui = kwargs.get("parent_ui", kwargs.get("parent", kwargs.get("p", None)))
        create: bool = kwargs.pop("create", kwargs.pop("cr", kwargs.pop("c", False)))
        super_args = [parent_ui, name, tool_name, type, width, height]
        # SUPER: self.name, self.readable_name, self.window_width, self.window_height
        # self.parent_ui, self.tool_name, self.type, self.ui, self.window, self.window_width, self.window_height, 
        # self.window_name, self.window_title
        super_kwargs = self.get_kwargs_for_super(kwargs)
        super().__init__(*super_args, **super_kwargs)
        
        # Variables
        self.rename = None
        self.naming_input = None
        self.name_choice = None
        self.parent_bool = None
        self.parent_name = None
        self.radius = None
        self.loc_list = None

        if create:
            self._window_setup()
        
    def _ui_setup(self, parent_ui: str | None, tool: str) -> str:
        def update_name_field(selection):
            if selection == "User Input":
                cmds.textField("name_input_field", edit=True, enable=True)
            else:
                cmds.textField("name_input_field", edit=True, enable=False)
        
        base_ui = cmds.columnLayout(f"{tool}_base", adj=True, bgc=[.3, .5, .55])
        if parent_ui:
            cmds.columnLayout(base_ui, e=True, p=parent_ui)
    
        desc = Description(base_ui, create=True, collapsable=True, collapsed=True)
        desc("This tool creates joints at the selected locations.")
        cmds.frameLayout("settings_frame", label="Tool Settings", collapsable=True, parent=base_ui)
        cmds.columnLayout("ui_block", adjustableColumn=True, parent="settings_frame")
        cmds.columnLayout("pos_list_block", adjustableColumn=True, p="ui_block")
        cmds.columnLayout("radius_block", adjustableColumn=True, p="ui_block")
        cmds.columnLayout("naming_block", adjustableColumn=True, p="ui_block")
        cmds.columnLayout("parent_block", adjustableColumn=True, p="ui_block")
        cmds.columnLayout("execute_block", adjustableColumn=True, parent="ui_block")
        cmds.columnLayout("naming_block_group", adjustableColumn=True, p="naming_block")
        cmds.columnLayout("naming_block_upper", adjustableColumn=True, p="naming_block")
        cmds.columnLayout("naming_block_lower", adjustableColumn=True, p="naming_block")
        cmds.rowColumnLayout("name_input_section", numberOfColumns=2, columnAttach=(1, "both", 20),
                             columnWidth=[(1, 125), (2, 175)], adjustableColumn=True, bgc=[0, 0, 0],
                             enable=False, parent="naming_block_lower")
        self.parent_options = ParentMenu("parent_block", "parent_opt_menu", create=True)
        self.loc_list = JointList("pos_list_block", "Creation_List", create=True)
        self.radius_input = LabeledTextField("radius_block", "Joint Radius", 100, 1, "right", create=True)
        self.rename = cmds.checkBox("name_bool", label="Name Joints", value=False,
                                    changeCommand=partial(toggle_state, "name_bool", "name_input_section"),
                                    parent="naming_block_upper")
        cmds.text(label="Naming Scheme Input", parent="name_input_section")
        self.name_input = cmds.textField("name_input_field", parent="name_input_section", bgc=[.1, .1, .1])
        cmds.text(label="Naming Presets:", parent="name_input_section")
        self.naming_option = cmds.optionMenu("NamingOpMenu", changeCommand=update_name_field,
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
    
        cmds.button(label="Execute", command=self.on_execute, backgroundColor=[1, 0, 0], parent="execute_block")
        self.loc_list.clear()
        self.parent_options.update()
        return base_ui
    
    def on_execute(self, *_):
        rename = cmds.checkBox(self.rename, query=True, value=True)
        naming_input = cmds.textField(self.name_input, query=True, text=True)
        name_choice = cmds.optionMenu(self.naming_option, query=True, value=True)
        parent_bool = bool(self.parent_options)
        parent_name = self.parent_options.get()
        radius = float(self.radius_input.get())
    
        if parent_name != "None" and parent_name is not None:
            self.loc_list.insert(0, parent_name)
        created_joints = creation(self.loc_list, radius, parent_bool)
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

        if parent_name != "None" and parent_name is not None:
            self.loc_list.pop(0)
    
        self.parent_options.update()


if __name__ == "__main__":
    from ui.components.modular_blocks.basic_mod.window_base import BaseUI as Window
    JointUI("Joint Tool", "joint", "tab", create=True)
