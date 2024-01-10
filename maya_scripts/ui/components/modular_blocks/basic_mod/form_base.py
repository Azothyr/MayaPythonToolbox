import maya.cmds as cmds
from abc import ABC, abstractmethod


class BaseUI(ABC):
    def __init__(self, parent_ui: str, name: str, width=300, **kwargs):
        # Variables
        name = name.lower()
        if " " in name:
            name = name.replace(" ", "_")

        self.name = name
        self.readable_name = name.replace("_", " ").title()
        self.window_width = width

        # Top level UI
        self.form = f"ui_form_{name}"
        self.frame = f"frame_{name}"
        self.parent_ui = parent_ui
        self.collapsible: bool = kwargs.get("collapsable", False)
        self.start_collapsed: bool = kwargs.get("collapsed", False)
        self.frame_label = self.readable_name if kwargs.get("label", kwargs.get("l", False)) else ""

    def _create_ui(self):
        l_vis_state = True if self.frame_label and self.frame_label != "" else False
        cmds.formLayout(
            self.form,
            bgc=[.5, .5, .5],
            p=self.parent_ui
        )
        cmds.frameLayout(
            self.frame,
            label=self.frame_label,
            labelVisible=l_vis_state,
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
