import maya.cmds as cmds
from utilities import selection_check
from core.components import xform_handler, select_cmds, selection_renamer, history_cmds, parent_cmds


def mirror_controls():
    selected_controls = selection_check.check_selection()
    mirrored_controls = []
    parent_group = []

    for control in selected_controls:
        _parent = select_cmds.select_top_hierarchy(object=control)
        mirrored_control = cmds.duplicate(control, name=f"R{control[1:]}")
        parent_cmds.unparent_selected(mirrored_control)
        # cmds.delete(parent_group)
        select_cmds.replace_selection(mirrored_control)
        xform_handler.set_xform_values(scale=True, x=-1)
        mirrored_controls.extend(mirrored_control)
    select_cmds.replace_selection(mirrored_controls)
    history_cmds.freeze_delete(mirrored_controls)
    select_cmds.replace_selection(mirrored_controls)
    print("Mirrored controls.")
