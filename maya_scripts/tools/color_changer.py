import maya.cmds as cmds
from maya_scripts.components import color_library


def change_color(_color, obj_lyst):
    library = color_library.ColorIndex()
    if isinstance(_color, str):
        color_index = library.get_cvalue_from_color(_color)
    elif isinstance(_color, int):
        color_index = library.get_color_from_index(_color)

    for obj in obj_lyst:
        connected_layer = cmds.listConnections(f"{obj}.drawOverride", destination=False)
        if connected_layer:
            for layer in connected_layer:
                print(f"Disconnecting drawInfo of {layer} from {obj}.drawOverride.")
                cmds.disconnectAttr(f"{layer}.drawInfo", f"{obj}.drawOverride")

        if cmds.nodeType(obj) == "joint":
            cmds.setAttr(f"{obj}.overrideEnabled", lock=False)
            cmds.setAttr(f"{obj}.overrideColor", lock=False)
            cmds.setAttr(f"{obj}.overrideEnabled", 1)
            cmds.setAttr(f"{obj}.overrideColor", color_index)

        else:
            shapes = cmds.listRelatives(obj, children=True, shapes=True)
            connected_layer = cmds.listConnections(f"{shapes}.drawOverride", shapes=True, destination=False)
            for shape in shapes:
                if connected_layer:
                    for layer in connected_layer:
                        print(f"Disconnecting drawInfo of {layer} from {obj}.drawOverride.")
                cmds.disconnectAttr(f"{layer}.drawInfo", f"{obj}.drawOverride")
                cmds.setAttr(f"{shape}.overrideEnabled", lock=False)
                cmds.setAttr(f"{shape}.overrideColor", lock=False)
                cmds.setAttr(f"{shape}.overrideEnabled", 1)
                cmds.setAttr(f"{shape}.overrideColor", color_index)
