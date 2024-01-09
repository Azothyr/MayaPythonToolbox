import maya.cmds as cmds
from core.maya_managers.selection_manager import Select as sl
from core.components.validate_cmds import exists_maya as exists
from core.maya_managers.control_manager import ControlManager as ctrlManager


class ControlFactory:
    def __init__(self, *args, radius=1.0, **kwargs):
        self.radius = radius
        self.selection = sl() if not args else self._process_args(args)
        self.controls = []

    def __call__(self, mode="all"):
        return self._at_selection(mode)

    def __iter__(self):
        return iter(self.selection)

    @staticmethod
    def _process_args(args):
        valid_args = [arg for arg in args if isinstance(arg, str)]
        return sl(valid_args)

    @staticmethod
    def _process_selection(orig_sel, mode):
        new_sel = []

        for name in orig_sel:
            if mode == "joint":
                if exists.joint(name):
                    processing = name.replace("Jnt", "Ctrl") if name.endswith("_Jnt") else f"{name}_Ctrl"
                    new_sel.append(processing)
                else:
                    cmds.warning(f"{name} is not a joint.")
            else:
                processing = f"{name}_Ctrl" if not name.endswith("_Ctrl") else name
                new_sel.append(processing)
        return

    def _at_selection(self, selction_type: str = None):
        selection = self.selection()
        new_sel = []
        xform_objs = []
        match selction_type.lower():
            case opt if opt in ["joint", "jnt", "j"]:
                for name in selection(joint=True):
                    processing = name.replace("Jnt", "Ctrl")
                    new_sel.append(processing)
                    xform_objs.append(name)
            case _:
                for name in selection:
                    processing = f"{name}_Ctrl" if not name.endswith("_Ctrl") else name
                    new_sel.append(processing)
                    xform_objs.append(name)
        self.controls = self._process_args(new_sel)
        return self.create(new_sel, xform_objs)

    def create(self, objects: list[str] = None, xform_objs: list[str] = None):
        objects = objects if len(objects) > 1 else [objects] if isinstance(objects, str) else self.selection
        if not objects:
            raise ValueError("ERROR: No objects to create controls from!")

        control_list = []
        for i, obj in enumerate(objects):
            new_control = ctrlManager(obj, radius=self.radius)
            control_list.append(new_control)
            if xform_objs:
                new_control.set_xform(xform_objs[i])

        return control_list


if __name__ == "__main__":
    selection = cmds.ls(sl=True)
    controls = ControlFactory(radius=5)
    controls()
