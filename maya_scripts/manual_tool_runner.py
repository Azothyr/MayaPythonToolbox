import maya.cmds as cmds


def main():
    id_25 = ["upper_arm_twist_01", "upper_arm_twist_02", "forearm_twist_01", "forearm_twist_02",
             "upper_leg_twist_01", "upper_leg_twist_02", "lower_leg_twist_01", "lower_leg_twist_02"]
    id_01 = ["tail_fk_08", "finger_01_fk_04", "finger_02_fk_04", "finger_03_fk_04", "finger_04_fk_04"]
    id_1 = ["finger_01_fk_03", "finger_02_fk_03", "finger_03_fk_03", "finger_04_fk_03"]
    id_15 = ["finger_01_fk_02", "finger_04_fk_02", "finger_03_fk_02", "finger_02_fk_02"]
    cmds.select(clear=True)

    for obj in cmds.ls(type="joint"):
        if any(item in obj.lower() for item in id_25):
            cmds.setAttr(f"{obj}.radius", 0.25)
        elif any(item in obj.lower() for item in id_01):
            cmds.setAttr(f"{obj}.radius", 0.01)
        elif any(item in obj.lower() for item in id_1):
            cmds.setAttr(f"{obj}.radius", 0.1)
        elif any(item in obj.lower() for item in id_15):
            cmds.setAttr(f"{obj}.radius", 0.15)
        else:
            print(f"Object {obj} not found")


if __name__ == "__main__":
    main()
