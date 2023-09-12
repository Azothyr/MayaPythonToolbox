import maya.cmds as cmds
from maya_scripts.tools import xform_handler
from maya_scripts.tools import select_cmds
from maya_scripts.tools import mirror_cmds


def pass_to_func(func, *args, **kwargs):
    func(*args, **kwargs)


if __name__ == "__main__":
    # pass_to_func(xform_handler.set_xform_values, rotation=True, x=0)
    # pass_to_func(select_cmds.select_all_hierarchy())
    """
    pass_to_func(select_cmds.select_chain()
    pass_to_func(xform_handler.check_strange_values())
    """
    # pass_to_func(mirror_cmds.mirror_controls())

    sels = cmds.ls(sl=True)
    parent_ctrls = sels[0]
    child_ctrl = sels[1]
    child_ctrl_grp = cmds.listRelatives(child_ctrl, parent=True)[0]

    p_contraint1 = cmds.parentConstraint(mo=True, skipRotate=["x", "y", "z"], weight=1)[0]
    p_contraint2 = cmds.parentConstraint(mo=True, skipRotate=["x", "y", "z"], weight=1)[0]

    cmds.addAttr(child_ctrl, ln='FollowTranslate', at='double', min=0, max=1, dv=1)
    cmds.setAttr('%s.FollowTranslate' % (child_ctrl), e=True, keyable=True)
    cmds.addAttr(child_ctrl, ln='FollowRotate', at='double', min=0, max=1, dv=1)
    cmds.setAttr('%s.FollowRotate' % (child_ctrl), e=True, keyable=True)

    cmds.connectAttr('%s.FollowTranslate' % (child_ctrl), '%s.w0' % (p_contraint1), f=True)
    cmds.connectAttr('%s.FollowRotate' % (child_ctrl), '%s.w0' % (p_contraint2), f=True)
    pass
