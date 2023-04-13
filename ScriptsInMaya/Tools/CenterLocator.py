import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds


def get_center(_input):
    """
    finds the selection(s) center of mass.
    Returns: (center x, center y, center z)
    """
    bbox = cmds.exactWorldBoundingBox(_input)

    center = (
        (bbox[0] + bbox[3]) / 2,
        (bbox[1] + bbox[4]) / 2,
        (bbox[2] + bbox[5]) / 2
    )

    return center
