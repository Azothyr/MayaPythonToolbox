import maya.cmds as cmds


def initialization_check(window_name):
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
