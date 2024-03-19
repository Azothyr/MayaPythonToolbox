import maya.cmds as cmds
from core.maya_managers.control_manager import ControlManager
from core.maya_managers.selection_manager import Select as sl


class ControlFactory:
    def __init__(self, *args, **kwargs):
        self.radius = kwargs.get("radius", 1.0)
        if "radius" in kwargs:
            kwargs.pop("radius")
        self.selection = sl() if not args else self._process_args(args)
        self.controls = []

    def __str__(self):
        return f"Selection: {self.selection!s}\nRadius: {self.radius!s}\nControls: {self.controls!s}"

    def __call__(self):
        return self.create()

    def __iter__(self):
        if not isinstance(self.controls, list):
            if isinstance(self.controls, ControlManager):
                return iter([self.controls])
            else:
                raise TypeError(f"Expected self.controls to be a list, got {type(self.controls)} instead.")
        return iter(self.controls)

    @staticmethod
    def _process_args(args):
        valid_args = [arg for arg in args if isinstance(arg, str)]
        return sl(valid_args)

    def create(self, objects: list[str] = None):
        if not objects:
            objects = self.selection
        objects = objects if len(objects) > 1 else [objects] if isinstance(objects, str) else self.selection
        if not objects:
            raise ValueError("ERROR: No objects to create controls from!")

        self.controls = []
        for obj in objects:
            new_control = ControlManager(obj, radius=self.radius, match=True, create=True)
            self.controls.append(new_control)

        return self.controls


if __name__ == "__main__":
    controls = ControlFactory(radius=5)()
    print(controls)

    # created_ctrls = controls()
    # print(created_ctrls)
