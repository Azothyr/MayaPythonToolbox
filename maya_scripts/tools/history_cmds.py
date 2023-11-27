import maya.cmds as cmds


def _freeze_transformations(obj):
    """
    Freezes the transformations of the specified object.
    """
    cmds.makeIdentity(obj, apply=True, translate=1, rotate=1, scale=1, normal=0)
    print(f"{obj}'s transformation frozen")


def _delete_history(obj):
    """
    Deletes the history of the specified object.
    """
    cmds.delete(obj, ch=True)
    print(f"Deleted {obj} history.")


def freeze_delete(obj_lyst):
    for obj in obj_lyst:
        _delete_history(obj)
        _freeze_transformations(obj)
    cmds.warning("Completed freezing of transforms and deleting history.")
