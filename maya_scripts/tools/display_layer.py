import maya.cmds as cmds
from functools import partial
from .connection_cmds import ConnectionCmds as cc

print_allowed = False


def print_list(list_to_print):
    to_print = "\n".join(list_to_print)
    print_if_allowed(f"{to_print}\n", print_allowed)


def print_if_allowed(message, allow=False):
    if allow:
        print(message)


class LayerCmds:
    @staticmethod
    def preserve_color_and_override(obj):
        # print_allowed = True
        """Preserves the color and override settings of the object."""
        current_override_enabled = cmds.getAttr(f"{obj}.overrideEnabled")
        current_override_color = cmds.getAttr(f"{obj}.overrideColor")

        # Force all objects to have their overrides enabled
        if not current_override_enabled:
            cmds.setAttr(f"{obj}.overrideEnabled", True)
            current_override_enabled = True

        return current_override_enabled, current_override_color

    @staticmethod
    def restore_color_and_override(obj, enabled, color, shape=False):
        # print_allowed = True
        """Restores the color and override settings of the object."""
        if not shape and "Shape" not in obj:
            print_if_allowed(f"CONFIRMED NOT A SHAPE: Restoring {obj} to {enabled} and {color}", print_allowed)
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
            print_if_allowed(f"CONFIRMED IS A SHAPE: Restoring {obj} to {enabled} and {color}", print_allowed)
            shape_is_locked = cmds.getAttr(f"{obj}.overrideEnabled", lock=True)
            shape_current_color = cmds.getAttr(f"{obj}.overrideColor")
            shape_is_connected = cmds.listConnections(f"{obj}.overrideEnabled", shapes=True, destination=False)

            # Disconnect the drawOverride attribute
            if shape_is_connected or enabled != shape_is_locked or color != shape_current_color:
                shape_connected_layer = cmds.listConnections(f"{obj}.drawOverride", shapes=True, destination=False)
                if shape_connected_layer:
                    for layer in shape_connected_layer:
                        cmds.disconnectAttr(f"{layer}.drawInfo", f"{obj}.drawOverride")

    @staticmethod
    def all_but_color_connect_to_layer(obj, layer_name):
        # print_allowed = True
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

            if not cc.is_connected(src_attr, dest_attr):
                print_if_allowed(f"Connecting {src_attr} -> {dest_attr}", print_allowed)
                cmds.connectAttr(src_attr, dest_attr, force=True)
            else:
                print_if_allowed(f"Connection already exists: {src_attr} -> {dest_attr}", print_allowed)

    @staticmethod
    def connect_joint_layer(joint, sub_layer_name):
        # print_allowed = True
        """Connects a sub-layer to a layer."""
        top_layer_name = "MAIN_JOINT_LAYER"
        if sub_layer_name == top_layer_name:
            return LayerCmds.all_but_color_connect_to_layer(joint, top_layer_name)
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

        def generate_nodes():
            # print_allowed = True
            _nodes = {
                f"Top_Layer_Override_Conditional": {
                    "create": partial(create_node, node_type="condition", name=f"Top_Layer_Override_Conditional",
                                      asUtility=True),
                    "set": [
                        partial(set_attributes, host=f"Top_Layer_Override_Conditional", attr="operation",
                                value=1),
                        partial(set_attributes, host=f"Top_Layer_Override_Conditional", attr="secondTerm",
                                value=0),
                    ],
                    "primary_connection": [
                        partial(connect_attributes, source=f"{sub_layer_name}", from_attr="drawInfo.displayType",
                                to_attr="colorIfFalseR", destination=f"Top_Layer_Override_Conditional"),
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.displayType",
                                to_attr="colorIfTrueR", destination=f"Top_Layer_Override_Conditional"),
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.displayType",
                                to_attr="firstTerm", destination=f"Top_Layer_Override_Conditional"),
                        partial(connect_attributes, source=f"Top_Layer_Override_Conditional",
                                from_attr="colorIfFalseR", to_attr="input[0]",
                                destination=f"Display_Type_Result_Choice"),
                        partial(connect_attributes, source=f"Top_Layer_Override_Conditional",
                                from_attr="firstTerm", to_attr="input[1]",
                                destination=f"Display_Type_Result_Choice"),
                    ],
                    "purpose": "If the Joint Layer is not actively changing the Display Type, it will allow the sub "
                               "layer to override the Display Type.",
                },
                f"Override_Zero_To_One_Clamp": {
                    "create": partial(create_node, node_type="clamp", name=f"Override_Zero_To_One_Clamp",
                                      asUtility=True),
                    "set": [
                        partial(set_attributes, host=f"Override_Zero_To_One_Clamp", attr="operation", value=1),
                        partial(set_attributes, host=f"Override_Zero_To_One_Clamp", attr="minR", value=0),
                        partial(set_attributes, host=f"Override_Zero_To_One_Clamp", attr="maxR", value=1),
                    ],
                    "primary_connection": [
                        partial(connect_attributes, source=f"Top_Layer_Override_Conditional",
                                from_attr="colorIfTrueR", to_attr="inputR",
                                destination=f"Override_Zero_To_One_Clamp"),
                        partial(connect_attributes, source=f"Override_Zero_To_One_Clamp",
                                from_attr="outputR", to_attr="selector",
                                destination=f"Display_Type_Result_Choice"),
                    ],
                    "purpose": "Forces the Top Layer's Enum output to be 0 when not active and 1 when active.",
                },
                f"Display_Type_Result_Choice": {
                    "create": partial(create_node, node_type="choice", name=f"Display_Type_Result_Choice",
                                      asUtility=True),
                    "primary_connection": [
                        partial(connect_attributes, source=f"Display_Type_Result_Choice",
                                from_attr="output", to_attr="drawOverride.overrideDisplayType", destination=f"{joint}"),
                    ],
                    "purpose": "Outputs the Top Layer's or Sub Layer's Display Type to Joint depending on which is"
                               " active.",
                },
                f"Visibility_Result_Choice": {
                    "create": partial(create_node, name=f"Visibility_Result_Choice",
                                      node_type="choice", asUtility=True),
                    "primary_connection": [
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.visibility",
                                to_attr="input[0]", destination=f"Visibility_Result_Choice"),
                        partial(connect_attributes, source=f"{sub_layer_name}", from_attr="drawInfo.visibility",
                                to_attr="input[1]", destination=f"Visibility_Result_Choice"),
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.visibility",
                                to_attr="selector", destination=f"Visibility_Result_Choice"),
                        partial(connect_attributes, source=f"Visibility_Result_Choice",
                                from_attr="output", to_attr="drawOverride.overrideVisibility", destination=f"{joint}"),
                    ],
                    "purpose": "Outputs the Top Layer's or Sub Layer's Visibility Value to Joint depending on which is"
                               " active.",
                },
                f"Hide_On_Playback_Result_Choice": {
                    "create": partial(create_node, name=f"Hide_On_Playback_Result_Choice",
                                      node_type="choice", asUtility=True),
                    "primary_connection": [
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.hideOnPlayback",
                                to_attr="input[0]", destination=f"Hide_On_Playback_Result_Choice"),
                        partial(connect_attributes, source=f"{sub_layer_name}", from_attr="drawInfo.hideOnPlayback",
                                to_attr="input[1]", destination=f"Hide_On_Playback_Result_Choice"),
                        partial(connect_attributes, source=f"{top_layer_name}", from_attr="drawInfo.hideOnPlayback",
                                to_attr="selector", destination=f"Hide_On_Playback_Result_Choice"),
                        partial(connect_attributes, source=f"Hide_On_Playback_Result_Choice",
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
            if not cc.is_connected(src_attr, dest_attr):
                print_if_allowed(f"Connecting {src_attr} -> {dest_attr}", print_allowed)
                cmds.connectAttr(src_attr, dest_attr, force=True)
            else:
                print_if_allowed(f"Connection already exists: {src_attr} -> {dest_attr}", print_allowed)

        nodes = generate_nodes()
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

    @staticmethod
    def add_object_to_layer(obj, layer_name):
        # print_allowed = True
        # Check if layer exists, if not create one
        if not cmds.objExists(layer_name):
            cmds.createDisplayLayer(name=layer_name, noRecurse=True, empty=True)
        relatives_list = cmds.listRelatives(obj, children=True, shapes=True)
        shape = relatives_list[0] if relatives_list else None

        s_enabled, s_color = LayerCmds.preserve_color_and_override(shape) if shape else (None, None)
        o_enabled, o_color = LayerCmds.preserve_color_and_override(obj)

        # Get current layer members
        current_members = cmds.editDisplayLayerMembers(layer_name, query=True) or []

        message = f"\n_____-----_____\n--OBJ '{obj}' -----> LAYER: '{layer_name}'\n"
        # Check if the object is already in the layer
        if obj in current_members:
            message += f"{obj} is already in {layer_name}."
            return 0

        # Add object to layer
        if cmds.objectType(obj) == "joint":
            message += f"RUNNING DOWN JOINT PATH"
            LayerCmds.connect_joint_layer(obj, layer_name)
        elif "Shape" in obj:
            message += f"RUNNING DOWN OBJECT NURBSCURVE PATH FOR {obj}"
            LayerCmds.all_but_color_connect_to_layer(obj, layer_name)
        elif shape is not None:
            if "Shape" in shape:
                message += f"RUNNING DOWN SHAPE NURBSCURVE PATH FOR {shape}"
                LayerCmds.all_but_color_connect_to_layer(shape, layer_name)
            message += f"\nSHAPE {shape}\nRUNNING DOWN OBJECT (SHAPE NOT EMPTY) PATH FOR {obj}"
            LayerCmds.restore_color_and_override(shape, s_enabled, s_color, shape=True)
        else:
            cmds.editDisplayLayerMembers(layer_name, obj, noRecurse=True)
            message += f"RUNNING DOWN OBJECT (SHAPE EMPTY) PATH FOR {obj}"
            LayerCmds.restore_color_and_override(obj, o_enabled, o_color)

        print_if_allowed(f"{message}\n-----_____-----\n", print_allowed)
        return 1  # Return 1 to signify the object was added

    @staticmethod
    def get_current_members_of_layer(layer_name):
        """Returns current members of a specified layer."""
        return cmds.editDisplayLayerMembers(layer_name, query=True) or []

    @staticmethod
    def add_list_to_layer(layer_name, object_list=None):
        # print_allowed = True
        if object_list is None:
            object_list = cmds.ls(selection=True)

        added_count = 0
        for obj in object_list:
            added_count += LayerCmds.add_object_to_layer(obj, layer_name)

        print_if_allowed(f"_____-----_____\nAdded {added_count} objects to {layer_name}.\n-----_____-----",
                         print_allowed)

    @staticmethod
    def walk_up(select_type=None):
        if select_type is None:
            raise ValueError("select_type cannot be None.")
        selection = cmds.ls(type=select_type)
        cmds.pickWalk(selection, direction="up")
        result = cmds.ls(selection=True)
        cmds.select(clear=True)
        return result
