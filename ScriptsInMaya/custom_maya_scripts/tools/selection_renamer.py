import maya.cmds as cmds
from customscript_util import selection_checkas util, custom_exception as util


def _single_renamer(new_name, obj):
    """
    Renames selected object
    """
    cmds.rename(obj, new_name)
    cmds.select(clear=True)
    cmds.select(new_name, replace=True)
    return new_name


def _sequential_renamer(txt, lyst):
    """
    Renames selected objects sequentially.
    """
    count = txt.count('#')
    scheme_parts = txt.partition(count * "#")
    objects_changed = 0

    new_names = []
    for i in range(len(lyst)):
        new_name = scheme_parts[0] + str(i + 1).zfill(count) + scheme_parts[2]
        new_names.append(cmds.rename(lyst[i], new_name))
        objects_changed += 1
    cmds.select(clear=True)
    cmds.select(new_names, replace=True)
    return new_names


def rename_selection(name_schema, selection=None):
    try:
        util.check_selection(selection)
    except util.CustomException as err:
        print(err)
        if "#" in name_schema:

