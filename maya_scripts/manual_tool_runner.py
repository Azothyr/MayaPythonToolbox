import sys

if 'C:/Repos/MayaPythonToolbox/maya_scripts' in sys.path:
    sys.path.remove('C:/Repos/MayaPythonToolbox/maya_scripts')
if 'C:/Repos/MayaPythonToolbox/maya_scripts' not in sys.path:
    sys.path.append('C:/Repos/MayaPythonToolbox/maya_scripts')
import maya.cmds as cmds
# from pprint import pprint
# import re
from tools.xform_handler import XformHandler
from maya_scripts.tools.color_changer import change_color


class LimbTwistManager:
    def __init__(self, limb_name, upper_name, lower_name, rk_top_jnt, rk_pivot_jnt, rk_bot_jnt, rk_bot2_jnt,
                 twist_count=1, aim_vector=(1, 0, 0), up_vector=(0, 1, 0)):
        self.limb_name = limb_name
        self.u_name = upper_name
        self.l_name = lower_name
        self.count = twist_count
        self.rk_top_jnt = rk_top_jnt
        self.rk_pivot_jnt = rk_pivot_jnt
        self.rk_bot_jnt = rk_bot_jnt
        self.rk_bot2_jnt = rk_bot2_jnt
        self.top_jnt_xform = XformHandler(self.rk_top_jnt)
        self.pivot_jnt_xform = XformHandler(self.rk_pivot_jnt)
        self.bot_jnt_xform = XformHandler(self.rk_bot_jnt)
        self.bot2_jnt_xform = XformHandler(self.rk_bot2_jnt)
        # Deselecting all created objects
        cmds.select(clear=True)

        self.radius = self._set_radius()

        self.helper_top_joint_correcter = cmds.joint(name=f"{self.u_name}_Twist_01_Corrective_Jnt", radius=self.radius)
        self.correcter_xform = XformHandler(self.helper_top_joint_correcter)
        cmds.select(clear=True)

        # Creating upper locators and group
        self.u_full_grp = cmds.group(empty=True, name=f"{self.u_name}_Twist_Grp")
        self.u_loc_grp = cmds.group(empty=True, name=f"{self.u_name}_Loc_Grp")
        self.u_aim = cmds.spaceLocator(name=f"{self.u_name}_Aim_Loc")[0]
        self.u_target = cmds.spaceLocator(name=f"{self.u_name}_Target_Loc")[0]
        self.u_up = cmds.spaceLocator(name=f"{self.u_name}_Up_Loc")[0]
        self.u_twist_joints = None
        self.u_twist_locators = None
        self.u_loc_grp_xform = XformHandler(self.u_loc_grp)
        self.u_aim_xform = XformHandler(self.u_aim)
        self.u_target_xform = XformHandler(self.u_target)
        self.u_up_xform = XformHandler(self.u_up)
        cmds.select(clear=True)

        if self.get_limb() == "Arm":
            # Creating upper arm helpers
            self.helper_jnt_grp = cmds.group(empty=True, name=f"{self.u_name}_Twist_IK_Jnt_Grp")
            self.helper_pv_locator = cmds.spaceLocator(name=f"{self.u_name}_Twist_PV_Loc")[0]
            cmds.select(clear=True)
            self.helper_joint1 = cmds.joint(name=f"{self.u_name}_Twist_IK_01_Jnt", radius=self.radius)
            cmds.select(clear=True)
            self.helper_joint2 = cmds.joint(name=f"{self.u_name}_Twist_IK_02_Jnt", radius=self.radius)
            cmds.select(clear=True)
            self.loc_pv_xform = XformHandler(self.helper_pv_locator)
            self.help_jnt_grp_xform = XformHandler(self.helper_jnt_grp)
            self.help_jnt1_xform = XformHandler(self.helper_joint1)
            self.help_jnt2_xform = XformHandler(self.helper_joint2)

        # Creating lower locators and group
        self.l_full_grp = cmds.group(empty=True, name=f"{self.l_name}_Twist_Grp")
        self.l_loc_grp = cmds.group(empty=True, name=f"{self.l_name}_Loc_Grp")
        self.l_twist_joints = None
        self.l_twist_locators = None
        self.l_aim = cmds.spaceLocator(name=f"{self.l_name}_Aim_Loc")[0]
        self.l_target = cmds.spaceLocator(name=f"{self.l_name}_Target_Loc")[0]
        self.l_up = cmds.spaceLocator(name=f"{self.l_name}_Up_Loc")[0]
        self.l_loc_grp_xform = XformHandler(self.l_loc_grp)
        self.l_aim_xform = XformHandler(self.l_aim)
        self.l_target_xform = XformHandler(self.l_target)
        self.l_up_xform = XformHandler(self.l_up)
        cmds.select(clear=True)

        if self.get_limb() == "Arm":
            self.u_aim_vector = aim_vector
            self.u_up_vector = tuple([up_vector[i] * -1 for i in range(len("xyz"))])
            self.l_aim_vector = tuple([aim_vector[i] * -1 for i in range(len("xyz"))])
            self.l_up_vector = up_vector
        elif self.get_limb() == "Leg":
            self.u_aim_vector = tuple([up_vector[i] * -1 for i in range(len("xyz"))])
            self.u_up_vector = up_vector
            self.l_aim_vector = aim_vector
            self.l_up_vector = up_vector
        else:
            self.u_aim_vector = aim_vector
            self.u_up_vector = up_vector
            self.l_aim_vector = aim_vector
            self.l_up_vector = up_vector

    def run(self, l_up_dist=None, u_up_dist=None, u_up_axis=None, l_up_axis=None, u_helper_dist=None,
            u_helper_axis=None, correct_percent=None):
        self.create_lower_twist_system(l_up_dist, l_up_axis)
        self.create_upper_twist_system(u_up_dist, u_up_axis, u_helper_dist, u_helper_axis, correct_percent)
        self.clean_up()
        self.connect_to_rig()
        self.color_twist_system()
        if self.get_limb() == "Arm":
            self.color_helpers()
        print(f"Twist system created for {self.u_name} and {self.l_name}.")

    def get_side(self):
        if self.limb_name is None:
            return
        return self.limb_name.split("_")[0].upper()

    def get_limb(self):
        if self.limb_name is None:
            return
        return self.limb_name.split("_")[1].capitalize()

    def connect_to_rig(self):
        if self.limb_name is None:
            return
        side = self.get_side()
        limb = self.get_limb()
        if side not in ["L", "R", "C"]:
            raise ValueError(f"Invalid limb name: {self.limb_name}.")
        if limb not in ["Arm", "Leg"]:
            raise ValueError(f"Invalid limb name: {self.limb_name}.")
        if limb == "Arm":
            connection = f"{side}_Clav"
        elif limb == "Leg":
            connection = f"{side}_Leg_Clav"
        else:
            raise ValueError(f"Invalid limb name: {self.limb_name}.")
        objects = cmds.ls(type="joint")
        con_jnt = None
        for obj in objects:
            if connection in obj:
                con_jnt = obj
                break
        if not con_jnt:
            raise ValueError(f"Could not find connection joint for {self.limb_name}.")
        if not cmds.objExists(con_jnt):
            raise ValueError(f"Could not find connection joint for {self.limb_name}.")
        if not cmds.objExists(self.helper_top_joint_correcter):
            # Parent constraint tying the upper helper IK group to the clavicle joint
            cmds.parentConstraint(con_jnt, self.helper_jnt_grp, maintainOffset=True,
                                  name=f"parent_constraint__from_{con_jnt}")

            # Scale constraint tying the upper helper IK group to the clavicle joint
            cmds.scaleConstraint(con_jnt, self.helper_jnt_grp, maintainOffset=True,
                                 name=f"scale_constraint__from_{con_jnt}")

    def _set_radius(self):
        radius = int(cmds.getAttr(f"{self.rk_bot_jnt}.radius") * 0.50)
        return radius

    def _set_locator_scale(self):
        scale = cmds.getAttr(f"{self.rk_bot_jnt}.radius")
        sels = cmds.ls("*_Loc", type="transform")
        locators = [sel for sel in sels if "Loc_Grp" not in sel or "Constraint" not in sel]
        print(f"setting scale to {scale} for {locators}")
        for loc in locators:
            shape = cmds.listRelatives(loc, shapes=True)[0] if cmds.listRelatives(loc, shapes=True) else None
            if shape:
                for axis in "XYZ":
                    cmds.setAttr(f"{shape}.localScale{axis}", scale)

    def create_upper_twist_system(self, up_dist=None, on_axis=None, helper_dist=None, helper_axis=None,
                                  correct_percent=None):
        self.create_upper_twist_base(up_dist=up_dist, on_axis=on_axis)
        cmds.select(clear=True)
        if self.get_limb() == "Arm":
            self.create_upper_limb_helpers(helper_dist=helper_dist, helper_axis=helper_axis)
        cmds.select(clear=True)
        self.u_twist_locators = self.create_falloff_twist(self.u_name, self.top_jnt_xform, self.u_aim, self.u_target,
                                                          self.u_loc_grp)
        cmds.select(clear=True)
        self.u_twist_joints = self.create_twist_joints(self.u_name, self.u_twist_locators, self.u_target,
                                                       self.rk_top_jnt)
        cmds.select(clear=True)
        self.create_upper_twist_corrective(correct_percent)
        cmds.select(clear=True)

    def create_upper_twist_base(self, up_dist=None, on_axis="y"):
        if up_dist is None:
            base_dist = self.top_jnt_xform.calculate_distance(self.pivot_jnt_xform)
            up_dist = int(base_dist * 0.9)
        if "-" in on_axis:
            up_dist *= -1
            on_axis = on_axis.replace("-", "")

        # Setting to joint positions
        for obj in [self.u_loc_grp_xform, self.u_aim_xform]:
            obj.match_xform(self.rk_top_jnt, "translate")
        for obj in [self.u_target_xform, self.u_up_xform]:
            obj.match_xform(self.rk_pivot_jnt, "translate")
        for obj in [self.u_loc_grp_xform, self.u_aim_xform, self.u_target_xform, self.u_up_xform]:
            obj.match_xform(self.rk_top_jnt, "rotate")

        # Moving the aim locator -5 units in the y-axis
        self.u_up_xform.add_in_local('translate', **{on_axis: up_dist})
        cmds.parent(self.u_aim, self.u_target, self.u_up, self.u_loc_grp)

        # Creating constraints
        # Locking the position of the group to the top_jnt
        cmds.parentConstraint(self.rk_top_jnt, self.u_loc_grp, maintainOffset=True,
                              name=f'parent_constraint__from_{self.rk_top_jnt}')
        # Locking the scale of the group to the top_jnt
        cmds.scaleConstraint(self.rk_top_jnt, self.u_loc_grp, maintainOffset=True,
                             name=f"scale_constraint__from_{self.rk_top_jnt}")
        # Creating the locator aim constraint
        cmds.aimConstraint(self.u_target, self.u_aim, worldUpType="object", worldUpVector=self.u_up_vector, weight=1,
                           aimVector=self.u_aim_vector, maintainOffset=False, worldUpObject=self.u_up,
                           name=f'aim_constraint__from_{self.u_target}__up_vector_to_{self.u_up}')
        # Point constraint keeping the target locator on the pivot_jnt
        cmds.pointConstraint(self.rk_pivot_jnt, self.u_target, weight=1, maintainOffset=True,
                             name=f'point_constraint__from_{self.u_target}')

    def create_upper_limb_helpers(self, helper_dist=None, helper_axis="z"):
        if helper_dist is None:
            base_dist = self.top_jnt_xform.calculate_distance(self.pivot_jnt_xform)
            helper_dist = int(base_dist + (base_dist * 0.1))
        if "-" in helper_axis:
            helper_dist *= -1
            helper_axis = helper_axis.replace("-", "")

        # Setting the helper joint1 to the position of the top_jnt
        self.help_jnt1_xform.match_xform(self.top_jnt_xform, "translate")
        # Moving the helper joint1 -3 units in the z axis
        self.help_jnt1_xform.add_in_world('translate', **{helper_axis: helper_dist})
        # Setting the helper joint2 to the position of the pivot_jnt
        self.help_jnt2_xform.match_xform(self.pivot_jnt_xform, "translate")
        # Moving the helper joint2 to be halfway between helper 1 and the pivot_jnt
        self.help_jnt2_xform.move_relative_to_obj(self.help_jnt1_xform,
                                                  self.help_jnt2_xform.calculate_distance(self.help_jnt1_xform) / 2)
        cmds.parent(self.helper_joint2, self.helper_joint1)
        # Orienting the helper joints
        cmds.joint(self.helper_joint1, edit=True, orientJoint="xzy", secondaryAxisOrient="ydown", children=True,
                   zeroScaleOrient=True)
        # Setting the joint orient of the second helper joint to be the same as the first
        self.help_jnt2_xform.set_xform("jointOrient", zero_out=True)

        # Setting the position of the pole vector locator
        self.loc_pv_xform.match_xform(self.help_jnt1_xform, "translate")
        # Moving the pole vector locator 3 units in the y-axis
        distance = abs(helper_dist) / 2 if abs(helper_dist) > 5 else 5
        self.loc_pv_xform.add_in_world('translate', y=distance)

        # Creating the group for the helper joints
        self.help_jnt_grp_xform.match_xform(self.help_jnt1_xform, ["translate", "rotate"])
        self.help_jnt_grp_xform.set_attribute_x("rotate", 0)

        # Creating the IK handle for the helper joints
        cmds.ikHandle(startJoint=self.helper_joint1, endEffector=self.helper_joint2, solver="ikRPsolver",
                      name=f"{self.u_name}_Twist_IK_Handle")

        # Deselecting all created objects
        cmds.select(clear=True)

        # Creating the pole vector constraint
        cmds.poleVectorConstraint(self.helper_pv_locator, f"{self.u_name}_Twist_IK_Handle", weight=1,
                                  name=f'pole_vector_constraint__from_{self.helper_pv_locator}')

        # Point constraint keeping the ik handle pointing at the pivot_jnt
        cmds.pointConstraint(self.rk_pivot_jnt, f"{self.u_name}_Twist_IK_Handle", weight=1, maintainOffset=False,
                             name=f'point_constraint__from_{self.rk_pivot_jnt}')

        # Setting all pieces of the helper group to be children of the helper group
        cmds.parent(self.helper_pv_locator, self.helper_joint1, f"{self.u_name}_Twist_IK_Handle",
                    self.helper_jnt_grp)

        # Parent constraint keeping the up locator's position relative to the helper 1 joint
        cmds.parentConstraint(self.helper_joint1, self.u_up, mo=True,
                              name=f"parent_constraint__from_{self.helper_joint1}")

    def create_upper_twist_corrective(self, affect_percent=10):
        affect_percent /= 100
        self.correcter_xform.match_xform(self.top_jnt_xform, ["translate", "rotate"])
        mult_div = cmds.shadingNode('multiplyDivide', name=f"{self.limb_name}_Twist_Corrective_MD", asUtility=True)
        if not cmds.isConnected(f"{self.rk_top_jnt}.rotateX", f"{mult_div}.input1X"):
            cmds.connectAttr(f"{self.rk_top_jnt}.rotateX", f"{mult_div}.input1X", force=True)
        cmds.setAttr(f"{mult_div}.input2X", affect_percent)
        if not cmds.isConnected(f"{mult_div}.outputX", f"{self.helper_top_joint_correcter}.rotateX"):
            cmds.connectAttr(f"{mult_div}.outputX", f"{self.helper_top_joint_correcter}.rotateX", force=True)
        cmds.parent(self.helper_top_joint_correcter, self.rk_top_jnt)
        self.u_twist_joints.append(self.helper_top_joint_correcter)

    def create_lower_twist_system(self, up_dist=None, on_axis=None):
        self.create_lower_twist_base(up_dist=up_dist, on_axis=on_axis)
        cmds.select(clear=True)
        self.l_twist_locators = self.create_falloff_twist(self.l_name, self.pivot_jnt_xform, self.l_aim,
                                                          self.l_target, self.l_loc_grp)
        cmds.select(clear=True)
        self.l_twist_joints = self.create_twist_joints(self.l_name, self.l_twist_locators, self.l_aim,
                                                       self.rk_pivot_jnt)
        cmds.select(clear=True)

    def create_lower_twist_base(self, up_dist=None, on_axis='y'):
        if up_dist is None:
            base_dist = self.pivot_jnt_xform.calculate_distance(self.bot_jnt_xform)
            up_dist = int(base_dist / 4)
        if "-" in on_axis:
            up_dist *= -1
            on_axis = on_axis.replace("-", "")

        # Setting to joint positions
        for obj in [self.l_loc_grp_xform, self.l_aim_xform, self.l_up_xform]:
            obj.match_xform(self.bot_jnt_xform, "translate")
        self.l_target_xform.match_xform(self.pivot_jnt_xform, "translate")
        for obj in [self.l_loc_grp_xform, self.l_aim_xform, self.l_target_xform, self.l_up_xform]:
            obj.match_xform(self.bot_jnt_xform, "rotate")

        self.l_up_xform.add_in_local('translate', **{on_axis: up_dist})

        cmds.parent(self.l_aim, self.l_target, self.l_up, self.l_loc_grp)

        # Locking the position of the group to the pivot_jnt
        cmds.parentConstraint(self.rk_pivot_jnt, self.l_loc_grp, mo=True,
                              name=f'parent_constraint__from_{self.rk_pivot_jnt}')
        cmds.scaleConstraint(self.rk_pivot_jnt, self.l_loc_grp, maintainOffset=True,
                             name=f"scale_constraint__from_{self.rk_pivot_jnt}")
        # Creating the locator aim constraint
        cmds.aimConstraint(self.l_target, self.l_aim, worldUpType="object", worldUpVector=self.l_up_vector,
                           aimVector=self.l_aim_vector, worldUpObject=self.l_up, weight=1,
                           name=f'aim_constraint__from_{self.l_target}')
        # Creating the point constraint keeping the aim locator on the bot2_jnt joint
        cmds.pointConstraint(self.rk_bot2_jnt, self.l_aim, weight=1, maintainOffset=False,
                             name=f'point_constraint__from_{self.rk_bot2_jnt}')
        # Creating the parent constraint of the bot2_jnt joint to the up locator to maintain its position
        cmds.parentConstraint(self.rk_bot2_jnt, self.l_up, mo=True,
                              name=f'parent_constraint__from_{self.rk_bot2_jnt}')

    def create_falloff_twist(self, name, xform_to_match, aim_loc, target_loc, grp):
        if self.count < 1:
            count = 1
        elif self.count > 3:
            count = 3
        else:
            count = self.count

        locators = []

        weight_ratio = {25: (0.75, 0.25), 33: (0.67, 0.33), 50: (1, 1), 66: (0.33, 0.67), 75: (0.25, 0.75)}
        md_connections = {25: "outputY", 33: "outputX", 50: "outputX", 66: "outputY", 75: "outputZ"}

        if cmds.objExists(f"{name}_Twist_Falloff_MD"):
            mult_div = f"{name}_Twist_Falloff_MD"
        else:
            mult_div = cmds.shadingNode('multiplyDivide', name=f"{name}_Twist_Falloff_MD", asUtility=True)
        cmds.setAttr(f"{mult_div}.operation", 1)

        if count == 1:
            if not cmds.isConnected(f"{aim_loc}.rotateX", f"{mult_div}.input1X"):
                cmds.connectAttr(f"{aim_loc}.rotateX", f"{mult_div}.input1X", force=True)
            cmds.setAttr(f"{mult_div}.input2X", 0.5)

        elif count == 2:
            cmds.setAttr(f"{mult_div}.input2X", 0.33)
            cmds.setAttr(f"{mult_div}.input2Y", 0.66)
            if not cmds.isConnected(f"{aim_loc}.rotateX", f"{mult_div}.input1X"):
                cmds.connectAttr(f"{aim_loc}.rotateX", f"{mult_div}.input1X", force=True)
            if not cmds.isConnected(f"{aim_loc}.rotateX", f"{mult_div}.input1Y"):
                cmds.connectAttr(f"{aim_loc}.rotateX", f"{mult_div}.input1Y", force=True)

        else:
            if not cmds.isConnected(f"{aim_loc}.rotateX", f"{mult_div}.input1X"):
                cmds.connectAttr(f"{aim_loc}.rotateX", f"{mult_div}.input1X", force=True)
            if not cmds.isConnected(f"{aim_loc}.rotateX", f"{mult_div}.input1Y"):
                cmds.connectAttr(f"{aim_loc}.rotateX", f"{mult_div}.input1Y", force=True)
            if not cmds.isConnected(f"{aim_loc}.rotateX", f"{mult_div}.input1Z"):
                cmds.connectAttr(f"{aim_loc}.rotateX", f"{mult_div}.input1Z", force=True)
            cmds.setAttr(f"{mult_div}.input2X", 0.5)
            cmds.setAttr(f"{mult_div}.input2Y", 0.25)
            cmds.setAttr(f"{mult_div}.input2Z", 0.75)

        for i in range(count):
            percent = int(100 / (count + 1)) * (i + 1)
            percent_string = f"{percent}" if percent != 50 else "Mid"
            locator = cmds.spaceLocator(name=f"{name}_{percent_string}_Loc")[0]
            locators.append(locator)
            loc_xform = XformHandler(locator)
            loc_xform.match_xform(xform_to_match, ["translate", "rotate"])
            cmds.parent(locator, grp)

            # Creating the dynamic point constraint holding the middle locator between the two joints
            pt_constraint = cmds.pointConstraint(target_loc, aim_loc, locator, weight=1,
                                                 maintainOffset=False,
                                                 name=f'point_constraint__from_{target_loc}_and_{aim_loc}')[0]

            cmds.setAttr(f"{pt_constraint}.{target_loc}W0", weight_ratio[percent][0])
            cmds.setAttr(f"{pt_constraint}.{aim_loc}W1", weight_ratio[percent][1])
            if not cmds.isConnected(f"{mult_div}.{md_connections[percent]}", f"{locator}.rotateX"):
                cmds.connectAttr(f"{mult_div}.{md_connections[percent]}", f"{locator}.rotateX", force=True)

        return locators

    def create_twist_joints(self, name, loc_grp, initial_locator, parent_joint):
        if type(loc_grp) is not list:
            loc_grp = [loc_grp]
        loc_grp.append(initial_locator)

        twist_joints = []
        for i, locator in enumerate(loc_grp):
            twist_joint = cmds.joint(name=f"{name}_Twist_{str(i + 1).zfill(2)}_Jnt", radius=self.radius)
            cmds.select(clear=True)
            twist_joints.append(twist_joint)
            twist_jnt_xform = XformHandler(twist_joint)
            loc_xform = XformHandler(locator)
            twist_jnt_xform.match_xform(loc_xform, "translate")
            cmds.parent(twist_joint, parent_joint)
            cmds.makeIdentity(twist_joint, apply=True, rotate=1)
            twist_jnt_xform.set_xform("jointOrient", zero_out=True)

            cmds.parentConstraint(locator, twist_joint, maintainOffset=False,
                                  name=f'parent_constraint__from_{locator}')

        return twist_joints

    def clean_up(self):
        _group = cmds.group(name="Limb_Twist_Grp", empty=True) if not cmds.objExists(
            "Limb_Twist_Grp") else "Limb_Twist_Grp"

        cmds.parent(self.l_loc_grp, self.l_full_grp)
        if self.get_limb() == "Arm":
            cmds.parent(self.helper_jnt_grp, self.u_full_grp)
        cmds.parent(self.u_loc_grp, self.u_full_grp)
        cmds.parent(self.l_full_grp, self.u_full_grp, _group)

        if cmds.objExists("Deformers"):
            if "Limb_Twist_Grp" not in cmds.listRelatives("Deformers", children=True):
                cmds.parent(_group, "Deformers")

        self._set_locator_scale()

    def color_twist_system(self, twist_color="White"):
        twist_objects_to_color = (self.u_twist_joints + self.l_twist_joints + self.u_twist_locators +
                                  self.l_twist_locators)
        twist_objects_to_color += [self.u_aim, self.u_target, self.u_up, self.l_aim, self.l_target, self.l_up]
        change_color(twist_color, twist_objects_to_color)

    def color_helpers(self, helper_color="Black"):
        helper_objects_to_color = [self.helper_pv_locator, self.helper_joint1, self.helper_joint2,
                                   self.helper_top_joint_correcter]
        change_color(helper_color, helper_objects_to_color)


