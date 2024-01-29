import maya.cmds as cmds
from abc import ABC, abstractmethod


class BaseUI(ABC):
    def __init__(self, name: str, **kwargs):
        # Variables
        name = name.lower()
        if " " in name:
            name = name.replace(" ", "_").lower()

        self.name = name
        self.readable_name = name.replace("_", " ").title()
        self.window_width = kwargs.get("width", kwargs.get("w", 500))
        self.window_height = kwargs.get("height", kwargs.get("h", 300))
        self.allow_maximize = kwargs.get("maximize", kwargs.get("max", kwargs.get("m", False)))
        self.allow_minimize = kwargs.get("minimize", kwargs.get("min", kwargs.get("mn", True)))
        self.allow_resize = kwargs.get("resize", kwargs.get("r", False))
        self.fit_children = kwargs.get("fit", kwargs.get("f", False))
        self.dockable = kwargs.get("dock", kwargs.get("d", False))

        # Top level UI
        self.window = f"{name}_ui_window"
        self.window_base = f"{name}_ui_base"

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
            self._window_setup()
            self._ui_setup()
            self.show()

    def __call__(self):
        self._window_setup()
        self.show()

    def _check_window(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window)

    def show(self):
        cmds.showWindow(self.window)

    @abstractmethod
    def _window_setup(self):
        self._check_window()
        self.window = cmds.window(
            self.window,
            t=self.readable_name,
            widthHeight=(self.window_width, self.window_height),
            maximizeButton=False,
            minimizeButton=self.allow_minimize,
            resizeToFitChildren=self.fit_children,
            nestedDockingEnabled=self.dockable,
            sizeable=self.allow_resize)
        self.window_base = cmds.columnLayout(self.window_base, adjustableColumn=True, p=self.window)

    @abstractmethod
    def _ui_setup(self):
        self.update_window_size()

    def update_window_size(self):
        debug = False
        if not cmds.columnLayout(self.window_base, exists=True):
            if debug:
                print(f"Base layout {self.window_base} does not exist.")
            return

        children = cmds.columnLayout(self.window_base, query=True, childArray=True) or []
        total_height = 0
        for child in children:
            if cmds.layout(child, exists=True):
                height = cmds.layout(child, query=True, height=True)
                if height:
                    total_height += height
                else:
                    if debug:
                        print(f"No height could be queried for {child}.")
            else:
                if debug:
                    print(f"Child {child} does not exist.")

        cmds.window(self.window, edit=True, height=total_height)


class TestUI(BaseUI):
    def _window_setup(self):
        super()._window_setup()

    def _ui_setup(self):
        print("UI Setup Done")


if __name__ == "__main__":
    test = TestUI("test", create=True)
