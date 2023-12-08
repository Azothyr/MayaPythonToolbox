import maya.cmds as cmds


import maya.cmds as cmds


class WeightPaintHelper:
    def __init__(self, obj=None, rotation_plane='yz', translate_axis='x', rotation_amount=35, translation_amount=2,
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

    def set_keyframes_for_weight_painting(self):
        time = 0
        for attr in self.get_ctrl_shape_attrs():
            cmds.currentTime(time)
            cmds.setKeyframe(attr)

        for attr in self.get_ctrl_shape_attrs():
            if attr.split(".")[1].startswith("r"):
                print(f"TIME: {time}")
                for i in range(2):
                    print(i)
                    if i == 0:
                        cmds.setAttr(attr, self.rotation_amount)
                    elif i == 1:
                        cmds.setAttr(attr, -self.rotation_amount)
                    else:
                        cmds.setAttr(attr, 0)
                    cmds.currentTime(time)
                    cmds.setKeyframe(attr)
                    time += self.time_interval
            elif attr.split(".")[1].startswith("t"):
                for i in range(1):
                    if i == 0:
                        cmds.setAttr(attr, self.translation_amount)
                    else:
                        cmds.setAttr(attr, 0)
                    cmds.currentTime(time)
                    cmds.setKeyframe(attr)
                    time += self.time_interval


if __name__ == "__main__":
    tool = WeightPaintHelper()


'''
cmds.currentTime(0)
# Keyframe 1
cmds.currentTime(0)
cmds.setAttr(selected_obj + '.rz', 35) # noqa
cmds.setKeyframe(selected_obj)

# Keyframe 2
cmds.currentTime(15)
cmds.setAttr(selected_obj + '.rz', -35) # noqa
cmds.setKeyframe(selected_obj)

# Keyframe 3
cmds.currentTime(30)
cmds.setAttr(selected_obj + '.rz', 0) # noqa
cmds.setKeyframe(selected_obj)

# Keyframe 4
cmds.currentTime(45)
cmds.setAttr(selected_obj + '.ry', 35) # noqa
cmds.setKeyframe(selected_obj)

# Keyframe 5
cmds.currentTime(60)
cmds.setAttr(selected_obj + '.ry', -35) # noqa
cmds.setKeyframe(selected_obj)

# Keyframe 6
cmds.currentTime(75)
cmds.setAttr(selected_obj + '.ry', 0) # noqa
cmds.setKeyframe(selected_obj)

# Keyframe 7
cmds.currentTime(90)
cmds.setAttr(selected_obj + '.tx', 2) # noqa
cmds.setKeyframe(selected_obj)

# Keyframe 8
cmds.currentTime(105)
cmds.setKeyframe(selected_obj)

# Set time slider back to 0
cmds.currentTime(0)
'''