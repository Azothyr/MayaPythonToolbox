import maya.cmds as cmds
from abc import ABC, abstractmethod


class BaseUI(ABC):
    def __init__(self, parent_ui: str, name: str, width=300, **kwargs):
        # Variables
        self.name = name
        self.readable_name = name.replace("_", " ").capitalize()
        self.window_width = width

        # Top level UI
        self.form = f"ui_form_{name}"
        self.frame = f"frame_{name}"
        self.parent_ui = parent_ui
        self.collapsible: bool = kwargs.get("collapsible", False)
        self.start_collapsed: bool = kwargs.get("collapsed", False)

    def _create_ui(self):
        cmds.formLayout(
            self.form,
            bgc=[.5, .5, .5],
            p=self.parent_ui
        )
        cmds.frameLayout(
            self.frame,
            label=self.readable_name,
            collapsable=self.collapsible,
            collapse=self.start_collapsed,
            parent=self.form
        )
        self._setup_main_ui()
        self._setup_ui_components()

    @abstractmethod
    def _setup_main_ui(self): ...

    @abstractmethod
    def _setup_ui_components(self): ...
