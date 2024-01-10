import maya.cmds as cmds
from ui.components.modular_blocks.basic_mod.form_base import BaseUI


class MainUI(BaseUI):
    def __init__(self, parent_ui: str, name: str, width=300, default=None, align_text="center", **kwargs):
        super_args = [parent_ui, name, width]
        # SUPER: self.name, self.readable_name, self.window_width, self.form, self.frame, self.parent_ui
        super().__init__(*super_args)

        # Variables
        self.text = str(default) if default else None

        # Sub UIs
        self.section = f"{self.name}_section"
        self.columns = f"{self.name}_columns"

        # Sub UI Components
        self.input = f"{self.name}_input"
        self.label = f"{self.name}_label"
        self.align_text = align_text

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
            self._create_ui()

    def get(self):
        return cmds.textField(self.input, query=True, text=True)

    def _setup_main_ui(self):
        col_width = int(self.window_width / 2)

        self.section = cmds.columnLayout(self.section, adjustableColumn=True, p=self.frame)
        self.columns = cmds.rowColumnLayout(self.columns, numberOfColumns=2,
                             columnWidth=[(1, col_width), (2, col_width)],
                             adjustableColumn=True,
                             enable=True, parent=self.section)

    def _setup_ui_components(self):
        cmds.text(l=f"{self.readable_name}:", bgc=[.7, .7, .7], p=self.columns, align=self.align_text)
        self.input = cmds.textField(self.label, tx=self.text, bgc=[.1, .1, .1], p=self.columns, width=100)


if __name__ == "__main__":
    if cmds.window("test_win", exists=True):
        cmds.deleteUI("test_win")
    win = cmds.window("test_win")
    cmds.showWindow(win)
    test = MainUI(win, "test_win", create=True)
