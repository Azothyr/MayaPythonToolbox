import maya.cmds as cmds


def add_to_layer(layer_name, data):
    if not cmds.objExists(layer_name):
        cmds.createDisplayLayer(name=layer_name)

    cmds.editDisplayLayerMembers(layer_name, data, noRecurse=True)
