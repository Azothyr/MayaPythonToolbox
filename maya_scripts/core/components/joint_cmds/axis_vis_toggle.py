import maya.cmds as cmds
from core.maya_managers.selection_manager import Select as sl


def toggle_visibility(hierarchy=False, *args):
    selection = sl().filter_selection(joints=True)
    if not selection:
        cmds.warning("No joints selected")
        return
    if hierarchy:
        children = cmds.listRelatives(selection, ad=True, type="joint")
        if children:
            selection.extend(children)
    print(selection)

    for joint_name in selection:
        display_local_axis = cmds.getAttr(joint_name + ".displayLocalAxis")
        cmds.setAttr(joint_name + ".displayLocalAxis", not display_local_axis)


if __name__ == "__main__":
    toggle_visibility()
