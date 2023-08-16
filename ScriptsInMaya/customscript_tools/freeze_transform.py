import maya.cmds as cmds


def freeze_transformations(obj_lyst):
    """
    Freezes the transformations of the specified objects.
    """
    for obj in obj_lyst:
        cmds.makeIdentity(obj, apply=True, translate=1, rotate=1, scale=1, n=0)
