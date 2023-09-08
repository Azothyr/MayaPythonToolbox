import maya.cmds as cmds


def add_to_layer(layer_name, lyst):
    if not cmds.objExists(layer_name):
        cmds.createDisplayLayer(n=layer_name, num=1, nr=True)

    cmds.editDisplayLayerMembers(layer_name, lyst, noRecurse=True)