if __name__ == "__main__":
    from functools import partial

    def module_name():
        import inspect
        import os
        # Get the current frame and find the file name of the script
        frame = inspect.currentframe()
        filename = inspect.getfile(frame)
        return os.path.basename(filename).split('.')[0]

    print(f"\n{'-' * 25 + '|' + ' ' * 4} RUNNING {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 25}")

    def perform_l_arm(selection, twist_count=1):
        return LimbTwistManager("L_Arm", "L_Upper_Arm", "L_ForeArm", selection[0], selection[1], selection[2],
                                selection[3], twist_count=twist_count, aim_vector=(1, 0, 0), up_vector=(0, 1, 0))

    def perform_r_arm(selection, twist_count=1):
        return LimbTwistManager("R_Arm", "R_Upper_Arm", "R_ForeArm", selection[0], selection[1], selection[2],
                                selection[3], twist_count=twist_count, aim_vector=(1, 0, 0), up_vector=(0, 1, 0))

    def perform_l_leg(selection, twist_count=1):
        return LimbTwistManager("L_Leg", "L_Upper_Leg", "L_Lower_Leg", selection[0], selection[1], selection[2],
                                selection[3], twist_count=twist_count, aim_vector=(1, 0, 0), up_vector=(0, -1, 0))

    def perform_r_leg(selection, twist_count=1):
        return LimbTwistManager("R_Leg", "R_Upper_Leg", "R_Lower_Leg", selection[0], selection[1], selection[2],
                                selection[3], twist_count=twist_count, aim_vector=(1, 0, 0), up_vector=(0, 0, 1))

    def perform_func_call(excluded=None):
        excluded = [] if not excluded else excluded

        run_parameters = {"arm": {'u_up_axis': "-y", 'l_up_axis': "y", 'u_helper_axis': "z", 'correct_percent': 10},
                          "leg": {'u_up_axis': "y", 'l_up_axis': "z", 'correct_percent': 10}}

        functions = [partial(perform_l_arm, ["L_Arm_01_RK_Jnt", "L_Arm_02_RK_Jnt", "L_Arm_03_RK_Jnt", "L_Hand_FK_Jnt"],
                             twist_count=1),
                     partial(perform_r_arm, ["R_Arm_01_RK_Jnt", "R_Arm_02_RK_Jnt", "R_Arm_03_RK_Jnt", "R_Hand_FK_Jnt"],
                             twist_count=1),
                     partial(perform_l_leg,
                             ["L_Leg_01_RK_Jnt", "L_Leg_02_RK_Jnt", "L_Leg_03_RK_Jnt", "L_Foot_01_RK_Jnt"],
                             twist_count=1),
                     partial(perform_r_leg,
                             ["R_Leg_01_RK_Jnt", "R_Leg_02_RK_Jnt", "R_Leg_03_RK_Jnt", "R_Foot_01_RK_Jnt"],
                             twist_count=1)]

        for i, func in enumerate(functions):
            if i not in excluded:
                func().run(**run_parameters["arm" if i < 2 else "leg"])

    def toggle_twist_grp_visibility():
        cmds.setAttr("Limb_Twist_Grp.visibility", 1 - cmds.getAttr("Limb_Twist_Grp.visibility"))

    perform_func_call([2, 3])
    # perform_func_call()
    # toggle_twist_grp_visibility()

    print(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED {module_name()}  DUNDER MAIN {' ' * 4 + '|' + '-' * 25}\n")
