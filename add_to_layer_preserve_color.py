import maya.cmds as cmds
from functools import partial


def preserve_color_and_override(obj):
    """Preserves the color and override settings of the object."""
    current_override_enabled = cmds.getAttr(f"{obj}.overrideEnabled")
    current_override_color = cmds.getAttr(f"{obj}.overrideColor")

    return current_override_enabled, current_override_color


def restore_color_and_override(obj, enabled, color, shape=False):
    """Restores the color and override settings of the object."""
    if not shape:
        # Check if attributes are locked or connected
        obj_is_locked = cmds.getAttr(f"{obj}.overrideEnabled", lock=True)
        obj_current_color = cmds.getAttr(f"{obj}.overrideColor")
        obj_is_connected = cmds.listConnections(f"{obj}.overrideEnabled", destination=False)

        # Disconnect the drawOverride attribute
        if obj_is_connected or enabled != obj_is_locked or color != obj_current_color:
            connected_layer = cmds.listConnections(f"{obj}.drawOverride", shapes=True, destination=False)
            if connected_layer:
                for layer in connected_layer:
                    cmds.disconnectAttr(f"{layer}.drawInfo", f"{obj}.drawOverride.overrideEnabled",
                                        f"{obj}.drawOverride.overrideColor")

        cmds.setAttr(f"{obj}.overrideEnabled", enabled)
        cmds.setAttr(f"{obj}.overrideColor", color)
    else:
        shape_is_locked = cmds.getAttr(f"{obj}.overrideEnabled", lock=True)
        shape_current_color = cmds.getAttr(f"{obj}.overrideColor")
        shape_is_connected = cmds.listConnections(f"{obj}.overrideEnabled", shapes=True, destination=False)

        # Disconnect the drawOverride attribute
        if shape_is_connected or enabled != shape_is_locked or color != shape_current_color:
            shape_connected_layer = cmds.listConnections(f"{obj}.drawOverride", shapes=True, destination=False)
            if shape_connected_layer:
                for layer in shape_connected_layer:
                    cmds.disconnectAttr(f"{layer}.drawInfo", f"{obj}.drawOverride")


def is_connected(src_attr, dest_attr):
    """Check if an attribute is already connected to another attribute."""
    connections = cmds.listConnections(dest_attr, plugs=True, source=True, destination=False)
    return src_attr in connections if connections else False


def all_but_color_connect_to_layer(obj, layer_name):
    attributes_to_connect = [
        ("visibility", "overrideVisibility"),
        ("displayType", "overrideDisplayType"),
        ("levelOfDetail", "overrideLevelOfDetail"),
        ("hideOnPlayback", "hideOnPlayback"),
        ("texturing", "overrideTexturing"),
        ("shading", "overrideShading"),
        ("playback", "overridePlayback"),
    ]

    for src_suffix, dest_suffix in attributes_to_connect:
        src_attr = f"{layer_name}.drawInfo.{src_suffix}"
        dest_attr = f"{obj}.drawOverride.{dest_suffix}"

        if not is_connected(src_attr, dest_attr):
            # print(f"Connecting {src_attr} -> {dest_attr}")
            cmds.connectAttr(src_attr, dest_attr, force=True)
        else:
            print(f"Connection already exists: {src_attr} -> {dest_attr}")


def connect_joint_layer(joint, sub_layer_name):
    """Connects a sub-layer to a layer."""
    top_layer_name = "MAIN_JOINT_LAYER"
    if sub_layer_name == top_layer_name:
        return all_but_color_connect_to_layer(joint, top_layer_name)
    if not cmds.objExists(top_layer_name):
        cmds.createDisplayLayer(name=top_layer_name, noRecurse=True, empty=True)
    if not cmds.objExists(sub_layer_name):
        cmds.createDisplayLayer(name=sub_layer_name, noRecurse=True, empty=True)

    def create_node(node_type, name, **kwargs):
        cmds.shadingNode(node_type, name=name, **kwargs)

    def connect_attributes(source, from_attr, to_attr, destination, **kwargs):
        if not cmds.isConnected(f"{source}.{from_attr}", f"{destination}.{to_attr}"):
            cmds.connectAttr(f"{source}.{from_attr}", f"{destination}.{to_attr}", force=True, **kwargs)

    def set_attributes(host, attr, value, **kwargs):
        if cmds.attributeQuery(attr, node=host, exists=True):
            cmds.setAttr(f"{host}.{attr}", value, edit=True, keyable=True, **kwargs)

    def generate_nodes(name):
        _nodes = {
                f"{name}_Top_Layer_Override_Conditional": {
                    "create": partial(create_node, node_type="condition", name=f"{name}_Top_Layer_Override_Conditional",
                                      asUtility=True),
                    "set": [
                        partial(set_attributes, host=f"{name}_Top_Layer_Override_Conditional", attr="operation",
                                value=1),
                        partial(set_attributes, host=f"{name}_Top_Layer_Override_Conditional", attr="secondTerm",
                                value=0),
                    ],
                    "primary_connection": [
                        partial(connect_attributes, source=f"{sub_layer_name}", from_attr="drawInfo.displayType",
                                to_attr="colorIfFalseR", destination=f"{name}_Top_Layer_Override_Conditional"),
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.displayType",
                                to_attr="colorIfTrueR", destination=f"{name}_Top_Layer_Override_Conditional"),
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.displayType",
                                to_attr="firstTerm", destination=f"{name}_Top_Layer_Override_Conditional"),
                        partial(connect_attributes, source=f"{name}_Top_Layer_Override_Conditional",
                                from_attr="colorIfFalseR", to_attr="input[0]",
                                destination=f"{name}_Display_Type_Result_Choice"),
                        partial(connect_attributes, source=f"{name}_Top_Layer_Override_Conditional",
                                from_attr="firstTerm", to_attr="input[1]",
                                destination=f"{name}_Display_Type_Result_Choice"),
                    ],
                    "purpose": "If the Joint Layer is not actively changing the Display Type, it will allow the sub "
                               "layer to override the Display Type.",
                },
                f"{name}_Override_Zero_To_One_Clamp": {
                    "create": partial(create_node, node_type="clamp", name=f"{name}_Override_Zero_To_One_Clamp",
                                      asUtility=True),
                    "set": [
                        partial(set_attributes, host=f"{name}_Override_Zero_To_One_Clamp", attr="operation", value=1),
                        partial(set_attributes, host=f"{name}_Override_Zero_To_One_Clamp", attr="minR", value=0),
                        partial(set_attributes, host=f"{name}_Override_Zero_To_One_Clamp", attr="maxR", value=1),
                    ],
                    "primary_connection": [
                        partial(connect_attributes, source=f"{name}_Top_Layer_Override_Conditional",
                                from_attr="colorIfTrueR", to_attr="inputR",
                                destination=f"{name}_Override_Zero_To_One_Clamp"),
                        partial(connect_attributes, source=f"{name}_Override_Zero_To_One_Clamp",
                                from_attr="outputR", to_attr="selector",
                                destination=f"{name}_Display_Type_Result_Choice"),
                    ],
                    "purpose": "Forces the Top Layer's Enum output to be 0 when not active and 1 when active.",
                },
                f"{name}_Display_Type_Result_Choice": {
                    "create": partial(create_node, node_type="choice", name=f"{name}_Display_Type_Result_Choice",
                                      asUtility=True),
                    "primary_connection": [
                        partial(connect_attributes, source=f"{name}_Display_Type_Result_Choice",
                                from_attr="output", to_attr="drawOverride.overrideDisplayType", destination=f"{joint}"),
                    ],
                    "purpose": "Outputs the Top Layer's or Sub Layer's Display Type to Joint depending on which is"
                               " active.",
                },
                f"{name}_Visibility_Result_Choice": {
                    "create": partial(create_node, name=f"{name}_Visibility_Result_Choice",
                                      node_type="choice", asUtility=True),
                    "primary_connection": [
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.visibility",
                                to_attr="input[0]", destination=f"{name}_Visibility_Result_Choice"),
                        partial(connect_attributes, source=f"{sub_layer_name}", from_attr="drawInfo.visibility",
                                to_attr="input[1]", destination=f"{name}_Visibility_Result_Choice"),
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.visibility",
                                to_attr="selector", destination=f"{name}_Visibility_Result_Choice"),
                        partial(connect_attributes, source=f"{name}_Visibility_Result_Choice",
                                from_attr="output", to_attr="drawOverride.overrideVisibility", destination=f"{joint}"),
                    ],
                    "purpose": "Outputs the Top Layer's or Sub Layer's Visibility Value to Joint depending on which is"
                               " active.",
                },
                f"{name}_Hide_On_Playback_Result_Choice": {
                    "create": partial(create_node, name=f"{name}_Hide_On_Playback_Result_Choice",
                                      node_type="choice", asUtility=True),
                    "primary_connection": [
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.hideOnPlayback",
                                to_attr="input[0]", destination=f"{name}_Hide_On_Playback_Result_Choice"),
                        partial(connect_attributes, source=f"{sub_layer_name}", from_attr="drawInfo.hideOnPlayback",
                                to_attr="input[1]", destination=f"{name}_Hide_On_Playback_Result_Choice"),
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.hideOnPlayback",
                                to_attr="selector", destination=f"{name}_Hide_On_Playback_Result_Choice"),
                        partial(connect_attributes, source=f"{name}_Hide_On_Playback_Result_Choice",
                                from_attr="output", to_attr="drawOverride.hideOnPlayback", destination=f"{joint}"),
                    ],
                    "purpose": "Outputs the Top Layer's or Sub Layer's Hide On Playback Value to Joint depending on"
                               " which is active.",
                },
        }
        return _nodes

    simple_connections = [
        ("levelOfDetail", "levelOfDetail"),
        ("texturing", "texturing"),
        ("shading", "shading"),
        ("playback", "playback"),
    ]

    def connect_simple(src_suffix, dest_suffix):
        src_attr = f"{top_layer_name}.drawInfo.{src_suffix}"
        dest_attr = f"{sub_layer_name}.drawInfo.{dest_suffix}"
        if not is_connected(src_attr, dest_attr):
            # print(f"Connecting {src_attr} -> {dest_attr}")
            cmds.connectAttr(src_attr, dest_attr, force=True)
        else:
            print(f"Connection already exists: {src_attr} -> {dest_attr}")

    nodes = generate_nodes(joint[:-4])
    for node_name, node_dict in nodes.items():
        node_dict["create"]()
    for node_name, node_dict in nodes.items():
        if "set" in node_dict:
            for func in node_dict["set"]:
                func()
    for node_name, node_dict in nodes.items():
        if "primary_connection" in node_dict:
            for func in node_dict["primary_connection"]:
                func()

    for src, dest in simple_connections:
        connect_simple(src, dest)


