import maya.cmds as cmds


class CreateBase:
    def __init__(self, name: str = None, leader: object = None, follower: object = None, constraint_type: str = None):
        if not all([name, leader, follower, constraint_type]):
            cmds.warning("ERROR: Please provide a name, leader, follower, and constraint type.")
        else:
            self.name = name
            self.leader = leader
            self.follower = follower
            self.constraint_type = constraint_type.lower()

    def create_constraint(self):
        match self.constraint_type:
            case mode_var if mode_var in ["point", "poi"]:
                self.create_point_constraint()
            case mode_var if mode_var in ["orient", "o"]:
                self.create_orient_constraint()
            case mode_var if mode_var in ["parent", "par"]:
                self.create_parent_constraint()
            case mode_var if mode_var in ["aim", "a"]:
                self.create_aim_constraint()
            case mode_var if mode_var in ["scale", "s"]:
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
    def __init__(self, objects: list = None, split: str = "half", **kwargs):
        if objects is None:
            super().__init__(**kwargs)
        else:
            self.objects = objects

    @staticmethod
    def parent_scale_constrain(obj_lyst, split="half"):
        # Check that there is an even number of objects selected
        if len(obj_lyst) % 2 != 0:
            cmds.warning("Please select an even number of objects")
            return

        # Cut the selection list in half
        half = int(len(obj_lyst) / 2)

        # Check if the split mode is valid, half, or every other
        match split:
            case var if var in any(["half", "h"]):
                parent_objs = obj_lyst[:half]
                child_objs = obj_lyst[half:]
            case var if var in any([ "every other", "eo", "mod", "modulo"]):
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


class Create(CreateAdvanced):
    def __init__(self, name: str, leader: object = None, follower: object = None, constraint_type: str = None,
                 objects: list = None):
        if objects is None:
            super().__init__(name, leader, follower, constraint_type)
        else:
            super().__init__(objects)
