import maya.cmds as cmds
from abc import ABC, abstractmethod


class BaseUI(ABC):
    def __init__(self, parent_ui: str, form_name: str, **kwargs):
        # Variables
        self.form: str
        self.parent: str = parent_ui
        self.name: str = f"{form_name}_form".replace(" ", "_") if " " in form_name else f"{form_name}_form"
        self.readable_name = form_name.replace("_", " ").title()
        self.width: int = kwargs.get("width", kwargs.get("w", 300))
        self.height: int = kwargs.get("height", kwargs.get("h", 300))
        self.visible: bool = kwargs.get("visible", kwargs.get("v", True))
        self.form_control: str = kwargs.get("form_control", kwargs.get("fc", kwargs.get("f", "top")))
        self.color: list[float] = kwargs.get("color", kwargs.get("c", [0.5, 0.5, 0.5]))

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
            self._create_form()
            self._attach_to_form()

    @abstractmethod
    def _create_form(self):
        self.form = cmds.formLayout(
            self.name,
            width=self.width,
            height=self.height,
            bgc=[.5, .5, .5],
            p=self.parent
        )

    @abstractmethod
    def _attach_to_form(self):
        cmds.formLayout(
            self.form, edit=True,
            attachForm=[
                (self.form, self.form_control, 0),
                (self.form, "left", 0),
                (self.form, "right", 0),
                (self.form, "bottom", 0)]
        )


class TestBase(BaseUI):
    def __init__(self, parent_ui: str = "test_win", name: str = "test", **kwargs):
        if cmds.window("test_win", exists=True):
            cmds.deleteUI("test_win")
        win = cmds.window("test_win")
        cmds.showWindow(win)
        super_args = [parent_ui, name]
        super().__init__(*super_args, **kwargs)

    def _test_ui(self):
        frame = cmds.frameLayout(label="Test Frame", p=self.form)
        col = cmds.columnLayout(adjustableColumn=True, bgc=[0, 0, 0], p=frame)
        cmds.text(label="This is a test", p=col)
        cmds.button(label="Test Button", bgc=[0.5, 0, 0], p=col)
        cmds.button(label="Test Button 2", bgc=[0, 0.5, 0], p=col)
        cmds.button(label="Test Button 3", bgc=[0, 0, 0.5], p=col)
        return frame

    def _create_form(self):
        super()._create_form()
        self.test_col = self._test_ui()

    def _attach_to_form(self):
        cmds.formLayout(
            self.form, edit=True,
            attachForm=[
                (self.test_col, "top", 0),
                (self.test_col, "left", 0),
                (self.test_col, "right", 0),
                (self.test_col, "bottom", 0)]
        )


if __name__ == "__main__":
    test = TestBase(create=True)
