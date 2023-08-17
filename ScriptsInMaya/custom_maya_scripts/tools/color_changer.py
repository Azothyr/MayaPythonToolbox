import maya.cmds as cmds


def _pass_color_info():
    color_options = [('Maya Default Blue', 0), ('Black', 1), ('White', 16), ('Light Grey', 3), ('Dark Grey', 2),
                     ('Red', 13), ('Dark Red', 4), ('Light Pink', 20), ('Mid Pink', 31), ('Pink', 9),
                     ('Light Yellow', 22), ('Yellow', 17), ('Dark Yellow', 25), ('Light Orange', 21),
                     ('Dark Orange', 12), ('Light Green', 27), ('Green', 23), ('Dark Green', 7),
                     ('Light Neon Green', 19), ('Neon Green', 14), ('Dark Neon Green', 26), ('Neon Blue', 18),
                     ('Light Navy Blue', 28), ('Navy Blue', 15), ('Light Blue', 29), ('Blue', 6), ('Dark Blue', 5),
                     ('Light Purple', 30), ('Dark Purple', 8), ('Light Brown', 10), ('Brown', 11), ('Golden Brown', 24)]
    return color_options


def get_color_order():
    order = []
    for color in _pass_color_info():
        order.append(color[0])
    return order


def get_color_index(color_name):
    for color, index in _pass_color_info():
        if color_name == color:
            return index


def change_color(color, obj_lyst):
    color_index = get_color_index(color)

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
