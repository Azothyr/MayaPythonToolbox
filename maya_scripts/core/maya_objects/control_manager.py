import maya.cmds as cmds


class Main:
    def __init__(self, name: str = None):
        self.group, self.control = self._split_to_control_and_group(control_objects)

    @staticmethod
    def _split_to_control_and_group(_object):
        if cmds.objectType(_object) != "transform":
            raise ValueError(f"ERROR: Incorrect object type for {_object}. Expected 'transform', got {cmds.objectType(_object)}.")

        if _object.lower().endswith("_ctrl"):
            return cmds.listRelatives(_object, parent=True, type="transform")[0], _object
        elif _object.lower().endswith("_grp"):
            return _object, cmds.listRelatives(_object, children=True, type="transform")[0]

        raise ValueError(f"ERROR: {_object} does not end with '_Ctrl' or '_Grp'.")
