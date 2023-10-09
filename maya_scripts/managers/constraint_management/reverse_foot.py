import maya.cmds as cmds


def set_driven_key(driver, driven, driver_attr, driver_values, driven_values, tangent='spline',
                   pre_infinity='linear', post_infinity='linear'):
    for dv, ddv in zip(driver_values, driven_values):
        # Set the driver attribute to the respective value
        if not cmds.objExists(f"{driven}"):
            raise ValueError(f"Object or attribute {driven} does not exist!")
        # print(f"Setting {driver}.{driver_attr} to {dv}")
        cmds.setAttr(f"{driver}.{driver_attr}", dv)

        # Set the driven keyframe
        # print(f"Setting driven keyframe for {driven} at {dv} to {ddv}, with {tangent} tangent.")
        cmds.setDrivenKeyframe(
            f"{driven}",
            cd=f"{driver}.{driver_attr}",
            driverValue=dv, value=ddv,
            inTangentType=tangent, outTangentType=tangent
        )

    # Reset the driver attribute to default (0)
    cmds.setAttr(f"{driver}.{driver_attr}", 0)

    cmds.setInfinity(f"{driven}", preInfinite=pre_infinity, postInfinite=post_infinity)


def hard_code_reverse_foot(driver_dict, attr_list):
    for driver, frame_data in driver_dict.items():
        if frame_data is None:
            raise ValueError(f"Driver {driver} is not a valid foot control!")
        driven = None
        keyframe_data = None
        keyframe_tangent_group = None
        inf_keyframe_group = None
        # print(f"Processing {driver} with {frame_data} data.")
        for _attr, _attr_info in attr_list.items():
            driven = _attr_info.get("attr", None)

            keyframe_data = _attr_info.get(frame_data, None)
            keyframe_tangent_group = _attr_info.get("tangents", None)
            inf_keyframe_group = _attr_info.get("infinity", None)

            if driven is None or keyframe_data is None or keyframe_tangent_group is None or inf_keyframe_group is None:
                raise ValueError(f"Attribute {_attr} is missing required data!")
            # print(f"DATA {keyframe_data}")

            if isinstance(driven, list):
                for i in range(len(driven)):
                    driven_to_process = driven[i]
                    driven_to_process = driven_to_process.format(driver[0])
                    # print(f"DRIVER: {driver}----{driver[0]} DRIVEN: {driven_to_process}")
                    amount_to_parse = len(keyframe_data)
                    for j in range(amount_to_parse):
                        attr_value = keyframe_data[j][0]
                        driven_value = keyframe_data[j][i + 1]
                        pre_inf = inf_keyframe_group[j][i][0]
                        post_inf = inf_keyframe_group[j][i][1]
                        key_tangent = keyframe_tangent_group[j][i]

                        # print(f"\n I: {i}, J: {j} SETTING: {driver}-{_attr}"
                        #       f"\n\tFRAME: ({attr_value})---to {driven[i]}---({driven_value})"
                        #       f"\n\tTANGENT: {key_tangent}"
                        #       f"\n\tPRE & POST INFINITY:{pre_inf},  {post_inf}")
                        set_driven_key(driver, driven_to_process, _attr, [attr_value], [driven_value],
                                       tangent=key_tangent, pre_infinity=pre_inf, post_infinity=post_inf)

            else:
                if len(keyframe_data) != len(keyframe_tangent_group) or len(keyframe_data) != len(inf_keyframe_group):
                    raise ValueError(f"Keyframe data for {_attr} does not match the number of tangents or infinity "
                                     f"values!")
                driven = driven.format(driver[0])
                for i in range(len(keyframe_data)):
                    attr_value = keyframe_data[i][0]
                    driven_value = keyframe_data[i][1]
                    pre_inf = inf_keyframe_group[i][0]
                    post_inf = inf_keyframe_group[i][1]
                    key_tangent = keyframe_tangent_group[i]

                    # print(f"\nSETTING: {driver}-{_attr}\n\tFRAME: {attr_value} to {driven} {driven_value}"
                    #       f"\n\tTANGENT: {keyframe_tangent_group[i]}\n\tPRE & POST INFINITY:{inf_keyframe_group[i]}")
                    set_driven_key(driver, driven, _attr, [attr_value], [driven_value],
                                   tangent=key_tangent, pre_infinity=pre_inf, post_infinity=post_inf)
        # print(f"End of Processing {driver} with {frame_data} data.")


def attribute_exists(node, attribute):
    return cmds.attributeQuery(attribute, node=node, exists=True)


