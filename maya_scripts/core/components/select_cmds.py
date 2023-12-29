import maya.cmds as cmds
from utilities import selection_check


def __selection():
    return selection_check.check_selection()


def replace_selection(obj):
    clear_selection()
    if len(obj) > 1:
        for item in obj:
            cmds.select(item, add=True)
    else:
        cmds.select(obj, add=True)


def clear_selection():
    cmds.select(clear=True)


def select_all_children():
    selected_objects = __selection()
    for obj in selected_objects:
        children = cmds.listRelatives(obj, allDescendents=True)
        cmds.select(children, add=True)
    cmds.select(selected_objects[0], add=True)


def select_parent():
    selected_objects = __selection()
    clear_selection()
    for obj in selected_objects:
        parent = cmds.listRelatives(obj, parent=True)
        cmds.select(parent, add=True)


def select_top_hierarchy(**kwargs):
    selected_object = kwargs.get('object', __selection())
    if not isinstance(selected_object, str):
        select_top_multi(error="ERROR: select_top_hierarchy only works with a single object selected.")
    parent = cmds.listRelatives(selected_object, parent=True)
    while parent:
        prev_parent = parent
        parent = cmds.listRelatives(parent, parent=True)
    cmds.select(prev_parent, replace=True)


def select_top_multi(**kwargs):
    error = kwargs.get('error', "ERROR: select_top_multi only works with multiple objects selected.")
    selected_objects = __selection()
    if not isinstance(selected_objects, list):
        raise TypeError(error)
    selection_parents = []
    for obj in selected_objects:
        replace_selection(obj)
        select_top_hierarchy()
        selection_parents.append(__selection())
    replace_selection(selection_parents)


def select_chain():
    select_top_hierarchy()
    select_all_children()