def add_object_to_layer(obj, layer_name):
    # Check if layer exists, if not create one
    if not cmds.objExists(layer_name):
        cmds.createDisplayLayer(name=layer_name, noRecurse=True, empty=True)
    relatives_list = cmds.listRelatives(obj, children=True, shapes=True)
    shape = relatives_list[0] if relatives_list else None

    s_enabled, s_color = preserve_color_and_override(shape) if shape else (None, None)
    o_enabled, o_color = preserve_color_and_override(obj)

    # Get current layer members
    current_members = cmds.editDisplayLayerMembers(layer_name, query=True) or []

    # Check if the object is already in the layer
    if obj in current_members:
        print(f"{obj} is already in {layer_name}.")
        return 0

    # Add object to layer
    if cmds.objectType(obj) == "joint":
        # print(f"RUNNING DOWN JOINT PATH FOR {obj}")
        connect_joint_layer(obj, layer_name)
    elif "CtrlShape" in obj:
        # print(f"RUNNING DOWN NURBSCURVE PATH FOR {obj}")
        all_but_color_connect_to_layer(obj, layer_name)
    elif "CtrlShape" in shape:
        # print(f"RUNNING DOWN NURBSCURVE PATH FOR {shape}")
        all_but_color_connect_to_layer(shape, layer_name)
    else:
        cmds.editDisplayLayerMembers(layer_name, obj, noRecurse=True)

    # print(f"SHAPE {shape}")
    if shape is not None:
        # print(f"RUNNING DOWN SHAPE PATH FOR {obj}")
        restore_color_and_override(shape, s_enabled, s_color, shape=True)
    else:
        # print(f"RUNNING DOWN OBJECT PATH FOR {obj}")
        restore_color_and_override(obj, o_enabled, o_color)
    return 1  # Return 1 to signify the object was added