def delete_attr_nodes(node, attr):
    """
    Deletes unitConversion nodes connected to a specific attribute of a given node.
    """
    attr_connections = cmds.listConnections(f"{node}.{attr}", type="unitConversion")
    check_against = []
    to_remove = []

    selection = cmds.ls(type="unitConversion")
    for node in selection:
        connections = cmds.listConnections(node)
        for conn in connections:
            cmds.listConnections(conn)
            if "unitConversion" in conn or "blendWeighted" in conn or "animCurveUU" in conn or "animCurveUA" in conn \
                    or "animCurveUL" in conn or "animCurveUT" in conn:
                check_against.append(conn)
                # print(f"NODE {conn} with connections {cmds.listConnections(conn)}")
        # print(f"NODE {node} with connections {connections}")
        if "unitConversion" in node or "blendWeighted" in node or "animCurveUU" in node or "animCurveUA" in node \
                or "animCurveUL" in node or "animCurveUT" in node:
            check_against.append(node)

    # printing = '\n'.join([f"{k}, {v}" for k, v in enumerate(check_against)])
    # print(f"Processing {printing}")
    # print(cmds.ls(type="unitConversion")) if cmds.ls(type="unitConversion") else print("No unitConversion nodes left.")
    # print('\n'.join([f"{k}, {v}" for k, v in enumerate(cmds.ls(type="unitConversion"))]))

    for obj in attr_connections:
        if obj in check_against:
            to_remove.append(obj)

    if not to_remove:
        return  # No unitConversion nodes connected

    for obj in to_remove:
        # Disconnect all connections this node is part of, then delete the node
        cmds.disconnectAttr(obj)
        cmds.delete(obj)

    # print(f"Removed {len(to_remove)} unitConversion nodes.")
    cmds.deleteAttr(f"{node}.{attr}")


def create_driver_attr(driver, _attr_name, _attr_info, force_recreate=False):
    should_create = True
    # print(f"Creating {_attr_name} for {driver}")
    if attribute_exists(driver, _attr_name):
        # Check if the attribute's properties differ
        current_attr_type = cmds.getAttr(f"{driver}.{_attr_name}", type=True)
        current_default_value = cmds.addAttr(f"{driver}.{_attr_name}", query=True, defaultValue=True)

        desired_attr_type = _attr_info['creation_kwargs'].get('attributeType')
        desired_default_value = _attr_info['creation_kwargs'].get('defaultValue')

        if current_attr_type != desired_attr_type or current_default_value != desired_default_value or \
                force_recreate:
            # Cleanup any existing unitConversion nodes related to this attribute
            delete_attr_nodes(driver, _attr_name)
            # print(f"Deleted existing attribute {_attr_name} on {driver}")
        else:
            # print(f"Attribute {_attr_name} already exists on {driver} with the same properties. Skipping.")
            should_create = False

    if should_create:
        formatted_attr_name = _attr_name.format(driver=driver)
        # print(f"\nCreating {formatted_attr_name} for {driver}")
        cmds.addAttr(driver, longName=formatted_attr_name, **_attr_info['creation_kwargs'])


