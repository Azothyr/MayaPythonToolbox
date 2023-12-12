import maya.cmds as cmds


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
        end_time = self.time_interval * 6 + 1
        for attr in self.get_ctrl_shape_attrs():
            keyframes = cmds.keyframe(attr, q=True, time=(0, end_time))
            if keyframes:
                cmds.cutKey(attr, time=(keyframes[0], keyframes[-1]))


if __name__ == "__main__":
    obj = "Pelvis_FK_Ctrl"
    rem_obj = lambda obj_name, fallback: cmds.objExists(obj_name) and obj_name or fallback
    rem_obj = rem_obj("Pelvis_FK_Ctrl", obj)
    to_remove = rem_obj if cmds.objExists(rem_obj) else obj if cmds.objExists(obj) else None

    tool = WeightPaintHelper(obj="Pelvis_FK_Ctrl", translation_amount=100)
    WeightPaintHelper(obj=to_remove, mode="rem").remove_keyframes()
