import maya.cmds as cmds


def freeze_transformations(data):
    """
    Freezes the transformations of the specified objects.
    """
    for obj in data:
        cmds.makeIdentity(obj, apply=True, translate=1, rotate=1, scale=1, n=0)
