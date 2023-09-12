import maya.cmds as cmds
from maya_scripts.utilities import selection_check


def xform_attributes():
    attributes = {
        'rotation': (False, {'x': None, 'y': None, 'z': None}),
        'translation':  (False, {'x': None, 'y': None, 'z': None}),
        'joint_orient':  (False, {'x': None, 'y': None, 'z': None}),
        'scale':  (False, {'x': None, 'y': None, 'z': None})
    }
    return attributes


def check_strange_values():
    objs = selection_check.check_selection()
    check = {
        'rotation': 'rotate',
        'translation': 'translate',
        'joint': 'jointOrient'
    }
    strange_count = 0
    for obj in objs:
        for key, value in check.items():
            for axis in 'XYZ':
                if 0 < cmds.getAttr(f"{obj}.{value}{axis}") < 0.01 or 0 > cmds.getAttr(f"{obj}.{value}{axis}") < -0.01:
                    print(f"{obj}.{value}{axis} = {cmds.getAttr(f'{obj}.{value}{axis}')}")
                    cmds.setAttr(f"{obj}.{value}{axis}", 0)
                    strange_count += 1
    if strange_count:
        cmds.warning(f"Fixed {strange_count} strange values.")
    else:
        cmds.warning("No strange values found.")


def set_xform_values(**kwargs):
    selected_objects = selection_check.check_selection()

    options = xform_attributes()

    for key, value in kwargs.items():
        if key in options:
            options[key] = (True, value)

    rotation, translation, joint_orient, scale = options.values()

    for obj in selected_objects:
        if rotation[0]:
            cmds.setAttr(f"{obj}.rotateX", rotation[1]['x'])
            cmds.setAttr(f"{obj}.rotateY", rotation[1]['y'])
            cmds.setAttr(f"{obj}.rotateZ", rotation[1]['z'])
        if translation[0]:
            cmds.setAttr(f"{obj}.translateX", translation[1]['x'])
            cmds.setAttr(f"{obj}.translateY", translation[1]['y'])
            cmds.setAttr(f"{obj}.translateZ", translation[1]['z'])
        if joint_orient[0]:
            cmds.setAttr(f"{obj}.jointOrientX", joint_orient[1]['x'])
            cmds.setAttr(f"{obj}.jointOrientY", joint_orient[1]['y'])
            cmds.setAttr(f"{obj}.jointOrientZ", joint_orient[1]['z'])
        if scale[0]:
            cmds.setAttr(f"{obj}.scaleX", scale[1]['x'])
            cmds.setAttr(f"{obj}.scaleY", scale[1]['y'])
            cmds.setAttr(f"{obj}.scaleZ", scale[1]['z'])


def get_xform_values(**kwargs):
    selected_objects = selection_check.check_selection()

    options = xform_attributes()

    for key, value in kwargs.items():
        if key in options:
            options[key] = (True, value)

    rotation, translation, joint_orient, scale = options.values()

    for obj in selected_objects:
        if rotation[0]:
            rotation[1]['x'] = cmds.getAttr(f"{obj}.rotateX")
            rotation[1]['y'] = cmds.getAttr(f"{obj}.rotateY")
            rotation[1]['z'] = cmds.getAttr(f"{obj}.rotateZ")
        if translation[0]:
            translation[1]['x'] = cmds.getAttr(f"{obj}.translateX")
            translation[1]['y'] = cmds.getAttr(f"{obj}.translateY")
            translation[1]['z'] = cmds.getAttr(f"{obj}.translateZ")
        if joint_orient[0]:
            joint_orient[1]['x'] = cmds.getAttr(f"{obj}.jointOrientX")
            joint_orient[1]['y'] = cmds.getAttr(f"{obj}.jointOrientY")
            joint_orient[1]['z'] = cmds.getAttr(f"{obj}.jointOrientZ")
        if scale[0]:
            scale[1]['x'] = cmds.getAttr(f"{obj}.scaleX")
            scale[1]['y'] = cmds.getAttr(f"{obj}.scaleY")
            scale[1]['z'] = cmds.getAttr(f"{obj}.scaleZ")
    return rotation, translation, joint_orient
