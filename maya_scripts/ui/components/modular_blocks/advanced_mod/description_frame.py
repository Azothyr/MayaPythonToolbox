import maya.cmds as cmds
from ui.components.modular_blocks.basic_mod.form_base import BaseUI


class MainUI(BaseUI):
    def __init__(self, parent_ui: str, width=300, **kwargs):
        name = "Description"
        super_args = [parent_ui, name, width]
        super_kwargs = {"collapsed": True, "collapsable": True, "label": "Description"}
        # SUPER: self.name, self.readable_name, self.window_width, self.form, self.frame, self.parent_ui
        super().__init__(*super_args, **super_kwargs)

        # Sub UIs
        self.section = f"{self.name}_section"

        # Sub UI Components
        self.text_block = f"{self.name}_text_block"
        self.text = "Default Desscription" if kwargs.get("text", kwargs.get("t", False)) else\
            kwargs.get("text", kwargs.get("t"))

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
            self._create_ui()

    def __call__(self, description: str):
        self.text = description
        self.update()

    def _setup_main_ui(self):
        cmds.columnLayout(self.section, adjustableColumn=True, p=self.frame)

    def _setup_ui_components(self):
        self.text_block = cmds.text(self.text_block, p=self.section, font="smallPlainLabelFont", backgroundColor=[0, 0, 0])

    def _update_text(self):
        self.text_block = cmds.text(self.text_block, edit=True, label=self.text)

    def update(self, text=None, *_):
        self.text = text if text else self.text
        self._update_text()

    def set(self, text: str):
        self.text = text
        self._update_text()


if __name__ == "__main__":
    if cmds.window("test_win", exists=True):
        cmds.deleteUI("test_win")
    win = cmds.window("test_win")
    cmds.showWindow(win)
    test = MainUI(win, "test_win", create=True)
    test("This is a test")
