import sys
if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' in sys.path:
    sys.path.remove('C:/GitRepos/MayaPythonToolbox/maya_scripts')
if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' not in sys.path:
    sys.path.append('C:/GitRepos/MayaPythonToolbox/maya_scripts')
import maya.cmds as cmds
from pprint import pprint
import re
from tools.xform_handler import match_xform, add_to_xform_values, set_xform_values, xform_attributes


class LowerLimbTwistManager:
    def __init__(self, name, rk_wrist, rk_elbow, rk_hand, twist_count=1, aim_vector=(1,0,0), up_vector=(0,1,0)):
        self.name = name
        self.rk_wrist = rk_wrist
        self.rk_elbow = rk_elbow
        self.rk_hand = rk_hand
        self.radius = self.set_radius()
        self.twist_Grp = f"{self.name}_Loc_Grp"
        self.aim = f"{self.name}_Aim_Loc"
        self.target = f"{self.name}_Target_Loc"
        self.up = f"{self.name}_Up_Loc"
        self.aim_vector = aim_vector
        self.up_vector = up_vector

        self.create_twist_base()
        self.twist_locators = self.create_falloff_twist(twist_count)
        self.twist_joints = self.create_twist_joints()
        self.clean_up()

    def set_radius(self):
        radius = cmds.getAttr(f"{self.rk_wrist}.radius") * 0.75
        return radius

    def create_twist_base(self):
        # Creating locators and group
        self.twist_Grp = cmds.group(empty=True, name=self.twist_Grp)
        self.aim = cmds.spaceLocator(name=self.aim)[0]
        self.target = cmds.spaceLocator(name=self.target)[0]
        self.up = cmds.spaceLocator(name=self.up)[0]

        # Setting to joint positions
        match_xform(self.rk_wrist, [self.aim, self.up, self.twist_Grp], translation=True)
        match_xform(self.rk_elbow, self.target, translation=True)
        match_xform(self.rk_wrist, [self.aim, self.twist_Grp, self.target, self.up], rotation=True)
        add_to_xform_values(self.up, 'translation', y=5)
        cmds.parent(self.aim, self.target, self.up, self.twist_Grp)

        # Creating constraints

        cmds.parentConstraint(self.rk_elbow, self.twist_Grp, mo=True, name=f'parent_constraint__from_{self.rk_elbow}')
        cmds.scaleConstraint(self.rk_elbow, self.twist_Grp, maintainOffset=True,
                             name=f"scale_constraint__from_{self.rk_elbow}")
        # Creating the locator aim constraint
        cmds.aimConstraint(self.target, self.aim, worldUpType="object", worldUpVector=self.up_vector,
                           aimVector=self.aim_vector, worldUpObject=self.up, weight=1,
                           name=f'aim_constraint__from_{self.target}')
        # Creating the point constraint keeping the aim locator on the hand/foot joint
        cmds.pointConstraint(self.rk_hand, self.aim, weight=1, maintainOffset=True,
                             name=f'point_constraint__from_{self.rk_hand}')
        # Creating the parent constraint of the hand/foot joint to the up locator to maintain its position
        cmds.parentConstraint(self.rk_hand, self.up, mo=True, name=f'parent_constraint__from_{self.rk_hand}')

    def create_falloff_twist(self, count=1):
        if count < 1:
            count = 1
        if count > 3:
            count = 3

        locators = []

        weight_ratio = {25: (0.75,0.25), 33: (0.67,0.33), 50: (1,1), 66: (0.33,0.67), 75: (0.25,0.75)}
        md_connections = {25: "outputY", 33: "outputX", 50: "outputX", 66: "outputY", 75: "outputZ"}

        mult_div = cmds.shadingNode('multiplyDivide', name=f"{self.name}_Twist_Falloff_MD", asUtility=True)
        cmds.setAttr(f"{mult_div}.operation", 1)

        if count == 1:
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1X"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1X", force=True)
            cmds.setAttr(f"{mult_div}.input2X", 0.5)

        elif count == 2:
            cmds.setAttr(f"{mult_div}.input2X", 0.33)
            cmds.setAttr(f"{mult_div}.input2Y", 0.66)
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1X"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1X", force=True)
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1Y"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1Y", force=True)

        else:
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1X"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1X", force=True)
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1Y"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1Y", force=True)
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1Z"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1Z", force=True)
            cmds.setAttr(f"{mult_div}.input2X", 0.5)
            cmds.setAttr(f"{mult_div}.input2Y", 0.25)
            cmds.setAttr(f"{mult_div}.input2Z", 0.75)


        for i in range(count):
            percent = int(100 / (count+1)) * (i+1)
            percent_string = f"{percent}" if percent != 50 else "Mid"
            locator = cmds.spaceLocator(name=f"{self.name}_{percent_string}_Loc")[0]
            locators.append(locator)
            match_xform(self.rk_elbow, locator, translation=True, rotation=True)
            cmds.parent(locator, self.twist_Grp)

            # Creating the dynamic point constraint holding the middle locator between the two joints
            pt_constraint = cmds.pointConstraint(self.target, self.aim, locator, weight=1,
                                                 maintainOffset=False,
                                                 name=f'point_constraint__from_{self.target}_and_{self.aim}')[0]

            cmds.setAttr(f"{pt_constraint}.{self.target}W0", weight_ratio[percent][0])
            cmds.setAttr(f"{pt_constraint}.{self.aim}W1", weight_ratio[percent][1])
            if not cmds.isConnected(f"{mult_div}.{md_connections[percent]}", f"{locator}.rotateX"):
                cmds.connectAttr(f"{mult_div}.{md_connections[percent]}", f"{locator}.rotateX", force=True)

        return locators

    def create_twist_joints(self):
        if not self.twist_locators:
            raise ValueError("No twist locators found.")
        if type(self.twist_locators) is not list:
            self.twist_locators = [self.twist_locators]
        self.twist_locators.append(self.aim)

        twist_joints = []
        for i, locator in enumerate(self.twist_locators):
            twist_joint = cmds.joint(name=f"{self.name}_Twist_{str(i + 1).zfill(2)}_Jnt", radius=self.radius)
            twist_joints.append(twist_joint)
            match_xform(locator, twist_joint, translation=True)
            cmds.parent(twist_joint, self.rk_elbow)
            cmds.makeIdentity(twist_joint, apply=True, rotate=1)
            orientation = xform_attributes()
            orientation['joint_orient'] = (True, {'x': 0, 'y': 0, 'z': 0})
            set_xform_values(objects=twist_joint, options=orientation)

            cmds.parentConstraint(locator, twist_joint, maintainOffset=False,
                                  name=f'parent_constraint__from_{locator}')

        return twist_joints

    def clean_up(self):
        _group = cmds.group(name="Limb_Twist_Loc_Grp", empty=True) if not\
            cmds.objExists("Limb_Twist_Loc_Grp") else "Limb_Twist_Loc_Grp"

        cmds.scaleConstraint(self.rk_elbow, self.twist_Grp, maintainOffset=True,
                             name=f"scale_constraint__from_{self.rk_elbow}")

        cmds.parent(self.twist_Grp, _group)

        if cmds.objExists("Deformers"):
            cmds.parent("Limb_Twist_Loc_Grp", "Deformers")


