import maya.cmds as cmds


class ConstraintManager:
    def __init__(self, name: str, leader: object, follower: object, constraint_type: str):
        self.name = name
        self.leader = leader
        self.follower = follower
        self.constraint_type = constraint_type

    def create_constraint(self):
        match self.constraint_type:
            case "point":
                self.create_point_constraint()
            case "orient":
                self.create_orient_constraint()
            case "parent":
                self.create_parent_constraint()
            case "aim":
                self.create_aim_constraint()
            case _:
                pass

    def create_point_constraint(self):
        cmds.pointConstraint(self.leader, self.follower, name=self.name)

    def create_orient_constraint(self):
        cmds.orientConstraint(self.leader, self.follower, name=self.name)

    def create_parent_constraint(self):
        cmds.parentConstraint(self.leader, self.follower, name=self.name)

    def create_aim_constraint(self):
        cmds.aimConstraint(self.leader, self.follower, name=self.name)