def get_current_members_of_layer(layer_name):
    """Returns current members of a specified layer."""
    return cmds.editDisplayLayerMembers(layer_name, query=True) or []


def add_list_to_layer(layer_name, object_list=None):
    if object_list is None:
        object_list = cmds.ls(selection=True)

    added_count = 0
    for obj in object_list:
        added_count += add_object_to_layer(obj, layer_name)

    print(f"-----_____-----\nAdded {added_count} objects to {layer_name}.\n-----_____-----")


def print_list(list_to_print):
    to_print = "\n".join(list_to_print)
    print(to_print)


def walk_up(select_type=None):
    if select_type is None:
        raise ValueError("select_type cannot be None.")
    selection = cmds.ls(type=select_type)
    cmds.select(selection)
    cmds.pickWalk(direction="up")
    result = cmds.ls(selection=True)
    cmds.select(clear=True)
    return result


def set_geo_layer():
    selection = walk_up("mesh")
    print_list(selection)
    add_list_to_layer("Geo_Layer", object_list=selection)


def set_joint_layer():
    def set_dynamic_display_order():
        # Define the layers in their desired priority
        layer_priority = [
            'MAIN_JOINT_LAYER',
            'RK_Jnt_Sub_Layer',
            'IK_Jnt_Sub_Layer',
            'FK_Jnt_Sub_Layer'
        ]

        # Collect existing displayOrders and sort them
        existing_orders = []
        for layer in layer_priority:
            if cmds.objExists(layer):
                existing_order = cmds.getAttr(f"{layer}.displayOrder")
                existing_orders.append(existing_order)
            else:
                print(f"Warning: {layer} does not exist in the scene.")

        existing_orders.sort()

        # If the list is empty, we start our displayOrder from 1
        if not existing_orders:
            existing_orders = [0]

        # Set the new displayOrders based on priority
        for i, layer in enumerate(layer_priority):
            if cmds.objExists(layer):
                new_order = existing_orders[0] + i + 1
                cmds.setAttr(f"{layer}.displayOrder", new_order)

    exclude_list = ["COG", "Clav", "Pelvis", "Spine", "Head"]

    selection = cmds.ls(type="joint")
    ik_joints = []
    fk_joints = []
    rk_joints = []
    center_joints = []
    remaining_joints = []

    for joint in selection:
        if any(value in joint for value in exclude_list):
            print(f"Excluding {joint} from Joint_Layer.")
            center_joints.append(joint)
            add_object_to_layer(joint, "MAIN_JOINT_LAYER")
        elif "RK" in joint or "Hand" in joint or "Finger" in joint:
            print(f"Adding {joint} to RK_Jnt_Sub_Layer.")
            rk_joints.append(joint)
            connect_joint_layer(joint, "RK_Jnt_Sub_Layer")
        elif "IK" in joint:
            print(f"Adding {joint} to IK_Jnt_Sub_Layer.")
            ik_joints.append(joint)
            connect_joint_layer(joint, "IK_Jnt_Sub_Layer")
        elif "FK" in joint:
            print(f"Adding {joint} to FK_Jnt_Sub_Layer.")
            fk_joints.append(joint)
            connect_joint_layer(joint, "FK_Jnt_Sub_Layer")
        else:
            print(f"Adding {joint} to Joint_Layer.")
            remaining_joints.append(joint)
            add_object_to_layer(joint, "MAIN_JOINT_LAYER")

    print("\nCenter Joints:")
    print_list(center_joints)
    print("\nIK Joints:")
    print_list(ik_joints)
    print("\nFK Joints:")
    print_list(fk_joints)
    print("\nRK Joints:")
    print_list(rk_joints)
    print("\nRemaining Joints:")
    print_list(remaining_joints)

    set_dynamic_display_order()


def set_ctrl_layer():
    selection = walk_up("nurbsCurve")
    print_list(selection)
    add_list_to_layer("Control_Layer", object_list=selection)


if __name__ == "__main__":
    set_geo_layer()
    set_joint_layer()
    set_ctrl_layer()
