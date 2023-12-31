from core.components.constraint_cmds.removal import Remove as rem
from core.components.constraint_cmds.creation import Create as cr


class Main:
    def __init__(self, mode: str = None, create_method: str = None, **kwargs):
        create_method = create_method if create_method else "cm" if kwargs.get("cm") else ""
        match mode.lower():
            case "remove", "r", "rem":
                self.remove_constraints(**kwargs)
            case "create", "c", "cr":
                match create_method.lower():
                    case "cm":
                        self.create_constraints(**kwargs)
                    case "", _:
                        self.create_constraints(**kwargs)
            case _:
                raise ValueError(f"ERROR: Invalid mode: {mode}. Expected 'remove' ('r', 'rem') or"
                                 f" 'create' ('c', 'cr').")

    @staticmethod
    def create_constraints(**kwargs):
        """
        :param Required kwargs:
            name, n: str
            leader, l: str
            follower, f: str
            type, t: str
        :return:
            NA
        """
        name = kwargs.get("name", kwargs.get("n", None))
        leader = kwargs.get("leader", kwargs.get("l", None))
        follower = kwargs.get("follower", kwargs.get("f", None))
        type = kwargs.get("type", kwargs.get("t", None))
        if not all([name, leader, follower, type]):
            raise ValueError(f"ERROR: Missing required arguments: name, leader, follower, type.")
        cr(name, leader, follower, type).create_constraint()  # noqa

    @staticmethod
    def remove_constraints(**kwargs):
        """
        :param Required kwargs:
            object, o: str
        :return:
            NA
        """
        object = kwargs.get("object", kwargs.get("o", None))
        if not object:
            raise ValueError(f"ERROR: Missing required argument: object.")
        rem.remove_constraints_from_object(object)

"""
FOR REFERENCE ONLY
class Remove:
    @staticmethod
    def remove_attrs(obj, attrs: list = None):
        clean_attrs = ['FollowTranslate', 'FollowRotate'] if attrs is None else attrs
        for attr in clean_attrs:
            if cmds.attributeQuery(attr, node=obj, exists=True):
                cmds.deleteAttr(obj + '.' + attr)

    @staticmethod
    def remove_from_all_ctrls():
        controls = [x for x in cmds.ls(type="transform") if x.lower().endswith("_ctrl")]
        for ctrl in controls:
            Remove.remove_attrs(ctrl)
            Remove.remove_from_hierarchy([ctrl])

    @staticmethod
    def remove_from_hierarchy(selection=None):
        if selection is None:
            selection = cmds.ls(sl=True) if cmds.ls(sl=True) else\
                [x for x in cmds.ls(type="transform") if x.lower().endswith("_ctrl")]
        for node in selection:
            Remove.__recursive_removal_from_hierarchy(node)

    @staticmethod
    def __recursive_removal_from_hierarchy(_node):
        constraints = cmds.listRelatives(_node, type='constraint')
        if constraints:
            for constraint in constraints:
                cmds.delete(constraint)

        children = cmds.listRelatives(_node, children=True, fullPath=True)
        if children:
            for child in children:
                Remove.__recursive_removal_from_hierarchy(child)

    @staticmethod
    def remove_all_constraints():
        for constraint in cmds.ls(type='constraint'):
            cmds.delete(constraint)
        Remove.remove_from_all_ctrls()

    @staticmethod
    def remove_constraints_from_object(object_name, attrs=None):
        # Clean attributes from the object
        Remove.remove_attrs(object_name, attrs)

        # List all the constraints on the object
        constraints = cmds.listRelatives(object_name, type='constraint')

        # If no constraints found, print a message and return
        if constraints is None:
            print(f"No constraints found on object {object_name}.")
            return

        # Delete each constraint
        for constraint in constraints:
            cmds.delete(constraint)
            print(f"Deleted constraint: {constraint}")


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
        cmds.rename(parent_const[0], f"{child_objs[i]}_parentConstraint")

        scale_const = cmds.scaleConstraint(offset=(1, 1, 1), weight=1)
        cmds.rename(scale_const[0], f"{child_objs[i]}_scaleConstraint")

        # Set override display on constraints
        attrs = ["targetWeight{}".format(j) for j in range(1, len(parent_objs) + 1)]
        for attr in attrs:
            cmds.setAttr("{}.{}".format(parent_const[0], attr), l=False)
            cmds.setAttr("{}.{}".format(parent_const[0], attr), 2)
            cmds.setAttr("{}.{}".format(scale_const[0], attr), l=False)
            cmds.setAttr("{}.{}".format(scale_const[0], attr), 2)
"""