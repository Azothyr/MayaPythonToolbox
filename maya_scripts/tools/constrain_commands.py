import maya.cmds as cmds


def parent_scale_constrain(obj_lyst):
    # Check that there is an even number of objects selected
    if len(obj_lyst) % 2 != 0:
        cmds.warning("Please select an even number of objects")
        return

    # Cut the selection list in half
    half = int(len(obj_lyst) / 2)
    parent_objs = obj_lyst[:half]
    child_objs = obj_lyst[half:]

    # Create parent and scale constraints for each pair of objects
    for i in range(half):
        cmds.select(child_objs[i], add=True)
        cmds.select(parent_objs[i], toggle=True)

        parent_const = cmds.parentConstraint(mo=True, weight=1)
        cmds.rename(parent_const[0], "{}_parentConstraint".format(child_objs[i]))

        scale_const = cmds.scaleConstraint(offset=(1, 1, 1), weight=1)
        cmds.rename(scale_const[0], "{}_scaleConstraint".format(child_objs[i]))

        # Set override display on constraints
        attrs = ["targetWeight{}".format(j) for j in range(1, len(parent_objs) + 1)]
        for attr in attrs:
            cmds.setAttr("{}.{}".format(parent_const[0], attr), l=False)
            cmds.setAttr("{}.{}".format(parent_const[0], attr), 2)
            cmds.setAttr("{}.{}".format(scale_const[0], attr), l=False)
            cmds.setAttr("{}.{}".format(scale_const[0], attr), 2)
