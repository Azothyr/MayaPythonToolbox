import maya.cmds as cmds
from core.maya_managers.selection_manager import Select as sl


def _single_renamer(new_name, obj):
    """
    Renames selected object
    """
    print(obj)
    print(new_name)
    cmds.rename(obj, new_name)
    cmds.select(clear=True)
    cmds.select(new_name, replace=True)
    return list(new_name)


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


def perform_rename(txt, selection=None) -> list[str]:
    """
    Renames selected objects.
    :param txt:
    :param selection:
    :return new_names (list[str]):
    """
    sl(selection)
    if len(selection) > 1 and "#" not in txt:
        txt = txt + "##"
    if "#" in txt:
        new_names = _sequential_renamer(txt, selection)
    else:
        new_names = _single_renamer(txt, selection)

    return new_names


def rename_selected():
    """
    Renames selected objects.
    """
    selection = sl()
    new_name = cmds.promptDialog(
        title='Rename',
        message='Enter Name:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')
    if new_name == 'OK':
        new_name = cmds.promptDialog(query=True, text=True)
        perform_rename(new_name, selection)
