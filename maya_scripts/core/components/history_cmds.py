import maya.cmds as cmds


def _freeze_transformations(obj):
    """
    Freezes the transformations of the specified object.
    """
    cmds.makeIdentity(obj, apply=True, translate=1, rotate=1, scale=1, normal=0)
    print(f"{obj}'s transformation frozen")


def _delete_history(obj):
    """
    Deletes the history of the specified object.
    """
    cmds.delete(obj, ch=True)
    print(f"Deleted {obj} history.")


def freeze_delete(obj_lyst, freeze: bool = True, delete: bool = True):
    for obj in obj_lyst:
        if freeze:
            _freeze_transformations(obj)
        if delete:
            delete_history_preserve_creation_nodes(obj)
    cmds.warning("Completed freezing of transforms and deleting history.")


def delete_history_preserve_creation_nodes(obj):
    # Get the object's history
    history = cmds.listHistory(obj, pdo=True)

    # Nodes to preserve: SkinClusters and creation nodes like makeNurbCircle
    preserve_types = ['skinCluster']
    creation_nodes = ['makeNurbCircle', 'makeNurbSphere', 'makeNurbCone', 'makeNurbCube', 'makeNurbCylinder',
                      'makeNurbPlane', 'makeNurbTorus']

    # Find skinClusters and creation nodes in history
    nodes_to_preserve = cmds.ls(history, type=preserve_types)
    for node in history:
        if cmds.nodeType(node) in creation_nodes:
            nodes_to_preserve.append(node)

    # Nodes to delete are those in history but not in nodes_to_preserve
    nodes_to_delete = [node for node in history if
                       node not in nodes_to_preserve and cmds.nodeType(node) != 'transform']

    # Delete non-preserved history nodes
    if nodes_to_delete:
        cmds.delete(nodes_to_delete)

    # Provide feedback
    print(f"Processed '{obj}': History deleted, specified nodes preserved.")


if __name__ == "__main__":
    freeze_delete(cmds.ls(sl=True), freeze=False, delete=True)
