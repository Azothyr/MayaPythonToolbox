import maya.cmds as cmds
from pprint import pprint
# import re
# from weight_paint_time_scratch import WeightPaintHelper
from components.xform_handler import XformHandler

debug_bool = False


def debug(text: str, _debug: bool = False, pretty: bool = False):
    if debug_bool or _debug:
        if pretty:
            pprint(f"{text}")
        else:
            print(f"{text}")


class WeightPaintHelper:
    @staticmethod
    def preset(preset_name, pose=None):
        presets = {
            "torso": {
                "rotation_plane": "yz",
                "translate_axis": "x",
                "rotation_amount": [0, 50, -50, 0, 50, -50],
                "translation_amount": -100,
                "time_interval": 15,
                "mode": "run",
                "include": ["ctrl"],
                "exclude": ["grp", "constraint", "jnt", "shape"],
            },
            "neck": {
                "rotation_plane": "yz",
                "translate_axis": "x",
                "rotation_amount": [0, 30, -30, 0, 30, -30],
                "translation_amount": 100,
                "time_interval": 15,
                "mode": "run",
                "include": ["ctrl"],
                "exclude": ["grp", "constraint", "jnt", "shape"],
            },
            "leg": {
                "rotation_plane": "xyz",
                "translate_axis": "x",
                "rotation_amount": [0, -30, 30, 0, 50, -15, 0, 45, -45],
                "translation_amount": 100,
                "time_interval": 10,
                "mode": "run",
                "include": ["ctrl"],
                "exclude": ["grp", "constraint", "jnt", "shape"],
            },
            "foot": {
                "rotation_plane": "xyz",
                "translate_axis": "y",
                "rotation_amount": [0, -25, 30, 0, 50, -15, 0, 40, -40],
                "translation_amount": -100,
                "time_interval": 10,
                "mode": "run",
                "include": ["ctrl"],
                "exclude": ["grp", "constraint", "jnt", "shape"],
            },
            "clav": {
                "rotation_plane": "yz",
                "translate_axis": "x",
                "rotation_amount": [0, -20, 30, 0, 35, -35],
                "translation_amount": 100,
                "time_interval": 10,
                "mode": "run",
                "include": ["ctrl"],
                "exclude": ["grp", "constraint", "jnt", "shape"],
            },
            "arm": {
                "rotation_plane": "yz",
                "translate_axis": "x",
                "rotation_amount": [0, -5, 5, 0, 90, -10],
                "translation_amount": 100,
                "time_interval": 10,
                "mode": "run",
                "include": ["ctrl"],
                "exclude": ["grp", "constraint", "jnt", "shape"],
            },
            "wrist": {
                "rotation_plane": "xyz",
                "translate_axis": "x",
                "rotation_amount": [0, -90, 90, 0, -90, 90, 0, 80, -80],
                "translation_amount": 100,
                "time_interval": 10,
                "mode": "run",
                "include": ["ctrl"],
                "exclude": ["grp", "constraint", "jnt", "shape"],
            },
            "finger": {
                "rotation_plane": "yz",
                "translate_axis": "x",
                "rotation_amount": [0, -60, 60, 0, 40, -40],
                "translation_amount": 100,
                "time_interval": 10,
                "mode": "run",
                "include": ["ctrl"],
                "exclude": ["grp", "constraint", "jnt", "shape"],
            },
            "thumb": {
                "rotation_plane": "xyz",
                "translate_axis": "x",
                "rotation_amount": [0, -25, 30, 0, 50, -15, 0, 40, -40],
                "translation_amount": 100,
                "time_interval": 10,
                "mode": "run",
                "include": ["ctrl"],
                "exclude": ["grp", "constraint", "jnt", "shape"],
            },
        } if pose is None or "t" in pose.lower() else {}

        other_identifiers = {
            "pelvis": "torso",
            "spine": "torso",
            "hip": "torso",
            "shoulder": "clav",
            "head": "neck",
            "hand": "wrist",
        }


        preset_name = preset_name.lower()
        if preset_name in other_identifiers.keys():
            preset_name = other_identifiers[preset_name]
        if preset_name not in presets.keys():
            raise RuntimeError(f"Preset not found: {preset_name}")
        return presets[preset_name]

    def __init__(self, control=None, skin=None, pose=None, preset=None, rotation_plane=None, translate_axis=None,
                 rotation_amount=None, translation_amount=None, time_interval=None, mode="run", include=None,
                 exclude=None):
        print(f"control: {control}\n")

        match control.lower():
            case "l_arm_03":
                preset = "hand"
            case "l_finger_01":
                preset = "thumb"
            case "l_finger_01_knuckle_01":
                preset = "thumb"
            case "l_finger_01_knuckle_02":
                preset = "thumb"
            case "l_finger_01_knuckle_03":
                preset = "thumb"
            case "l_finger_01_knuckle_03":
                preset = "thumb"
            case "l_leg_clav":
                preset = "leg"
        if preset is None:
            include = include if include is not None else ["ctrl"]
            exclude = exclude if exclude is not None else ["grp", "constraint", "jnt", "shape"]
            self.control = self.get_maya_obj(control, include=include, exclude=exclude)
            self.rotation_amount = rotation_amount if rotation_amount is not None else self.preset('torso')[
                'rotation_amount']
            self.translation_amount = translation_amount if translation_amount is not None else self.preset('torso')[
                'translation_amount']
            self.time_interval = time_interval if time_interval is not None else self.preset('torso')['time_interval']
            self.rotation_plane = rotation_plane.lower() if rotation_plane is not None else self.preset('torso')[
                'rotation_plane']
            self.translate_axis = translate_axis.lower() if translate_axis is not None else self.preset('torso')[
                'translate_axis']
            self.side = 1
        else:
            preset = self.preset(preset, pose=pose)
            self.control = self.get_maya_obj(control, include=preset['include'], exclude=preset['exclude'])
            self.rotation_amount = preset['rotation_amount']
            self.translation_amount = preset['translation_amount']
            self.time_interval = preset['time_interval']
            self.rotation_plane = preset['rotation_plane'].lower()
            self.translate_axis = preset['translate_axis'].lower()
            self.side = -1 if "r_" in self.control.lower() else 1

        self.__auto_run(mode)

        if skin is not None:
            self.skin = self.get_maya_obj(skin)
            cmds.select(self.skin)

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
    def get_maya_obj(obj: str, include=None, exclude=None):
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
                test_obj = obj.lower()
                test_possible = possible_obj.lower()
                if test_obj in test_possible:
                    if exclude is not None:
                        if any([exclude in test_possible for exclude in exclude]):
                            continue
                    if include is not None:
                        if any([include in test_possible for include in include]):
                            obj = possible_obj
                            debug(f"Found object: {obj}")
                            break
                        elif include is None:
                            obj = possible_obj
                            debug(f"Found object: {obj}")
                            break
        if not cmds.objExists(obj):
            raise RuntimeError(f"Object does not exist: {obj}")
        return obj

    def get_ctrl_assist_attrs(self, all=False):
        if all:
            self.rotation_plane = "xyz"
            self.translate_axis = "xyz"
            for attr in self.rotation_plane:
                yield f"{self.control}.r{attr}"
            for attr in self.translate_axis:
                yield f"{self.control}.t{attr}"
        else:
            for attr in self.rotation_plane:
                yield f"{self.control}.r{attr}"
            yield f"{self.control}.t{self.translate_axis}"

    def _set_keyframes(self, primary_attr):
        for attr in self.get_ctrl_assist_attrs():
            if attr != primary_attr:
                cmds.setAttr(attr, 0)
            cmds.setKeyframe(attr)

    def set_keyframes_for_weight_painting(self):
        rotations = ([0, self.rotation_amount * self.side, -1 * self.rotation_amount * self.side]
                     * len(self.rotation_plane)) if isinstance(self.rotation_amount, (int, float)) else\
            self.rotation_amount

        rotate_1 = rotations[:3]
        rotate_2 = rotations[3:6]
        rotate_3 = rotations[6:9]
        debug(f"{len(rotations)}\n{rotate_1}\n{rotate_2}\n{rotate_3}\n")

        time = 0
        cmds.currentTime(time)
        # self._set_keyframes("Initial 0 matrix")
        # time += self.time_interval
        count = 0
        for attr in self.get_ctrl_assist_attrs():
            if attr.split(".")[1].startswith("r"):
                for i in range(3):
                    cmds.currentTime(time)
                    if count == 0:
                        cmds.setAttr(attr, rotate_1[i])
                    elif count == 1:
                        cmds.setAttr(attr, rotate_2[i])
                    elif count == 2:
                        cmds.setAttr(attr, rotate_3[i])
                    else:
                        time -= self.time_interval + 1
                        cmds.setAttr(attr, 0)
                    self._set_keyframes(attr)
                    time += self.time_interval
                count += 1
            elif attr.split(".")[1].startswith("t"):
                for i in range(2):
                    cmds.currentTime(time)
                    if i == 1:
                        cmds.setAttr(attr, self.translation_amount)
                    else:
                        cmds.setAttr(attr, 0)
                    self._set_keyframes(attr)
                    time += self.time_interval
        time = 0
        cmds.currentTime(time)

    def remove_keyframes(self):
        cmds.currentTime(0)
        end_time = self.time_interval * 100 + 1
        for attr in self.get_ctrl_assist_attrs(all=True):
            keyframes = cmds.keyframe(attr, q=True, time=(-10, end_time))
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
                        return possible_obj


    def select_all_ctrls(key=None):
        key = key.lower()
        cmds.select(clear=True)
        if key is None:
            key = "ctrl"
        for obj in cmds.ls("*"):
            if key in obj.lower():
                cmds.select(obj, add=True)


    def run_tool(obj, skin=None, preset=None, pose=None, mode="tool"):
        match mode:
            case "tool":
                WeightPaintHelper(control=obj, skin=skin, preset=preset, pose=pose, translation_amount=100)
                debug("---WEIGHT PAINT PROCESS COMPLETE---\n")
            case "rem":
                debug(f"Removing keyframes for: {obj}")
                WeightPaintHelper(control=obj, mode=mode).remove_keyframes()
                cmds.select(clear=True)
                debug("---REMOVE PROCESS COMPLETE---\n")
            case "xform":
                pass
            case "select":
                select(obj)
                debug("---SELECT PROCESS COMPLETE---\n")


    l_spacer = "-" * 25 + "|" + " " * 4
    r_spacer = " " * 4 + "|" + "-" * 25
    debug(f"\n{l_spacer} RUNNING {module_name()} DUNDER MAIN {r_spacer}")

    ckecker_obj = lambda obj_name, fallback: select(obj_name) and obj_name or fallback

    # for finger in range(2, 6):
    #     knuckle = "_".join([i.capitalize() for i in f"l_finger_0{finger}_knuckle_02".split("_")])
    #     # run_tool(knuckle, "Proxy_Skin_Geo", mode="tool", preset=knuckle.split("_")[0] if knuckle.split("_")[0] not in ("L", "R") else knuckle.split("_")[1])
    #     run_tool(knuckle, "Proxy_Skin_Geo", mode="rem")

    obj = "_".join([i.capitalize() for i in "l_arm_02".split("_")])
    rem_obj = ckecker_obj(ckecker_obj("_".join([i.capitalize() for i in "l_arm_02".split("_")]), obj),
                          None)

    # run_tool(obj, mode="select")
    run_tool(rem_obj, mode="rem")
    # run_tool(obj, "Proxy_Skin_Geo", mode="tool", preset=obj.split("_")[0] if obj.split("_")[0] not in ("L", "R") else obj.split("_")[1])
    # select_all_ctrls("Head")
    # cmds.select(clear=True)

    debug(f"\n{l_spacer} COMPLETED {module_name()} DUNDER MAIN {r_spacer}")
