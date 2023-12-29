import maya.cmds as cmds
from core.components.attribute_cmds import Remove as attr_rem


class CreateBase:
    def __init__(self, name: str, leader: object, follower: object, constraint_type: str):
        self.name = name
        self.leader = leader
        self.follower = follower
        self.constraint_type = constraint_type.lower()

    def create_constraint(self):
        match self.constraint_type:
            case "point", "poi":
                self.create_point_constraint()
            case "orient", "o":
                self.create_orient_constraint()
            case "parent", "par":
                self.create_parent_constraint()
            case "aim", "a":
                self.create_aim_constraint()
            case "scale", "s":
                self.create_aim_constraint()
            case _:
                raise ValueError(f"ERROR: Invalid constraint type: {self.constraint_type}. Expected 'point' ('poi'),"
                                 f" 'orient' ('o'), 'parent' ('par'), 'aim' ('a'), or 'scale' ('s').")

    def create_point_constraint(self):
        cmds.pointConstraint(self.leader, self.follower, name=self.name)

    def create_orient_constraint(self):
        cmds.orientConstraint(self.leader, self.follower, name=self.name)

    def create_parent_constraint(self):
        cmds.parentConstraint(self.leader, self.follower, name=self.name)

    def create_aim_constraint(self):
        cmds.aimConstraint(self.leader, self.follower, name=self.name)

    def create_scale_constraint(self):
        cmds.scaleConstraint(self.leader, self.follower, name=self.name)


class CreateAdvanced(CreateBase):
    def __init__(self, name: str, leader: object, follower: object, constraint_type: str):
        super().__init__(name, leader, follower, constraint_type)


class Create(CreateAdvanced):
    def __init__(self, name: str, leader: object, follower: object, constraint_type: str):
        super().__init__(name, leader, follower, constraint_type)


class RemoveBase:
    pass


class RemoveAdvanced(RemoveBase):
    pass


class Remove(RemoveAdvanced):
    def remove_from_all_ctrls(self):
        controls = [x for x in cmds.ls(type="transform") if x.lower().endswith("_ctrl")]
        for ctrl in controls:
            attr_rem().remove_attrs(ctrl)
            self.remove_from_hierarchy([ctrl])

    @staticmethod
    def remove_from_hierarchy(selection=None):
        if selection is None:
            selection = cmds.ls(sl=True) if cmds.ls(sl=True) else \
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


def parent_scale_constrain(obj_lyst, split="half"):
    # Check that there is an even number of objects selected
    if len(obj_lyst) % 2 != 0:
        cmds.warning("Please select an even number of objects")
        return

    # Cut the selection list in half
    half = int(len(obj_lyst) / 2)

    # Check if the split mode is valid, half, or every other
    match split:
        case "half", "h":
            parent_objs = obj_lyst[:half]
            child_objs = obj_lyst[half:]
        case "every other", "eo", "mod", "modulo":
            parent_objs = obj_lyst[::2]
            child_objs = obj_lyst[1::2]
        case _:
            raise RuntimeError("Invalid split mode. Please use 'half' or 'every other'.")

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
