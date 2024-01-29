import maya.cmds as cmds
from ui.components.modular_blocks import FrameBase


class MainUI(FrameBase):
    def __init__(self, parent_ui: str, name: str, default=None, align_text="center", ui_align="center",
                 **kwargs):
        self.name = self._parse_init_name(name, before_super=True)

        # Variables
        self.text = str(default) if default else None

        # Sub UIs
        self.section = f"{self.name}_section"
        self.columns = f"{self.name}_columns"

        # Sub UI Components
        self.input = f"{self.name}_input"
        self.label = f"{self.name}_label"
        self.column_align = ui_align
        self.align_text = align_text

        super_args = [parent_ui, name]
        super().__init__(*super_args, **kwargs)

    def get(self):
        return cmds.textField(self.input, query=True, text=True)

    def _create_frame(self):
        super()._create_frame()

    def _setup_main_ui(self):
        col_width = int(self.width / 2)

        self.section = cmds.columnLayout(self.section, adjustableColumn=True, p=self.frame)
        self.columns = cmds.rowColumnLayout(self.columns, numberOfColumns=2,
                                            columnWidth=[(1, col_width), (2, col_width)],
                                            columnAlign=[1, self.column_align],
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
