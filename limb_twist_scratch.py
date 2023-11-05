import maya.cmds as cmds


if __name__ == "__main__":
    leader = "TARGET"
    follower = "AIMED"
    up_object = "UP"

    cmds.aimConstraint(leader, follower, worldUpType="object", worldUpVector=(0, 1, 0), worldUpObject=up_object,
                       weight=1, name=f'{follower}_to_{leader}__aim_constraint')
    # aimConstraint -offset 0 0 0 -weight 1 -aimVector 1 0 0 -upVector 0 1 0 -worldUpType "object" -worldUpObject UP;
