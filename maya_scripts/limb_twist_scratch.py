import maya.cmds as cmds
from tools.center_locator import get_center
from tools import xform_handler


class TwistSysManager:
    def __init__(self, name, joint1, joint2):
        self.name = name
        self.joint1 = joint1
        self.joint2 = joint2
        self.transform1 = get_center(self.joint1)
        self.transform2 = get_center(self.joint2)
        self.twist_Grp = f"{self.name}_Loc_Grp"
        self.aim = f"{self.name}_aim_Loc"
        self.target = f"{self.name}_target_Loc"
        self.mid = f"{self.name}_mid_Loc"
        self.up = f"{self.name}_up_Loc"

    def create_twist_base(self):
        self.twist_Grp = cmds.group(empty=True, name=self.twist_Grp)
        self.aim = cmds.spaceLocator(name=self.aim, position=self.transform1)[0]
        self.target = cmds.spaceLocator(name=self.target, position=self.transform2)[0]
        self.mid = cmds.spaceLocator(name=self.mid, position=self.transform1)[0]
        self.up = cmds.spaceLocator(name=self.up, position=self.transform1)[0]


if __name__ == "__main__":
    # aimConstraint -offset 0 0 0 -weight 1 -aimVector 1 0 0 -upVector 0 1 0 -worldupType "object" -worldupObject up;

    selection = cmds.ls(selection=True, type="joint")
    creator = TwistSysManager("L_ForeArm", selection[0], selection[1])
