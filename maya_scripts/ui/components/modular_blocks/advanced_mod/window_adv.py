import maya.cmds as cmds
from abc import ABC, abstractmethod
from ui.components.modular_blocks.basic_mod.window_base import BaseUI


class MainUI(BaseUI, ABC):
    def __init__(self, parent_ui: str | None, name: str, tool_name: str, type: str, width=100, height=50, **kwargs):
        super_args = [name, width, height]
        # SUPER: self.name, self.readable_name, self.window_width, self.window_height
        super_kwargs = self.get_kwargs_for_super(kwargs)
        super().__init__(*super_args, **super_kwargs)

        self.ui = None
        self.parent_ui = parent_ui
        self.tool_name = tool_name
        self.type = type

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
            self._window_setup()

    def _setup_secondary_ui(self):
        match self.type:
            case option if option in ["tab", "tabs", "t"]:
                return self._tab_type()
            case _:
                return self._tab_type()

    @staticmethod
    def get_kwargs_for_super(kwargs):
        options = [
            "create", "cr", "c",
            "maximize", "max", "mx",
            "minimize", "min", "mn",
            "resize", "r", "fit",
            "f", "dock", "d",
            "test", "t"
        ]
        return {key: kwargs[key] for key in kwargs if key not in options}

    def _default_type(self):
        return self.window
    
    def _tab_type(self):
        return cmds.tabLayout(f"{self.name}_tab", innerMarginWidth=5, innerMarginHeight=5)

    def _window_setup(self):
        self.ui = self._setup_secondary_ui()
        self._ui_setup(self.parent_ui, self.tool_name)
        self.show()

    @abstractmethod
    def _ui_setup(self, parent_ui: str | None, tool: str) -> str: ...
