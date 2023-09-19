import maya.cmds as cmds
from maya_scripts.tools import xform_handler
from maya_scripts.tools import select_cmds
from maya_scripts.tools import mirror_cmds
from maya_scripts.utilities.arg_lib_reader import LibReader as Reader
from maya_scripts.components.window_base import WindowBase as Window
from maya_scripts.ui import main_win_tab
from maya_scripts.utilities import cmds_class_builder as class_builder


def pass_to_func(func, *args, **kwargs):
    func(*args, **kwargs)


def broken_fk():
    """
    Select the parent and then the child
    """
    sels = cmds.ls(sl=True)
    leader = sels[0]
    follower = sels[1]
    follower_grp = cmds.listRelatives(follower, parent=True)[0]

    rotate_contraint = cmds.parentConstraint(mo=True, skipTranslate=["x", "y", "z"], weight=1)[0]
    translate_contraint = cmds.parentConstraint(mo=True, skipRotate=["x", "y", "z"], weight=1)[0]
    scale_contraint = cmds.scaleConstraint(mo=False, offset=[1, 1, 1], weight=1)[0]

    cmds.addAttr(follower, ln='FollowTranslate', at='double', min=0, max=1, dv=1)
    cmds.setAttr('%s.FollowTranslate' % follower_grp, e=True, keyable=True)
    cmds.addAttr(follower, ln='FollowRotate', at='double', min=0, max=1, dv=1)
    cmds.setAttr('%s.FollowRotate' % follower_grp, e=True, keyable=True)

    # connect the child's attribute to the rotate constraint weight 0
    cmds.connectAttr('%s.FollowTranslate' % follower, '%s.w0' % translate_contraint, f=True)
    # connect the attribute to the translation constraint weight 0
    cmds.connectAttr('%s.FollowRotate' % follower, '%s.w0' % rotate_contraint, f=True)


def constraint_remover():
    def remove_constraints_from_hierarchy(node):
        """
        Recursively remove constraints from the given node and its descendants.

        Args:
            node (str): The node to start from.
        """

        # List all the constraints attached to the node.
        constraints = cmds.listRelatives(node, type='constraint')

        # If there are constraints, delete them.
        if constraints:
            for constraint in constraints:
                cmds.delete(constraint)

        # Check children and continue the process recursively.
        children = cmds.listRelatives(node, children=True, fullPath=True)
        if children:
            for child in children:
                remove_constraints_from_hierarchy(child)

    # Get all selected objects.
    selected_objects = cmds.ls(selection=True,
                               long=True)  # Using long=True ensures full path names, which is useful when dealing with hierarchies.

    # Iterate over selected objects and remove constraints from the hierarchy.
    for obj in selected_objects:
        remove_constraints_from_hierarchy(obj)


if __name__ == "__main__":
    # pass_to_func(main_win_tab.create_tools_menu())
    # pass_to_func(xform_handler.set_xform_values, rotation=True, x=0)
    constraint_remover()
    """
    pass_to_func(select_cmds.select_chain()
    pass_to_func(xform_handler.check_strange_values())
    """
    # pass_to_func(mirror_cmds.mirror_controls())

    # make spring IK for quadrapeds
