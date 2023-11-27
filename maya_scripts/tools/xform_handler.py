import maya.cmds as cmds
from tools.select_cmds import selection_check


def xform_attributes():
    attributes = {
        'rotation': (False, {'x': None, 'y': None, 'z': None}),
        'translation':  (False, {'x': None, 'y': None, 'z': None}),
        'joint_orient':  (False, {'x': None, 'y': None, 'z': None}),
        'scale':  (False, {'x': None, 'y': None, 'z': None})
    }
    return attributes


def apply_threshold(value, threshold=1e-5):
    """
    Apply a threshold to a value to consider very small values as zero.

    :param value: The value to check against the threshold.
    :param threshold: The threshold below which values are considered as zero.
    :return: The original value if above the threshold, otherwise zero.
    """
    if abs(value) > threshold:
        return value
    return 0


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
                    cmds.setAttr(f"{obj}.{value}{axis}", 0)
                    strange_count += 1
    if strange_count:
        cmds.warning(f"Fixed {strange_count} strange values.")
    else:
        cmds.warning("No strange values found.")


def set_xform_values(**kwargs):
    selected_objects = kwargs.get("objects") if kwargs.get("objects") else selection_check.check_selection()
    if type(selected_objects) is not list:
        selected_objects = [selected_objects]
    if not selected_objects:
        raise ValueError("No objects selected.")

    options = kwargs.get("options") if kwargs.get("options") else xform_attributes()

    rotation, translation, joint_orient, scale = options.values()

    for obj in selected_objects:
        print(f"set_xform_values for loop-----{obj}")
        if rotation[0]:
            cmds.setAttr(f"{obj}.rotateX", apply_threshold(rotation[1]['x']))
            cmds.setAttr(f"{obj}.rotateY", apply_threshold(rotation[1]['y']))
            cmds.setAttr(f"{obj}.rotateZ", apply_threshold(rotation[1]['z']))
        if translation[0]:
            cmds.xform(obj, worldSpace=True, translation=(
                apply_threshold(translation[1]['x']),
                apply_threshold(translation[1]['y']),
                apply_threshold(translation[1]['z'])
            ))
        if joint_orient[0]:
            cmds.setAttr(f"{obj}.jointOrientX", apply_threshold(joint_orient[1]['x']))
            cmds.setAttr(f"{obj}.jointOrientY", apply_threshold(joint_orient[1]['y']))
            cmds.setAttr(f"{obj}.jointOrientZ", apply_threshold(joint_orient[1]['z']))
        if scale[0]:
            cmds.setAttr(f"{obj}.scaleX", apply_threshold(scale[1]['x']))
            cmds.setAttr(f"{obj}.scaleY", apply_threshold(scale[1]['y']))
            cmds.setAttr(f"{obj}.scaleZ", apply_threshold(scale[1]['z']))


def get_xform_values(**kwargs):
    selected_objects = kwargs.get("objects") if kwargs.get("objects") else selection_check.check_selection()
    if type(selected_objects) is not list:
        selected_objects = [selected_objects]
    if not selected_objects:
        raise ValueError("No objects selected.")

    options = kwargs.get("options") if kwargs.get("options") else xform_attributes()
    rotation, translation, joint_orient, scale = options.values()

    for obj in selected_objects:
        if rotation[0]:
            world_rot = cmds.xform(obj, query=True, worldSpace=True, rotation=True)
            rotation[1]['x'] = apply_threshold(world_rot[0]) if world_rot and world_rot[0] is not None else 0
            rotation[1]['y'] = apply_threshold(world_rot[1]) if world_rot and world_rot[1] is not None else 0
            rotation[1]['z'] = apply_threshold(world_rot[2]) if world_rot and world_rot[2] is not None else 0
        if translation[0]:
            world_trans = cmds.xform(obj, query=True, worldSpace=True, translation=True)
            translation[1]['x'] = apply_threshold(world_trans[0]) if world_trans and world_trans[0] is not None else 0
            translation[1]['y'] = apply_threshold(world_trans[1]) if world_trans and world_trans[1] is not None else 0
            translation[1]['z'] = apply_threshold(world_trans[2]) if world_trans and world_trans[2] is not None else 0
        if joint_orient[0]:
            joint_orient[1]['x'] = apply_threshold(cmds.getAttr(f"{obj}.jointOrientX")) if cmds.getAttr(f"{obj}.jointOrientX") is not None else 0
            joint_orient[1]['y'] = apply_threshold(cmds.getAttr(f"{obj}.jointOrientY")) if cmds.getAttr(f"{obj}.jointOrientY") is not None else 0
            joint_orient[1]['z'] = apply_threshold(cmds.getAttr(f"{obj}.jointOrientZ")) if cmds.getAttr(f"{obj}.jointOrientZ") is not None else 0
        if scale[0]:
            scale[1]['x'] = apply_threshold(cmds.getAttr(f"{obj}.scaleX")) if cmds.getAttr(f"{obj}.scaleX") is not None else 0
            scale[1]['y'] = apply_threshold(cmds.getAttr(f"{obj}.scaleY")) if cmds.getAttr(f"{obj}.scaleY") is not None else 0
            scale[1]['z'] = apply_threshold(cmds.getAttr(f"{obj}.scaleZ")) if cmds.getAttr(f"{obj}.scaleZ") is not None else 0
    if kwargs.get("return_dict"):
        return options
    return rotation, translation, joint_orient, scale


def add_to_xform_values(obj, attribute=None, x=0, y=0, z=0):
    if not attribute:
        raise ValueError("No attribute specified.")
    if not any([x, y, z]):
        raise ValueError("No values specified.")
    if attribute not in xform_attributes():
        raise ValueError(f"Invalid attribute: {attribute}")

    cmds.xform(obj, relative=True, **{attribute: [x, y, z]})


def match_xform(match_obj=None, objs_to_match=None, rotation=False, translation=False, joint_orient=False, scale=False):
    if not match_obj:
        match_obj = selection_check.check_selection()[0]
    if not objs_to_match:
        objs_to_match = selection_check.check_selection()[1:]


    attrs = xform_attributes()
    if rotation:
        attrs['rotation'] = (True, {'x': None, 'y': None, 'z': None})
    if translation:
        attrs['translation'] = (True, {'x': None, 'y': None, 'z': None})
    if joint_orient:
        attrs['joint_orient'] = (True, {'x': None, 'y': None, 'z': None})
    if scale:
        attrs['scale'] = (True, {'x': None, 'y': None, 'z': None})
    values_to_match = get_xform_values(options=attrs, objects=match_obj, return_dict=True)
    set_xform_values(options=values_to_match, objects=objs_to_match)
