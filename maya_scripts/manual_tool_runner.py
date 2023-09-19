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


if __name__ == "__main__":
    pass_to_func(main_win_tab.create_tools_menu())
    # pass_to_func(xform_handler.set_xform_values, rotation=True, x=0)
    # pass_to_func(select_cmds.select_all_hierarchy())
    """
    pass_to_func(select_cmds.select_chain()
    pass_to_func(xform_handler.check_strange_values())
    """
    # pass_to_func(mirror_cmds.mirror_controls())
    def broken_fk():
        """
        Select the parent and then the child
        """
        sels = cmds.ls(sl=True)
        constrainer = sels[0]  # parent
        constrainee = sels[1]  # child
        constrainee_grp = cmds.listRelatives(constrainee, parent=True)[0]

        rotate_contraint = cmds.parentConstraint(mo=True, skipTranslate=["x", "y", "z"], weight=1)[0]
        translate_contraint = cmds.parentConstraint(mo=True, skipRotate=["x", "y", "z"], weight=1)[0]
        scale_contraint = cmds.scaleConstraint(mo=False, offset=[1, 1, 1], weight=1)[0]

        cmds.addAttr(constrainee, ln='FollowTranslate', at='double', min=0, max=1, dv=1)
        cmds.setAttr('%s.FollowTranslate' % (constrainee), e=True, keyable=True)
        cmds.addAttr(constrainee, ln='FollowRotate', at='double', min=0, max=1, dv=1)
        cmds.setAttr('%s.FollowRotate' % (constrainee), e=True, keyable=True)

        # connect the child's attribute to the rotate constraint weight 0
        cmds.connectAttr('%s.FollowTranslate' % (constrainee), '%s.w0' % (translate_contraint), f=True)
        # connect the attribute to the translation constraint weight 0
        cmds.connectAttr('%s.FollowRotate' % (constrainee), '%s.w0' % (rotate_contraint), f=True)


    # make spring IK for quadrapeds

    class_builder.main(name=input("What will the name of this class be?"))