if __name__ == "__main__":
    to_set = {"L_Leg_IK_Tip_Ctrl": "left_frame_keys",
              "R_Leg_IK_Tip_Ctrl": "right_frame_keys"}

    attributes = {
        "HeelRotate":
            {"attr": "{0}_Foot_IK_Heel_Ctrl_Offset_Grp.rotateX",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [-1, 1], [1, -1]],
             "right_frame_keys": [[0, 0], [-1, 1], [1, -1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "HeelPivot":
            {"attr": "{0}_Foot_IK_Heel_Ctrl_Offset_Grp.rotateY",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [1, 1], [-1, -1]],
             "right_frame_keys": [[0, 0], [1, 1], [-1, -1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "HeelRoll":
            {"attr": "{0}_Foot_IK_Heel_Ctrl_Offset_Grp.rotateZ",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [1, -1], [-1, 1]],
             "right_frame_keys": [[0, 0], [1, -1], [-1, 1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "BallRotate":
            {"attr": "{0}_Foot_IK_Ball_Ctrl_Offset_Grp.rotateX",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [1, 1], [-1, -1]],
             "right_frame_keys": [[0, 0], [1, 1], [-1, -1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "BallPivot":
            {"attr": "{0}_Foot_IK_Ball_Ctrl_Offset_Grp.rotateY",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [1, -1], [-1, 1]],
             "right_frame_keys": [[0, 0], [1, -1], [-1, 1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "BallRoll":
            {"attr": "{0}_Foot_IK_Ball_Ctrl_Offset_Grp.rotateZ",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [-1, 1], [1, -1]],
             "right_frame_keys": [[0, 0], [-1, 1], [1, -1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "ToeRotate":
            {"attr": "{0}_Foot_IK_Toe_Ctrl_Offset_Grp.rotateX",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [1, 1], [-1, -1]],
             "right_frame_keys": [[0, 0], [1, 1], [-1, -1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "ToePivot":
            {"attr": "{0}_Foot_IK_Toe_Ctrl_Offset_Grp.rotateY",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [1, -1], [-1, 1]],
             "right_frame_keys": [[0, 0], [1, -1], [-1, 1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "ToeRoll":
            {"attr": "{0}_Foot_IK_Toe_Ctrl_Offset_Grp.rotateZ",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [-1, 1], [1, -1]],
             "right_frame_keys": [[0, 0], [-1, 1], [1, -1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "ToeTapRotate":
            {"attr": "{0}_Foot_IK_Toe_Tap_Ctrl_Offset_Grp.rotateX",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [-1, 1], [1, -1]],
             "right_frame_keys": [[0, 0], [-1, 1], [1, -1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "ToeTapPivot":
            {"attr": "{0}_Foot_IK_Toe_Tap_Ctrl_Offset_Grp.rotateY",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [1, 1], [-1, -1]],
             "right_frame_keys": [[0, 0], [1, 1], [-1, -1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "ToeTapRoll":
            {"attr": "{0}_Foot_IK_Toe_Tap_Ctrl_Offset_Grp.rotateZ",
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [1, -1], [-1, 1]],
             "right_frame_keys": [[0, 0], [1, -1], [-1, 1]],
             "tangents": ['spline', 'spline', 'spline'],
             "infinity": [('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')],
             },
        "RockFoot":
            {"attr": ["{0}_Foot_IK_In_Ctrl_Offset_Grp.rotateZ", "{0}_Foot_IK_Out_Ctrl_Offset_Grp.rotateZ"],
             "creation_kwargs": {
                 "attributeType": "float",
                 "keyable": True,
                 "defaultValue": 0,
                 "minValue": -10,
                 "maxValue": 10,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [
                 [0, 0, 0],
                 [10, 0, -60],
                 [-10, 60, 0],
             ],
             "right_frame_keys": [
                 [0, 0, 0],
                 [10, 0, -60],
                 [-10, 60, 0],
             ],
             "tangents": [
                 ('clamped', 'clamped'),
                 ('linear', 'linear'),
                 ('linear', 'linear')
             ],
             "infinity": [
                 (('linear', 'linear'), ('linear', 'linear')),
                 (('linear', 'linear'), ('linear', 'linear')),
                 (('linear', 'linear'), ('linear', 'linear')),
             ],
             },
        "FootRoll":
            {
                "attr": ["{0}_Foot_IK_Heel_Ctrl_Roll_Grp.rotateX", "{0}_Foot_IK_Ball_Ctrl_Roll_Grp.rotateX",
                         "{0}_Foot_IK_Toe_Ctrl_Roll_Grp.rotateX"],
                "creation_kwargs": {
                    "attributeType": "float",
                    "keyable": True,
                    "defaultValue": 0,
                    "readable": True,
                    "writable": True
                },
                "left_frame_keys": [
                    [0, 0, 0, 0],
                    [-10, -40, 0, 0],
                    [4, 0, 30, 0],
                    [10, 0, 0, 50]
                ],
                "right_frame_keys": [
                    [0, 0, 0, 0],
                    [-10, -40, 0, 0],
                    [4, 0, 30, 0],
                    [10, 0, 0, 50]
                ],
                "tangents": [
                    ('clamped', 'clamped', 'clamped'),  # at 0 (heel, ball, toe)
                    ('spline', 'spline', 'spline'),  # at -10
                    ('spline', 'spline', 'clamped'),  # at 4
                    ('spline', 'spline', 'spline')  # at 10
                ],
                "infinity": [
                    (('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')),  # at 0 (heel, ball, toe)
                    (('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')),  # at -10
                    (('linear', 'linear'), ('linear', 'linear'), ('linear', 'linear')),  # at 4
                    (('linear', 'linear'), ('linear', 'constant'), ('linear', 'linear'))  # at 10
                ],
            },
        "ControlVis":
            {"attr": "{0}_Foot_IK_Out_Ctrl_Grp.visibility",
             "creation_kwargs": {
                 "attributeType": "enum",
                 "enumName": "Off:On",
                 "keyable": True,
                 "defaultValue": 0,
                 "readable": True,
                 "writable": True
             },
             "left_frame_keys": [[0, 0], [1, 1]],
             "right_frame_keys": [[0, 0], [1, 1]],
             "tangents": ['linear', 'linear'],
             "infinity": [('linear', 'linear'), ('linear', 'linear')],
             },
    }

    for key in to_set:
        for attr_name, attr_info in attributes.items():
            # print(f"Creating {attr_name} for {driver}")
            # print(f"Info: {attr_info}")
            # print(f"Type: {attr_info.get('attributeType', None)}")
            # print(f"Value: {attr_info.get('defaultValue', None)}")
            create_driver_attr(key, attr_name, attr_info, force_recreate=False)

    hard_code_reverse_foot(to_set, attributes)
    print("Done!")
