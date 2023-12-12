import maya.cmds as cmds
from pprint import pprint


debug_bool = True


def debug(text: str, _debug: bool = False, pretty: bool = False):
    if debug_bool or _debug:
        if pretty:
            pprint(f"{text}")
        else:
            print(f"{text}")


class WeightPaintHelper:
    def __init__(self, obj=None, rotation_plane='yz', translate_axis='x', rotation_amount=50, translation_amount=5,
                 time_interval=15, mode="run"):
        self.obj = self.get_ctrl_shape(obj)
        self.rotation_amount = rotation_amount
        self.translation_amount = translation_amount
        self.time_interval = time_interval
        self.rotation_plane = rotation_plane.lower()
        self.translate_axis = translate_axis.lower()

        self.__auto_run(mode)

    def __auto_run(self, mode):
        valid_modes = ["run", "remove", "rem", "tool"]

        match mode.lower().strip():
            case "run":
                self.set_keyframes_for_weight_painting()
            case "remove":
                self.remove_keyframes()
            case "rem":
                self.remove_keyframes()
            case "tool":
                return
            case _:
                valid_modes = "\n".join(valid_modes)
                raise RuntimeError(f"Invalid mode: {mode}\n Valid modes: {valid_modes}")

    @staticmethod
    def get_ctrl_shape(obj):
        if obj is None:
            obj = cmds.ls(selection=True)[0]
        if not obj:
            raise RuntimeError("No object selected.")
        cmds.select(clear=True)
        possible_objs = cmds.ls(obj)
        debug(f"Found objects: {possible_objs}")
        if possible_objs:
            obj = possible_objs[0]
        else:
            possible_objs = cmds.ls(f"*{obj}*")
            debug(f"Searching through: {possible_objs}")
            for possible_obj in possible_objs:
                debug(f"Possible object: {possible_obj}")
                if (obj in possible_obj and "constraint" not in possible_obj.lower() and
                        "grp" not in possible_obj.lower() and "jnt" not in possible_obj.lower() and
                        "shape" not in possible_obj.lower()):
                    obj = possible_obj
                    debug(f"Found object: {obj}")
                    break
        if not cmds.objExists(obj):
            raise RuntimeError(f"Object does not exist: {obj}")
        return obj

    def get_ctrl_shape_attrs(self):
        for attr in self.rotation_plane:
            yield f"{self.obj}.r{attr}"
        yield f"{self.obj}.t{self.translate_axis}"

    def _set_keyframes(self, primary_attr):
        for attr in self.get_ctrl_shape_attrs():
            if attr != primary_attr:
                cmds.setAttr(attr, 0)
            cmds.setKeyframe(attr)

    def set_keyframes_for_weight_painting(self):
        time = 0
        cmds.currentTime(time)
        self._set_keyframes("NO PRIMARY ATTR")
        time += self.time_interval

        for attr in self.get_ctrl_shape_attrs():
            if attr.split(".")[1].startswith("r"):
                for i in range(3):
                    cmds.currentTime(time)
                    if i == 0:
                        cmds.setAttr(attr, self.rotation_amount)
                    elif i == 1:
                        cmds.setAttr(attr, -1 * self.rotation_amount)
                    else:
                        cmds.setAttr(attr, 0)
                    self._set_keyframes(attr)
                    time += self.time_interval
            elif attr.split(".")[1].startswith("t"):
                for i in range(1):
                    cmds.currentTime(time)
                    if i == 0:
                        cmds.setAttr(attr, self.translation_amount)
                    else:
                        cmds.setAttr(attr, 0)
                    self._set_keyframes(attr)
                    time += self.time_interval
        time = 0
        cmds.currentTime(time)

    def remove_keyframes(self):
        end_time = self.time_interval * 10 + 1
        for attr in self.get_ctrl_shape_attrs():
            keyframes = cmds.keyframe(attr, q=True, time=(0, end_time))
            if keyframes:
                cmds.cutKey(attr, time=(keyframes[0], keyframes[-1]))


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
            debug(f"{possible_objs}")
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
    obj = "spine_01".capitalize()
    rem_obj = ckecker_obj(ckecker_obj("", obj), None)

    run_tool(obj, mode="tool")
    #run_tool(obj, mode="select")
    # run_tool(obj, mode="rem")

    debug(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED {module_name()}  DUNDER MAIN {' ' * 4 + '|' + '-' * 25}\n")