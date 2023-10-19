import maya.cmds as cmds


def add_to_layer_preserve_color(obj, layer_name):
    if not cmds.objExists(layer_name):
        cmds.createDisplayLayer(name=layer_name)

    # Store the current color settings
    current_override_enabled = cmds.getAttr(f"{obj}.overrideEnabled")
    current_override_color = cmds.getAttr(f"{obj}.overrideColor")
    print(f"Stored color settings of {obj}: {current_override_enabled}, {current_override_color}")

    # Disconnect the drawOverride attribute
    connected_layer = cmds.listConnections(f"{obj}.drawOverride", s=True, d=False)
    if connected_layer:
        for layer in connected_layer:
            print(f"Disconnecting drawInfo of {layer} from {obj}.drawOverride.")
            cmds.disconnectAttr(f"{layer}.drawInfo", f"{obj}.drawOverride")

    # Explicitly unlock attributes
    cmds.setAttr(f"{obj}.overrideEnabled", lock=False)
    cmds.setAttr(f"{obj}.overrideColor", lock=False)

    # Check if attributes are locked or connected
    is_locked = cmds.getAttr(f"{obj}.overrideEnabled", lock=True)
    is_connected = cmds.listConnections(f"{obj}.overrideEnabled", s=True, d=False)
    print(f"Is {obj}.overrideEnabled locked? {is_locked}")
    print(f"Is {obj}.overrideEnabled connected? {is_connected}")

    # Add object to layer
    cmds.editDisplayLayerMembers(layer_name, obj)

    try:
        # Restore original color settings
        cmds.setAttr(f"{obj}.overrideEnabled", current_override_enabled)
        cmds.setAttr(f"{obj}.overrideColor", current_override_color)
    except RuntimeError as e:
        print(f"Failed to set attribute: {e}")

    # Debug print to verify if attributes are set as expected
    final_override_enabled = cmds.getAttr(f"{obj}.overrideEnabled")
    final_override_color = cmds.getAttr(f"{obj}.overrideColor")
    print(f"Final color settings of {obj}: {final_override_enabled}, {final_override_color}")


def add_list_to_layer_preserve_color(layer_name, lyst=None, type=None):
    if not lyst:
        if type:
            lyst = cmds.ls(type=type)
        else:
            lyst = cmds.ls(selection=True)
    cmds.select(clear=True)
    for item in lyst:
        add_to_layer_preserve_color(item, layer_name)


if __name__ == "__main__":
    selection = cmds.ls(selection=True)
    add_list_to_layer_preserve_color("Ctrl_Layer", lyst=selection)
