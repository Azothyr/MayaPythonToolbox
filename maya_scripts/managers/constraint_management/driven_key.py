import maya.cmds as cmds


if __name__ == "__main__":
    selection = cmds.ls(sl=True)
    ctrl = None
    constraint = []
    for i in selection:
        if "_Ctrl" in i and "_Grp" not in i:
            ctrl = i
        elif "Constraint" in i:
            constraint.append(i)

    if ctrl is None:
        raise ValueError("No control selected.")

    print(f"CONTROL: {ctrl}")
    print(f"CONSTRAINT: {constraint}")

    for i in constraint:
        print(cmds.setDrivenKeyframe(i, q=True, cd=True))
        print(cmds.setDrivenKeyframe(i, q=True, dn=True))

    driven_attr = [".Transform_CtrlW0", ".COG_FK_CtrlW1", ".ManW2"]
    check = "".join(ctrl)

    if "Arm" in check:
        driven_attr.append(f".{check[0]}_Clav_FK_CtrlW3")
    elif "Leg" in check:
        driven_attr.append(f".{check[0]}_Leg_Clav_CtrlW3")

    if "PV_Ctrl" not in check:
        print("Not PV_Ctrl")
    else:
        print("PV_Ctrl")
        check = check.replace("PV_Ctrl", "IK_Tip_CtrlW4")
        driven_attr.append(f".{check}")
        print(check)

    print(driven_attr)

    for i in range(len(driven_attr)):
        # Set the driver attribute to current enum value
        cmds.setAttr(f"{ctrl}.Follow", i)

        # Reset all driven attributes to 0
        for j in constraint:
            for attr in driven_attr:
                cmds.setAttr(f"{j}{attr}", 0)

        # Set the current i-th driven attribute to 1
        cmds.setAttr(f"{constraint[0]}{driven_attr[i]}", 1)
        cmds.setAttr(f"{constraint[1]}{driven_attr[i]}", 1)

        # Set driven keyframes for that configuration
        for j in driven_attr:
            cmds.setDrivenKeyframe(f"{constraint[0]}{j}", cd=f"{ctrl}.Follow", outTangentType='linear',
                                   inTangentType='linear', driverValue=i)
            cmds.setDrivenKeyframe(f"{constraint[1]}{j}", cd=f"{ctrl}.Follow", outTangentType='linear',
                                   inTangentType='linear', driverValue=i)

        print(f"{i} of {len(driven_attr)}-------------{cmds.getAttr(f'{ctrl}.Follow', asString=True)}")

