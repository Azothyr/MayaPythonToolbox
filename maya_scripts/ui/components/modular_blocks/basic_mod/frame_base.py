import maya.cmds as cmds
from abc import ABC, abstractmethod


class BaseUI(ABC):
    def __init__(self, parent_ui: str, frame_name: str, **kwargs):
        """
        Initializes a BaseUI class that handles custom actions for creating and handling a frame layout in maya with
        the specified parameters and optional keyword arguments.

        :type parent_ui: Str
        :param parent_ui: The parent UI element name.
        :type frame_name: Str
        :param frame_name: The name of the frame.
        :type kwargs: Dict
        :param kwargs: A dictionary of additional keyword arguments:
        :keyword label (str): The label text of the frame. Defaults to the readable name of the frame.:
        :keyword font (str): Font style for the label. Default is 'smallPlainLabelFont'.
        :keyword width (int): Width of the frame. Default is 300.
        :keyword height (int): Height of the frame. Default is 300.
        :keyword border (bool): Whether to show a border. Default is True.
        :keyword marginWidth (int): The width of the margin. Default is 5.
        :keyword marginHeight (int): The height of the margin. Default is 5.
        :keyword visible (bool): Whether the frame is visible. Default is True.
        :keyword collapsable (bool): Whether the frame is collapsible. Default is False.
        :keyword collapsed (bool): Whether the frame starts off collapsed. Default is False.
        :keyword color (list[float]): Background color of the label. Default is [0.5, 0.5, 0.5].
        :keyword annotation (str): Annotation for the frame. Default is an empty string.
        :keyword create (bool): Whether to create the frame on initialization. Default is False.

        :return: None
        """
        # Variables
        self.frame: str
        self.parent: str = parent_ui
        self.name = self._parse_init_name(frame_name)
        self.readable_name = frame_name.replace("_", " ").title()
        self.label: str = self.readable_name if kwargs.get("label", kwargs.get("l", True)) else ""
        self.label_visible: bool = kwargs.get("label_visible", kwargs.get("l_vis", True))
        self.font: str = kwargs.get("font", kwargs.get("f", "smallPlainLabelFont"))
        self.width: int = kwargs.get("width", kwargs.get("w", 300))
        self.height: int = kwargs.get("height", kwargs.get("h", 300))
        self.original_width: int = self.width
        self.original_height: int = self.height
        self.border: bool = kwargs.get("border", kwargs.get("b", True))
        self.marginWidth: int = kwargs.get("marginWidth", kwargs.get("mw", 5))
        self.marginHeight: int = kwargs.get("marginHeight", kwargs.get("mh", 5))
        self.visible: bool = kwargs.get("visible", kwargs.get("v", True))
        self.collapsible: bool = kwargs.get("collapsable", False)
        self.start_collapsed: bool = kwargs.get("collapsed", False)
        self.collapse_command: callable = kwargs.get(
            "collapse_command",
            kwargs.get("cc", kwargs.get("collapse_cmd",
                                        lambda *_: self.resize(self.original_width, 25, False))))
        self.expand_command: callable = kwargs.get(
            "expand_command",
            kwargs.get("ec", kwargs.get("expand_cmd",
                                        lambda *_: self.resize(self.original_width, self.original_height, True))))
        self.current_colasped = self.start_collapsed
        self.color: list[float] = (
            kwargs.get("label_color", kwargs.get("l_color", kwargs.get("title_color", kwargs.get(
                "t_color", kwargs.get("color", kwargs.get("clr", [0.5, 0.5, 0.5]))))))
        )
        self.annotation: str = kwargs.get("annotation", kwargs.get("ann", kwargs.get("a", "")))

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
            self._create_frame()

    def __repr__(self):
        return self.name

    def __str__(self):
        attributes = []
        for attr in [
            "parent", "frame", "readable_name",
            "label", "font", "width", "height", "border",
            "marginWidth", "marginHeight", "visible",
            "collapsible", "start_collapsed", "color",
            "annotation"
        ]:
            attributes.append(f"\t{attr}: {getattr(self, attr)}")
        attributes = "\n".join(attributes)
        children = "\n".join([child for child in self._get_ui_elements()]) if self._get_ui_elements() else "None"

        return (
            f"---|  FRAME LEVEL UI: {self.frame}  |---\n"
            f"{attributes}\n"
            "----------------------------------\n"
            "---------|  CHILDREN  |-----------\n"
            f"{children}\n"
            "----------------------------------\n")

    @staticmethod
    def _parse_init_name(name: str, before_super: bool = False) -> str:
        _name = name
        if " " in name:
            _name = f"{name}".replace(" ", "_") if " " in name else f"{name}"

        if before_super:
            return _name
        else:
            if "_frame" not in name.lower():
                _name = f"{name}_frame"\
                    if "_frame" not in name.lower() and not name.lower().endswith("_frame") else name

        return _name

    def _get_ui_elements(self):
        return cmds.frameLayout(self.frame, query=True, childArray=True)

    def resize(self, width: int, height: int, set_to_orig: bool) -> bool:
        if set_to_orig:
            width = self.original_width
            height = self.original_height

        if self.collapsible or set_to_orig:
            if width < 0:
                width = 0
            if height < 0:
                height = 0
            self.width = width
            self.height = height
            cmds.frameLayout(self.frame, edit=True, width=width, height=height)
        if self.original_width != self.width or self.original_height != self.height:
            self.current_colasped = True
        else:
            self.current_colasped = False
        return self.current_colasped

    @abstractmethod
    def _create_frame(self):
        self.frame = cmds.frameLayout(
            self.name,
            label=self.label,
            labelVisible=self.label_visible,
            parent=self.parent,
            borderVisible=self.border,
            width=self.width,
            height=self.height,
            marginWidth=self.marginWidth,
            marginHeight=self.marginHeight,
            visible=self.visible,
            collapsable=self.collapsible,
            collapse=self.start_collapsed,
            backgroundColor=self.color,
            annotation=self.annotation,
            # preCollapseCommand=self.collapse_command,
            collapseCommand=self.collapse_command,
            # preExpandCommand=self.expand_command,
            expandCommand=self.expand_command,
        )
        self._setup_main_ui()
        self._setup_ui_components()

    @abstractmethod
    def _setup_main_ui(self): ...

    @abstractmethod
    def _setup_ui_components(self): ...


