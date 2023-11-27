import maya.cmds as cmds


def rig_polish():
    sel = cmds.ls(type="shape")
    controls = []
    for item in sel:
        if "CtrlShape" in item:
            controls.append(item)
    cmds.select(clear=True)
    cmds.select(controls)
    cmds.pickWalk(direction="up")
    controls = cmds.ls(selection=True)
    cmds.select(clear=True)
    for control in controls:
        cmds.setAttr(f"{control}.v", lock=True, keyable=False, channelBox=False)
        # print(f"CONTROL: {control}\n\tLOCKING AND HIDING ATTRIBUTES")

    parent_constraints = cmds.ls(type="parentConstraint")
    for constraint in parent_constraints:
        cmds.setAttr(f"{constraint}.interpType", 2)
        print(f"{constraint} set to {cmds.getAttr(f'{constraint}.interpType')}")


if __name__ == "__main__":
    def module_name():
        import inspect
        import os
        # Get the current frame and find the file name of the script
        frame = inspect.currentframe()
        filename = inspect.getfile(frame)
        return os.path.basename(filename).split('.')[0]
    print(f"{'-' * 10 + '|' + ' ' * 4} RUNNING {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 10}")
    rig_polish()
    print(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 25}")
