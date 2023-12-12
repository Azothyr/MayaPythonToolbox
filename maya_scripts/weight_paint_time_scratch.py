import maya.cmds as cmds


class WeightPaintHelper:
    def __init__(self, obj=None, rotation_plane='yz', translate_axis='x', rotation_amount=50, translation_amount=10,
                 time_interval=15):
        self.obj = self.get_ctrl_shape(obj)
        self.rotation_amount = rotation_amount
        self.translation_amount = translation_amount
        self.time_interval = time_interval
        self.rotation_plane = rotation_plane.lower()
        self.translate_axis = translate_axis.lower()

        self.set_keyframes_for_weight_painting()

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
    tool = WeightPaintHelper()
    tool.remove_keyframes()
