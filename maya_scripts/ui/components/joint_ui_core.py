import maya.cmds as cmds
from functools import partial
from core.components.joint_cmds import create_joints, orient_joints, rename_joints, display_axis
from ui.components.utils.enable_handler import toggle_state
from ui.components.joint_ui_components import PositionListBlock, ParentBlock, NamingBlock
from ui.components.modular_blocks import WindowAdv, DescriptionFrame, LabeledTextField


class JointUI(WindowAdv):
    def __init__(self, name: str, tool_name: str, type: str, width=500, height=525, **kwargs):
        parent_ui = kwargs.get("parent_ui", kwargs.get("parent", kwargs.get("p", None)))
        create: bool = kwargs.pop("create", kwargs.pop("cr", kwargs.pop("c", False)))
        super_args = [parent_ui, name, tool_name, type, width, height]
        # SUPER: self.name, self.readable_name, self.window_width, self.window_height
        # self.parent_ui, self.tool_name, self.type, self.ui, self.window, self.window_width, self.window_height, 
        # self.window_name, self.window_title
        super_kwargs = self.get_kwargs_for_super(kwargs)
        super().__init__(*super_args, **super_kwargs)

        # Variables
        self.name_block = None
        self.parent_bool = None
        self.parent_name = None
        self.radius = None
        self.loc_list = None

        if create:
            self.create()

    def _ui_setup(self, parent_ui: str | None, tool: str) -> str:
        base_ui = cmds.columnLayout(f"{tool}_base", adj=True, bgc=[.3, .5, .55])
        if parent_ui:
            cmds.columnLayout(base_ui, e=True, p=parent_ui)

        desc = DescriptionFrame(base_ui, create=True, collapsable=True, collapsed=True)
        desc("This tool creates joints at the selected locations.")
        cmds.frameLayout("settings_frame", label="Tool Settings", collapsable=True, parent=base_ui)
        cmds.columnLayout("ui_block", adjustableColumn=True, parent="settings_frame")
        cmds.columnLayout("pos_list_block", adjustableColumn=True, p="ui_block")
        cmds.columnLayout("radius_block", adjustableColumn=True, p="ui_block")
        cmds.columnLayout("naming_block", adjustableColumn=True, p="ui_block")
        cmds.columnLayout("parent_block", adjustableColumn=True, p="ui_block")
        cmds.columnLayout("execute_block", adjustableColumn=True, parent="ui_block")
        self.parent_options = ParentBlock("parent_block", "parent_opt_menu", width=self.window_width, create=True)
        self.loc_list = PositionListBlock("pos_list_block", "Creation_List", width=self.window_width, create=True)
        self.radius_input = LabeledTextField("radius_block", "Joint Radius", 1, width=self.window_width, create=True)
        self.name_block = NamingBlock("naming_block", "name_choice", width=self.window_width, create=True)

        cmds.button(label="Execute", command=self.on_execute, backgroundColor=[1, 0, 0], parent="execute_block")
        self.loc_list.clear()
        self.parent_options.update()
        return base_ui

    def on_execute(self, *_):
        rename = bool(self.name_block)
        parent_bool = bool(self.parent_options)
        parent_name = None if self.parent_options.get() == "None" else self.parent_options.get()
        radius = float(self.radius_input.get())

        created_joints = create_joints(self.loc_list, radius, parent_bool, parent_name)

        if parent_bool:
            orient_joints(created_joints)
        display_axis(created_joints)

        if rename:
            rename_joints(created_joints, self.name_block.result())

        self.parent_options.update()


if __name__ == "__main__":
    JointUI("Joint Tool", "joint", "tab", create=True, parent=None)
