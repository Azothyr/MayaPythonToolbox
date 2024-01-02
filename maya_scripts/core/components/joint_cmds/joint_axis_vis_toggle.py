import maya.cmds as cmds
from core.maya_objects.selection_manager import Select as sl


def toggle_visibility(*args):
    selection = sl().filter_selection(joints=True)
    print(selection)

    for joint_name in selection:
        display_local_axis = cmds.getAttr(joint_name + ".displayLocalAxis")
        cmds.setAttr(joint_name + ".displayLocalAxis", not display_local_axis)


if __name__ == "__main__":
    toggle_visibility()