class TestBase(BaseUI):
    def __init__(self, name: str = "test", **kwargs):
        if cmds.window("test_win", exists=True):
            cmds.deleteUI("test_win")
        self.win = cmds.window("test_win")
        cmds.showWindow(self.win)

        self.main_col = cmds.columnLayout(adjustableColumn=True, p=self.win)

        self.name = self._parse_init_name(name, before_super=True)

        # Top Level UI
        self.col = f"{self.name}_col"

        # Sub UIs
        self.text = f"{self.name}_text"
        self.button1 = f"{self.name}_button1"
        self.button2 = f"{self.name}_button2"
        self.button3 = f"{self.name}_button3"

        super().__init__(self.main_col, name, **kwargs)

    def _create_frame(self):
        super()._create_frame()

    def _setup_main_ui(self):
        self.col = cmds.columnLayout(self.col, adjustableColumn=True, bgc=[0, 0, 0], p=self.frame)

    def _setup_ui_components(self):
        cmds.text(self.text, label="This is a test", p=self.col)
        cmds.button(self.button1, label="Test Button", bgc=[0.5, 0, 0], p=self.col)
        cmds.button(self.button2, label="Test Button 2", bgc=[0, 0.5, 0], p=self.col)
        cmds.button(self.button3, label="Test Button 3", bgc=[0, 0, 0.5], p=self.col)


if __name__ == "__main__":
    test = TestBase(
        label="Bold Test Frame",
        label_visible=True,
        font="boldLabelFont",
        width=300,
        height=100,
        border=True,
        marginWidth=5,
        marginHeight=5,
        visible=True,
        collapsable=True,
        collapsed=False,
        color=[0.6, 0.5, 0.6],
        annotation="This is a test frame.",
        create=True)

    test = cmds.columnLayout("test_col", adjustableColumn=1, bgc=[1, 1, 1], p=test.main_col)
    cmds.frameLayout("test_frame", bgc=[1, 1, 1], p=test)
    cmds.text("measuring_text", label="This is a new test", parent="test_frame")
