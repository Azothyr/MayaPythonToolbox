import maya.cmds as cmds
from custom_maya_scripts.components import color_library


def change_color(_color, obj_lyst):
    library = color_library.ColorIndex()
    color_index = library.get_cvalue_from_color(_color)

    for obj in obj_lyst:
        if cmds.nodeType(obj) == "joint":
            cmds.setAttr("%s.overrideEnabled" % obj, lock=False)
            cmds.setAttr("%s.overrideColor" % obj, lock=False)
            cmds.setAttr("%s.overrideEnabled" % obj, 1)
            cmds.setAttr("%s.overrideColor" % obj, color_index)
        else:
            shapes = cmds.listRelatives(obj, children=True, shapes=True)
            for shape in shapes:
                cmds.setAttr("%s.overrideEnabled" % shape, lock=False)
                cmds.setAttr("%s.overrideColor" % shape, lock=False)
                cmds.setAttr("%s.overrideEnabled" % shape, 1)
                cmds.setAttr("%s.overrideColor" % shape, color_index)
