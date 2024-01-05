import maya.cmds as cmds
from functools import partial
from ui.components.utils.enable_handler import toggle_state
from ui.components.mod_blocks.basic_mod.form_base import BaseUI


class MainUI(BaseUI):
    def __init__(self, parent_ui: str, name: str, width=300, **kwargs):
        super_args = [parent_ui, name, width]
        # SUPER: self.name, self.readable_name, self.window_width, self.form, self.frame, self.parent_ui
        super().__init__(*super_args)

        # Variables
        self.selected_option = None

        # Sub UIs
        self.top_section = f"{self.name}_top"
        self.bot_section = f"{self.name}_bot"

        # Sub UI Components
        self.input_columns = f"{self.name}_columns"
        self.toggle = f"{self.name}_bool"
        self.menu = f"{self.name}_menu"

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
            self._create_ui()

    def __bool__(self):
        return cmds.checkBox(self.toggle, query=True, value=True)

    def get(self):
        return cmds.optionMenu(self.menu, query=True, value=True)

    def _setup_main_ui(self):
        cmds.columnLayout(self.top_section, adjustableColumn=True, p=self.frame)
        self.bot_section = cmds.columnLayout(self.bot_section, adjustableColumn=True, p=self.frame)
        cmds.rowColumnLayout(self.input_columns, numberOfColumns=3,
                             columnWidth=[(1, 80), (2, 80), (3, 80)],
                             columnAlign=[1, "center"],
                             columnSpacing=(30, 0),
                             adjustableColumn=True, bgc=[.3, .3, .3],
                             enable=False, parent=self.bot_section)

    def _setup_ui_components(self):
        cmds.checkBox(self.toggle, label="Parent Objects on Creation", value=False,
                      changeCommand=partial(toggle_state, self.toggle, self.bot_section),
                      parent=self.top_section)

        scene_joints = cmds.ls(type="joint")

        cmds.text(label="Parent To:", parent=self.input_columns, align="right")
        self.selected_option: None = cmds.optionMenu(self.menu, bgc=[.5, .5, .5], parent=self.input_columns)
        cmds.menuItem(label="None", parent=self.menu)
        for joint in scene_joints:
            cmds.menuItem(label=joint, parent=self.menu)
        cmds.button(label="Update", command=self._update_menu,
                    backgroundColor=[.2, 1, .2], parent=self.input_columns)

    def _update_menu(self, *_):
        cmds.optionMenu(self.menu, edit=True, deleteAllItems=True)
        cmds.menuItem(label="None", parent=self.menu)
        scene_joints = cmds.ls(type="joint")
        for joint in scene_joints:
            cmds.menuItem(label=joint, parent=self.menu)

    def update(self, *_):
        self._update_menu()
