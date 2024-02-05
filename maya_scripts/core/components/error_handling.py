import maya.cmds as cmds


def safe_parent(child, parent):
    """
    Safely parents 'child' to 'parent', avoiding errors if 'child' is already a child of 'parent'.
    """
    # Check if 'child' is already under 'parent' to avoid redundant parenting.
    current_parent = cmds.listRelatives(child, parent=True)
    if current_parent and cmds.ls(current_parent[0], long=True)[0] == cmds.ls(parent, long=True)[0]:
        print(f"Warning: Object, '{child}', skipped. It is already a child of the parent, '{parent}'.")
        return
    try:
        cmds.parent(child, parent)
    except RuntimeError as e:
        print(f"Error: {e}")


def safe_delete(obj, **kwargs):
    """
    Safely deletes 'obj', avoiding errors if 'obj' does not exist or is already deleted.
    """
    if not cmds.objExists(obj):
        print(f"Warning: Object, '{obj}', does not exist. Skipping deletion.")
        return
    try:
        cmds.delete(obj, **kwargs)
    except RuntimeError as e:
        print(f"Error: {e}")


def safe_get_parent(obj):
    try:
        return cmds.listRelatives(obj, parent=True)
    except ValueError as e:
        print(f"Error: {e}")
        if "More than one object" in str(e):
            handle_naming_conflicts(obj)
        return None


def safe_get_children(obj):
    try:
        return cmds.listRelatives(obj, children=True)
    except ValueError as e:
        print(f"Error: {e}")
        if "More than one object" in str(e):
            handle_naming_conflicts(obj)
        return None


def handle_naming_conflicts(name: str):
    """
    Renames 'name' to 'name_1' if 'name' already exists in the scene.

    :param name: Str, name of the conflicting objects.
    """
    conflicting_objects = cmds.ls(name, long=True)
    if len(conflicting_objects) > 1:
        for i, name in enumerate(conflicting_objects):
            print(f"Renaming {name} to {name}_{i + 1}")
            cmds.rename(name, f"{name}_{i + 1}")


def safe_select(obj, **kwargs):
    """
    Safely selects 'obj', avoiding errors if 'obj' does not exist.
    """
    if not cmds.objExists(obj):
        print(f"Warning: Object, '{obj}', does not exist. Skipping selection.")
        return
    try:
        cmds.select(obj, **kwargs)
    except RuntimeError as e:
        print(f"Error: {e}")
