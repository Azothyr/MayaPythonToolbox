import maya.cmds as cmds
from ui.components.modular_blocks import FrameBase


class MainUI(FrameBase):
    def __init__(self, parent_ui: str, name="Description", **kwargs):
        # Variables
        self.name = self._parse_init_name(name, before_super=True)
        self.text = kwargs.get("text", kwargs.get("t", "Default Desscription"))
        self.secondary_color = kwargs.get("secondary_color", kwargs.get("s_color", kwargs.get("sc", [0.3, 0.3, 0.3])))

        # Sub UIs
        self.section = f"{self.name}_section"

        # Sub UI Components
        self.text_block = f"{self.name}_text_block"
        super_args = [parent_ui, name]
        super().__init__(*super_args, **kwargs)

    def __call__(self, description: str):
        self.update(description)

    def _create_frame(self):
        super()._create_frame()

    def _setup_main_ui(self):
        cmds.columnLayout(self.section, adjustableColumn=True, width=self.width, p=self.frame)

    def _setup_ui_components(self):
        self.text_block = cmds.text(self.text_block, p=self.section, font="smallPlainLabelFont",
                                    backgroundColor=self.secondary_color)

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
    test = MainUI(
        win,
        "test_win",
        label="Bold Test Frame",
        font="boldLabelFont",
        width=100,
        height=10,
        border=True,
        marginWidth=5,
        marginHeight=5,
        visible=True,
        collapsable=True,
        collapsed=True,
        title_color=[0.6, 0.5, 0.6],
        secondary_color=[0, 0.3, 0],
        annotation="This is a test frame.",
        create=True)
    test("This is a test")
