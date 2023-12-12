import sys

if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' in sys.path:
    sys.path.remove('C:/GitRepos/MayaPythonToolbox/maya_scripts')
if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' not in sys.path:
    sys.path.append('C:/GitRepos/MayaPythonToolbox/maya_scripts')
import maya.cmds as cmds
from pprint import pprint
# import re
from weight_paint_time_scratch import WeightPaintHelper
from tools.xform_handler import XformHandler


debug_bool = False


def debug(text: str, _debug: bool = False):
    if debug_bool or _debug:
        pprint(f"{text}")


if __name__ == "__main__":
    def module_name():
        import inspect
        import os
        # Get the current frame and find the file name of the script
        frame = inspect.currentframe()
        filename = inspect.getfile(frame)
        return os.path.basename(filename).split('.')[0]

    def select(obj):
        if cmds.objExists(obj):
            cmds.select(obj)
        else:
            cmds.select(clear=True)
            possible_objs = cmds.ls(obj)
            print(possible_objs)
            if possible_objs:
                cmds.select(possible_objs[0])
            else:
                for possible_obj in cmds.ls(f"*{obj}*"):
                    if (obj in possible_obj and "constraint" not in possible_obj.lower() and
                            "grp" not in possible_obj.lower() and "jnt" not in possible_obj.lower() and
                            "shape" not in possible_obj.lower()):
                        cmds.select(possible_obj)
                        break

    def run_tool(obj, mode="tool"):
        match mode:
            case "tool":
                tool = WeightPaintHelper(obj=obj, translation_amount=100)
            case "rem":
                WeightPaintHelper(obj=obj, mode=mode).remove_keyframes()
            case "xform":
                pass
            case "select":
                select(obj)


    debug(f"\n{'-' * 25 + '|' + ' ' * 4} RUNNING {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 25}")

    ckecker_obj = lambda obj_name, fallback: cmds.objExists(obj_name) and obj_name or fallback
    obj = "Spine_01"
    rem_obj = ckecker_obj(ckecker_obj("", obj), None)

    run_tool(obj, mode="select")

    debug(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED {module_name()}  DUNDER MAIN {' ' * 4 + '|' + '-' * 25}\n")
