import maya.cmds as cmds
from abc import ABC, abstractmethod


class BaseUI(ABC):
    def __init__(self, name: str, width=100, height=50, **kwargs):
        # Variables
        name = name.lower()
        if " " in name:
            name = name.replace(" ", "_")

        self.name = name
        self.readable_name = name.replace("_", " ").title()
        self.window_width = width
        self.window_height = height
        self.allow_maximize = kwargs.get("maximize", kwargs.get("max", kwargs.get("m", False)))
        self.allow_minimize = kwargs.get("minimize", kwargs.get("min", kwargs.get("mn", True)))
        self.allow_resize = kwargs.get("resize", kwargs.get("r", False))
        self.fit_children = kwargs.get("fit", kwargs.get("f", False))
        self.dockable = kwargs.get("dock", kwargs.get("d", False))
        self.test = False

        # Top level UI
        self.window = None
        self.window_name = f"{name}_ui_window"

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
            self.test = kwargs.get("test", kwargs.get("t", False))
            self.create()

    def __call__(self):
        self.create()

    def _check_window(self):
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

    def show(self):
        cmds.showWindow(self.window_name)

    def create(self, *_):
        self._check_window()
        self.window = cmds.window(self.window_name,
                                  t=self.readable_name,
                                  widthHeight=(self.window_width, self.window_height),
                                  maximizeButton=False,
                                  minimizeButton=self.allow_minimize,
                                  resizeToFitChildren=self.fit_children,
                                  nestedDockingEnabled=self.dockable,
                                  sizeable=self.allow_resize)
        if self.test:
            self.__test_setup()
            return
        self._window_setup()

    def __test_setup(self): self.show()

    @abstractmethod
    def _window_setup(self): self.show()

    @abstractmethod
    def _ui_setup(self, parent_ui: str, tool: str) -> str: ...
