import maya.cmds as cmds
from maya_scripts.components.color_library import ColorIndex


def change_color(_color, obj_lyst):
    library = ColorIndex()
    if isinstance(_color, str):
        color_index = library.get_cvalue_from_color(_color)
    elif isinstance(_color, int):
        color_index = library.get_color_from_index(_color)
    else:
        raise TypeError(f"Expected _color to be a string or integer, got {type(_color)} instead.")

    for obj in obj_lyst:
        if isinstance(obj, list) and len(obj) == 1:
            obj = obj[0]
        if not cmds.objExists(obj):
            print(f"{obj} does not exist in the scene.")
            continue

        shapes = cmds.listRelatives(obj, children=True, shapes=True) or [obj]
        for shape in shapes:
            connected_layers = cmds.listConnections(f"{shape}.drawOverride", destination=False) or []
            for layer in connected_layers:
                print(f"Disconnecting drawInfo of {layer} from {shape}.drawOverride.")
                cmds.disconnectAttr(f"{layer}.drawInfo", f"{shape}.drawOverride")

            cmds.setAttr(f"{shape}.overrideEnabled", lock=False)
            cmds.setAttr(f"{shape}.overrideColor", lock=False)
            cmds.setAttr(f"{shape}.overrideEnabled", 1)
            cmds.setAttr(f"{shape}.overrideColor", color_index)