class UpperLimbTwistManager:
    def __init__(self, name, rk_shoulder, rk_elbow, twist_count=1, aim_vector=(1,0,0), up_vector=(0,1,0)):
        self.name = name
        self.rk_shoulder = rk_shoulder
        self.rk_elbow = rk_elbow
        self.radius = self.set_radius()
        self.twist_Grp = f"{self.name}_Loc_Grp"
        self.aim = f"{self.name}_Aim_Loc"
        self.target = f"{self.name}_Target_Loc"
        self.up = f"{self.name}_Up_Loc"
        self.aim_vector = aim_vector
        self.up_vector = up_vector

        self.create_twist_base()
        self.twist_locators = self.create_falloff_twist(twist_count)
        self.twist_joints = self.create_twist_joints()
        self.clean_up()

    def set_radius(self):
        radius = cmds.getAttr(f"{self.rk_shoulder}.radius") * 0.75
        return radius

    def create_twist_base(self):
        # Creating locators and group
        self.twist_Grp = cmds.group(empty=True, name=self.twist_Grp)
        self.aim = cmds.spaceLocator(name=self.aim)[0]
        self.target = cmds.spaceLocator(name=self.target)[0]
        self.up = cmds.spaceLocator(name=self.up)[0]

        # Setting to joint positions
        match_xform(self.rk_shoulder, [self.aim, self.twist_Grp], translation=True)
        match_xform(self.rk_elbow, [self.target, self.up], translation=True)
        match_xform(self.rk_shoulder, [self.aim, self.twist_Grp, self.target, self.up], rotation=True)
        add_to_xform_values(self.up, 'translation', y=-5)
        cmds.parent(self.aim, self.target, self.up, self.twist_Grp)

        # Creating constraints

        cmds.parentConstraint(self.rk_elbow, self.twist_Grp, mo=True, name=f'parent_constraint__from_{self.rk_elbow}')
        cmds.scaleConstraint(self.rk_elbow, self.twist_Grp, maintainOffset=True,
                             name=f"scale_constraint__from_{self.rk_elbow}")

        # Creating the locator aim constraint
        cmds.aimConstraint(self.target, self.aim, worldUpType="object", worldUpVector=self.up_vector,
                           aimVector=self.aim_vector, worldUpObject=self.up, weight=1,
                           name=f'aim_constraint__from_{self.target}')
        # Creating the point constraint keeping the aim locator on the hand/foot joint
        cmds.pointConstraint(self.rk_elbow, self.aim, weight=1, maintainOffset=True,
                             name=f'point_constraint__from_{self.rk_elbow}')
        # Creating the parent constraint of the hand/foot joint to the up locator to maintain its position
        cmds.parentConstraint(self.rk_elbow, self.up, mo=True, name=f'parent_constraint__from_{self.rk_elbow}')

    def create_falloff_twist(self, count=1):
        if count < 1:
            count = 1
        if count > 3:
            count = 3

        locators = []

        weight_ratio = {25: (0.75,0.25), 33: (0.67,0.33), 50: (1,1), 66: (0.33,0.67), 75: (0.25,0.75)}
        md_connections = {25: "outputY", 33: "outputX", 50: "outputX", 66: "outputY", 75: "outputZ"}

        mult_div = cmds.shadingNode('multiplyDivide', name=f"{self.name}_Twist_Falloff_MD", asUtility=True)
        cmds.setAttr(f"{mult_div}.operation", 1)

        if count == 1:
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1X"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1X", force=True)
            cmds.setAttr(f"{mult_div}.input2X", 0.5)

        elif count == 2:
            cmds.setAttr(f"{mult_div}.input2X", 0.33)
            cmds.setAttr(f"{mult_div}.input2Y", 0.66)
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1X"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1X", force=True)
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1Y"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1Y", force=True)

        else:
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1X"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1X", force=True)
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1Y"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1Y", force=True)
            if not cmds.isConnected(f"{self.aim}.rotateX", f"{mult_div}.input1Z"):
                cmds.connectAttr(f"{self.aim}.rotateX", f"{mult_div}.input1Z", force=True)
            cmds.setAttr(f"{mult_div}.input2X", 0.5)
            cmds.setAttr(f"{mult_div}.input2Y", 0.25)
            cmds.setAttr(f"{mult_div}.input2Z", 0.75)


        for i in range(count):
            percent = int(100 / (count+1)) * (i+1)
            percent_string = f"{percent}" if percent != 50 else "Mid"
            locator = cmds.spaceLocator(name=f"{self.name}_{percent_string}_Loc")[0]
            locators.append(locator)
            match_xform(self.rk_elbow, locator, translation=True, rotation=True)
            cmds.parent(locator, self.twist_Grp)

            # Creating the dynamic point constraint holding the middle locator between the two joints
            pt_constraint = cmds.pointConstraint(self.target, self.aim, locator, weight=1,
                                                 maintainOffset=False,
                                                 name=f'point_constraint__from_{self.target}_and_{self.aim}')[0]

            cmds.setAttr(f"{pt_constraint}.{self.target}W0", weight_ratio[percent][0])
            cmds.setAttr(f"{pt_constraint}.{self.aim}W1", weight_ratio[percent][1])
            if not cmds.isConnected(f"{mult_div}.{md_connections[percent]}", f"{locator}.rotateX"):
                cmds.connectAttr(f"{mult_div}.{md_connections[percent]}", f"{locator}.rotateX", force=True)

        return locators

    def create_twist_joints(self):
        if not self.twist_locators:
            raise ValueError("No twist locators found.")
        if type(self.twist_locators) is not list:
            self.twist_locators = [self.twist_locators]
        self.twist_locators.append(self.aim)

        twist_joints = []
        for i, locator in enumerate(self.twist_locators):
            twist_joint = cmds.joint(name=f"{self.name}_Twist_{str(i + 1).zfill(2)}_Jnt", radius=self.radius)
            twist_joints.append(twist_joint)
            match_xform(locator, twist_joint, translation=True)
            cmds.parent(twist_joint, self.rk_elbow)
            cmds.makeIdentity(twist_joint, apply=True, rotate=1)
            orientation = xform_attributes()
            orientation['joint_orient'] = (True, {'x': 0, 'y': 0, 'z': 0})
            set_xform_values(objects=twist_joint, options=orientation)

            cmds.parentConstraint(locator, twist_joint, maintainOffset=False,
                                  name=f'parent_constraint__from_{locator}')

        return twist_joints

    def clean_up(self):
        _group = cmds.group(name="Limb_Twist_Loc_Grp", empty=True) if not\
            cmds.objExists("Limb_Twist_Loc_Grp") else "Limb_Twist_Loc_Grp"
        cmds.parent(self.twist_Grp, _group)

        if cmds.objExists("Deformers"):
            cmds.parent("Limb_Twist_Loc_Grp", "Deformers")


if __name__ == "__main__":
    def module_name():
        import inspect
        import os
        # Get the current frame and find the file name of the script
        frame = inspect.currentframe()
        filename = inspect.getfile(frame)
        return os.path.basename(filename).split('.')[0]
    print(f"{'-' * 10 + '|' + ' ' * 4} RUNNING {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 10}")

    selection = cmds.ls(selection=True, type="joint")
    # creator = LowerLimbTwistManager("L_ForeArm", selection[0], selection[1], selection[2],
    #                           twist_count=1, aim_vector=(-1,0,0), up_vector=(0,1,0))
    creator = UpperLimbTwistManager("L_Upper_Arm", selection[0], selection[1],
                              twist_count=1, aim_vector=(-1,0,0), up_vector=(0,1,0))

    print(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED {module_name()}  DUNDER MAIN {' ' * 4 + '|' + '-' * 25}")

