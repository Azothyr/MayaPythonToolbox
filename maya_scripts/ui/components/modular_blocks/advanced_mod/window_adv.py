import maya.cmds as cmds
from abc import ABC, abstractmethod
from ui.components.modular_blocks import WindowBase


class MainUI(WindowBase, ABC):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    @abstractmethod
    def _window_setup(self):
        super()._window_setup()

    @abstractmethod
    def _ui_setup(self):
        super()._ui_setup()


class TestUI(MainUI):
    def _window_setup(self):
        super()._window_setup()

    def _ui_setup(self):
        print("UI Setup Done")


if __name__ == "__main__":
    test = TestUI("test_win", width=300, height=700, create=True)
