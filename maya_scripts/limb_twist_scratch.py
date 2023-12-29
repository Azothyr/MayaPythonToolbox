import maya.cmds as cmds
from core.components.xform_handler import XformHandler, Calculator3dSpace
from core.components.color_changer import change_color


class LimbTwistManager:
    def __init__(self, limb_name, upper_name, lower_name, rk_top_jnt, rk_pivot_jnt, rk_bot_jnt, rk_bot2_jnt,
                 twist_count=1):
        # self.calculator = Calculator3dSpace()

        self.limb_name = limb_name
        self.upper_name = upper_name
        self.lower_name = lower_name
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
        self.calculator = Calculator3dSpace(self.top_jnt_xform)

        self.aim_axis = self.__set_aim_axis()
        self.up_axis = self.__set_up_axis()
        self.rotate_axis = self.__set_rotate_axis()
        self.radius = self._set_radius()
        self.helper_top_joint_correcter = cmds.joint(name=f"{self.upper_name}_Twist_01_Corrective_Jnt",
                                                     radius=self.radius)
        self.correcter_xform = XformHandler(self.helper_top_joint_correcter)
        cmds.select(clear=True)

        # Creating upper locators and group
        self.upper_full_grp = cmds.group(empty=True, name=f"{self.upper_name}_Twist_Grp")
        self.upper_loc_grp = cmds.group(empty=True, name=f"{self.upper_name}_Loc_Grp")
        self.upper_aim_loc = cmds.spaceLocator(name=f"{self.upper_name}_Aim_Loc")[0]
        self.upper_target_loc = cmds.spaceLocator(name=f"{self.upper_name}_Target_Loc")[0]
        self.upper_up_loc = cmds.spaceLocator(name=f"{self.upper_name}_Up_Loc")[0]
        self.upper_twist_joints = None
        self.upper_twist_locators = None
        self.upper_loc_grp_xform = XformHandler(self.upper_loc_grp)
        self.upper_aim_loc_xform = XformHandler(self.upper_aim_loc)
        self.upper_target_loc_xform = XformHandler(self.upper_target_loc)
        self.upper_up_loc_xform = XformHandler(self.upper_up_loc)
        cmds.select(clear=True)

        # Creating upper arm helpers
        self.helper_jnt_grp = cmds.group(empty=True, name=f"{self.upper_name}_Twist_IK_Jnt_Grp")
        self.helper_pv_locator = cmds.spaceLocator(name=f"{self.upper_name}_Twist_PV_Loc")[0] if (self.get_limb()
                                                                                                  == "Arm") else None
        cmds.select(clear=True)
        self.helper_joint1 = cmds.joint(name=f"{self.upper_name}_Twist_IK_01_Jnt", radius=self.radius)
        cmds.select(clear=True)
        self.helper_joint2 = cmds.joint(name=f"{self.upper_name}_Twist_IK_02_Jnt", radius=self.radius)
        cmds.select(clear=True)
        self.loc_pv_xform = XformHandler(self.helper_pv_locator) if self.get_limb() == "Arm" else None
        self.help_jnt_grp_xform = XformHandler(self.helper_jnt_grp)
        self.help_jnt1_xform = XformHandler(self.helper_joint1)
        self.help_jnt2_xform = XformHandler(self.helper_joint2)

        # Creating lower locators and group
        self.lower_full_grp = cmds.group(empty=True, name=f"{self.lower_name}_Twist_Grp")
        self.lower_loc_grp = cmds.group(empty=True, name=f"{self.lower_name}_Loc_Grp")
        self.lower_twist_joints = None
        self.lower_twist_locators = None
        self.lower_aim = cmds.spaceLocator(name=f"{self.lower_name}_Aim_Loc")[0]
        self.lower_target_loc = cmds.spaceLocator(name=f"{self.lower_name}_Target_Loc")[0]
        self.lower_up_loc = cmds.spaceLocator(name=f"{self.lower_name}_Up_Loc")[0]
        self.lower_loc_grp_xform = XformHandler(self.lower_loc_grp)
        self.lower_aim_xform = XformHandler(self.lower_aim)
        self.lower_target_loc_xform = XformHandler(self.lower_target_loc)
        self.lower_up_loc_xform = XformHandler(self.lower_up_loc)
        cmds.select(clear=True)

    def run(self, correct_percent=None, l_up_dist=None, upper_up_loc_dist=None, upper_helper_dist=None):
        self.create_upper_twist_system(upper_up_loc_dist, upper_helper_dist, correct_percent)
        self.create_lower_twist_system(l_up_dist)
        self.clean_up()
        self._set_locator_scale()
        self.connect_to_rig()
        self.color_twist_system()
        self.color_helpers()
        print(f"Twist system created for {self.upper_name} and {self.lower_name}.\n")

    def get_side(self):
        if self.limb_name is None:
            return
        return self.limb_name.split("_")[0].upper()

    def get_limb(self):
        if self.limb_name is None:
            return
        return self.limb_name.split("_")[1].capitalize()

    def __set_aim_axis(self):
        upper_aim = self.get_aim_axis(self.top_jnt_xform, self.pivot_jnt_xform)
        lower_aim = self.get_aim_axis(self.pivot_jnt_xform, self.bot_jnt_xform)
        if upper_aim == lower_aim:
            return upper_aim
        else:
            raise ValueError(f"Upper and lower aim axis do not match: {upper_aim}, {lower_aim}.")

    def __set_up_axis(self):
        upper_up_loc = self.top_jnt_xform.calc.calculate_local_axes_relativity_to_world()
        middle_up = self.pivot_jnt_xform.calc.calculate_local_axes_relativity_to_world()
        lower_up_loc = self.bot_jnt_xform.calc.calculate_local_axes_relativity_to_world()
        if upper_up_loc == lower_up_loc == middle_up:
            return upper_up_loc["z"]
        else:
            raise ValueError(f"Upper and lower up axis do not match: {upper_up_loc}, {lower_up_loc}.")

    def __set_rotate_axis(self):
        aim_axis = self.aim_axis.replace("-", "") if "-" in self.aim_axis else self.aim_axis
        up_axis = self.up_axis.replace("-", "") if "-" in self.up_axis else self.up_axis
        match aim_axis:
            case "x":
                match up_axis:
                    case "y": return "z"
                    case "z": return "y"
            case "y":
                match up_axis:
                    case "x": return "z"
                    case "z": return "x"
            case "z":
                match up_axis:
                    case "x": return "y"
                    case "y": return "x"

    def set_joint_to_orientation(self, joint, orientation=None, **kwargs):
        if orientation is None:
            aim_axis = self.aim_axis.replace("-", "") if "-" in self.aim_axis else self.aim_axis
            rotate_axis = self.rotate_axis.replace("-", "") if "-" in self.rotate_axis else self.rotate_axis
            up_axis = self.up_axis.replace("-", "") if "-" in self.up_axis else self.up_axis
            orientation = f"{aim_axis}{rotate_axis}{up_axis}"
        cmds.joint(joint, edit=True, orientJoint=orientation, zeroScaleOrient=kwargs.get("zeroScale", True),
                   secondaryAxisOrient=kwargs.get("secondary", "ydown"),
                   children=kwargs.get("children", True))

    @staticmethod
    def get_aim_vector(src_xform: XformHandler, target_xform: XformHandler):
        return src_xform.calc.calculate_aim_axis_vector(target_xform, True)

    def get_aim_axis(self, src_xform: XformHandler, target_xform: XformHandler):
        return src_xform.calc.get_axis_from_vector(self.get_aim_vector(src_xform, target_xform))

    def connect_to_rig(self):
        if self.limb_name is None:
            return
        side = self.get_side()
        limb = self.get_limb()
        if side not in ["L", "R"]:
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
        for loc in locators:
            shape = cmds.listRelatives(loc, shapes=True)[0] if cmds.listRelatives(loc, shapes=True) else None
            if shape:
                for axis in "XYZ":
                    cmds.setAttr(f"{shape}.localScale{axis}", scale)

    def create_upper_twist_system(self, up_dist=None, helper_dist=None, correct_percent=None):
        self.create_upper_twist_base(up_dist=up_dist)
        cmds.select(clear=True)
        self.create_upper_limb_helpers(helper_dist=helper_dist)
        cmds.select(clear=True)
        self.upper_twist_locators = self.create_falloff_twist(self.upper_name, self.top_jnt_xform, self.upper_aim_loc,
                                                              self.upper_target_loc, self.upper_loc_grp)
        cmds.select(clear=True)
        self.upper_twist_joints = self.create_twist_joints(self.upper_name, self.upper_twist_locators,
                                                           self.upper_target_loc, self.rk_top_jnt)
        cmds.select(clear=True)
        self.create_upper_twist_corrective(correct_percent)
        cmds.select(clear=True)

    def create_upper_twist_base(self, up_dist=None):
        if up_dist is None:
            base_dist = self.top_jnt_xform.calc.calculate_distance(self.pivot_jnt_xform)
            up_dist = int(base_dist * 0.9)
            if "-" in self.up_axis:
                up_dist *= -1
            if self.get_limb() == "Arm":
                up_dist *= -1

        # Setting to locator positions
        for obj in [self.upper_loc_grp_xform, self.upper_aim_loc_xform]:
            obj.match_xform(self.rk_top_jnt, "translate")
        for obj in [self.upper_target_loc_xform, self.upper_up_loc_xform]:
            obj.match_xform(self.rk_pivot_jnt, "translate")
        for obj in [self.upper_loc_grp_xform, self.upper_aim_loc_xform, self.upper_target_loc_xform, self.upper_up_loc_xform]:
            obj.match_xform(self.rk_top_jnt, "rotate")

        up_axis = self.up_axis.replace("-", "") if "-" in self.up_axis else self.up_axis
        if self.get_limb() == "Leg":
            up_vector = self.calculator.get_vector_from_axis(self.up_axis)
        else:
            up_vector = self.up_axis.replace("-", "") if "-" in self.up_axis else f"-{self.up_axis}"
            up_vector = self.calculator.get_vector_from_axis(up_vector)
        aim_vector = self.calculator.get_vector_from_axis(self.aim_axis)

        # Moving the aim locator 'up_dist' units in up_axis
        self.upper_up_loc_xform.add_in_local('translate', **{up_axis: up_dist})
        cmds.parent(self.upper_aim_loc, self.upper_target_loc, self.upper_up_loc, self.upper_loc_grp)
        # Locking the position of the group to the top_jnt
        cmds.parentConstraint(self.rk_top_jnt, self.upper_loc_grp, maintainOffset=True,
                              name=f'parent_constraint__from_{self.rk_top_jnt}')
        # Locking the scale of the group to the top_jnt
        cmds.scaleConstraint(self.rk_top_jnt, self.upper_loc_grp, maintainOffset=True,
                             name=f"scale_constraint__from_{self.rk_top_jnt}")
        # Creating the locator aim constraint
        cmds.aimConstraint(self.upper_target_loc, self.upper_aim_loc, worldUpType="object", upVector=up_vector,
                           weight=1, aimVector=aim_vector, maintainOffset=False, worldUpObject=self.upper_up_loc,
                           name=f'aim_constraint__from_{self.upper_target_loc}__up_vector_to_{self.upper_up_loc}')
        # Point constraint keeping the target locator on the pivot_jnt
        cmds.pointConstraint(self.rk_pivot_jnt, self.upper_target_loc, weight=1, maintainOffset=True,
                             name=f'point_constraint__from_{self.upper_target_loc}')

    def create_upper_limb_helpers(self, helper_dist=None):
        if helper_dist is None:
            base_dist = self.top_jnt_xform.calc.calculate_distance(self.pivot_jnt_xform)
            helper_dist = int(base_dist + (base_dist * 0.15)) * -1

        up_axis = self.up_axis.replace("-", "") if "-" in self.up_axis else self.up_axis
        rotate_axis = self.rotate_axis.replace("-", "") if "-" in self.rotate_axis else self.rotate_axis

        # Setting the helper joint1 to the position of the top_jnt
        self.help_jnt1_xform.match_xform(self.top_jnt_xform, "translate")
        # Setting the helper joint2 to the position of the pivot_jnt
        self.help_jnt2_xform.match_xform(self.pivot_jnt_xform, "translate")

        if self.get_limb() == "Arm":
            self.help_jnt1_xform.add_in_world('translate', **{rotate_axis: helper_dist})
        # Moving the helper joint2 to be halfway between helper 1 and the pivot_jnt
        self.help_jnt2_xform.move_relative_to_obj(self.help_jnt1_xform,
                                                  self.help_jnt2_xform.calc.calculate_distance(self.help_jnt1_xform)*0.5)
        cmds.parent(self.helper_joint2, self.helper_joint1)
        # Orienting the helper joints
        self.set_joint_to_orientation(self.helper_joint1)
        # Setting the joint orient of the second helper joint to be the same as the first
        self.help_jnt2_xform.set_xform("jointOrient", zero_out=True)

        # Creating the group for the helper joints
        self.help_jnt_grp_xform.match_xform(self.help_jnt1_xform, ["translate", "rotate"])
        self.help_jnt_grp_xform.set_attribute_x("rotate", 0)

        # Creating the IK handle for the helper joints
        cmds.ikHandle(startJoint=self.helper_joint1, endEffector=self.helper_joint2, solver="ikRPsolver",
                      name=f"{self.upper_name}_Twist_IK_Handle")

        # Deselecting all created objects
        cmds.select(clear=True)

        if self.get_limb() == "Arm":
            # Setting the position of the pole vector locator
            self.loc_pv_xform.match_xform(self.help_jnt1_xform, "translate")
            # Moving the pole vector locator 3 units in the y-axis
            distance = abs(helper_dist) / 2 if abs(helper_dist) > 5 else 5
            self.loc_pv_xform.add_in_world('translate', **{up_axis: distance})
            # Creating the pole vector constraint
            cmds.poleVectorConstraint(self.helper_pv_locator, f"{self.upper_name}_Twist_IK_Handle", weight=1,
                                      name=f'pole_vector_constraint__from_{self.helper_pv_locator}')

        # Point constraint keeping the ik handle pointing at the pivot_jnt
        cmds.pointConstraint(self.rk_pivot_jnt, f"{self.upper_name}_Twist_IK_Handle", weight=1, maintainOffset=False,
                             name=f'point_constraint__from_{self.rk_pivot_jnt}')

        # Setting all pieces of the helper group to be children of the helper group
        cmds.parent(self.helper_joint1, f"{self.upper_name}_Twist_IK_Handle",
                    self.helper_jnt_grp)
        if self.get_limb() == "Arm":
            cmds.parent(self.helper_pv_locator, self.helper_jnt_grp)

        # Parent constraint keeping the up locator's position relative to the helper 1 joint
        cmds.parentConstraint(self.helper_joint1, self.upper_up_loc, mo=True,
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
        self.upper_twist_joints.append(self.helper_top_joint_correcter)

    def create_lower_twist_system(self, up_dist=None):
        self.create_lower_twist_base(up_dist=up_dist)
        cmds.select(clear=True)
        self.lower_twist_locators = self.create_falloff_twist(self.lower_name, self.pivot_jnt_xform, self.lower_aim,
                                                          self.lower_target_loc, self.lower_loc_grp)
        cmds.select(clear=True)
        self.lower_twist_joints = self.create_twist_joints(self.lower_name, self.lower_twist_locators, self.lower_aim,
                                                       self.rk_pivot_jnt)
        cmds.select(clear=True)

    def create_lower_twist_base(self, up_dist=None):
        if up_dist is None:
            base_dist = self.pivot_jnt_xform.calc.calculate_distance(self.bot_jnt_xform)
            up_dist = int(base_dist / 4)
            if self.get_side() == "R":
                up_dist *= -1

        # Setting to joint positions
        for obj in [self.lower_loc_grp_xform, self.lower_aim_xform, self.lower_up_loc_xform]:
            obj.match_xform(self.bot_jnt_xform, "translate")
        self.lower_target_loc_xform.match_xform(self.pivot_jnt_xform, "translate")
        for obj in [self.lower_loc_grp_xform, self.lower_aim_xform, self.lower_target_loc_xform, self.lower_up_loc_xform]:
            obj.match_xform(self.bot_jnt_xform, "rotate")

        up_axis = self.up_axis.replace("-", "") if "-" in self.up_axis else self.up_axis
        if self.get_limb() == "Leg":
            up_axis = self.rotate_axis.replace("-", "") if "-" in self.rotate_axis else self.rotate_axis
        aim_axis = self.get_aim_axis(self.bot_jnt_xform, self.pivot_jnt_xform)
        up_vector = self.calculator.get_vector_from_axis(self.up_axis) if self.get_limb() == "Arm" else\
            self.calculator.get_vector_from_axis(f"-{self.rotate_axis}") if self.get_side() == "R" else\
            self.calculator.get_vector_from_axis(self.rotate_axis)
        aim_vector = self.calculator.get_vector_from_axis(aim_axis)

        cmds.parent(self.lower_aim, self.lower_target_loc, self.lower_up_loc, self.lower_loc_grp)

        self.lower_up_loc_xform.add_in_world('translate', **{up_axis: up_dist})

        # Locking the position of the group to the pivot_jnt
        cmds.parentConstraint(self.rk_pivot_jnt, self.lower_loc_grp, mo=True,
                              name=f'parent_constraint__from_{self.rk_pivot_jnt}')
        cmds.scaleConstraint(self.rk_pivot_jnt, self.lower_loc_grp, maintainOffset=True,
                             name=f"scale_constraint__from_{self.rk_pivot_jnt}")
        # # Creating the locator aim constraint
        cmds.aimConstraint(self.lower_target_loc, self.lower_aim, worldUpType="object", upVector=up_vector,
                           aimVector=aim_vector, worldUpObject=self.lower_up_loc, weight=1, maintainOffset=False,
                           name=f'aim_constraint__from_{self.lower_target_loc}')
        # Creating the point constraint keeping the aim locator on the bot2_jnt joint
        cmds.pointConstraint(self.rk_bot2_jnt, self.lower_aim, weight=1, maintainOffset=False,
                             name=f'point_constraint__from_{self.rk_bot2_jnt}')
        # Creating the parent constraint of the bot2_jnt joint to the up locator to maintain its position
        cmds.parentConstraint(self.rk_bot2_jnt, self.lower_up_loc, mo=True,
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

        match count:
            case 1:
                if not cmds.isConnected(f"{aim_loc}.rotateX", f"{mult_div}.input1X"):
                    cmds.connectAttr(f"{aim_loc}.rotateX", f"{mult_div}.input1X", force=True)
                cmds.setAttr(f"{mult_div}.input2X", 0.5)

            case 2:
                cmds.setAttr(f"{mult_div}.input2X", 0.33)
                cmds.setAttr(f"{mult_div}.input2Y", 0.66)
                if not cmds.isConnected(f"{aim_loc}.rotateX", f"{mult_div}.input1X"):
                    cmds.connectAttr(f"{aim_loc}.rotateX", f"{mult_div}.input1X", force=True)
                if not cmds.isConnected(f"{aim_loc}.rotateX", f"{mult_div}.input1Y"):
                    cmds.connectAttr(f"{aim_loc}.rotateX", f"{mult_div}.input1Y", force=True)

            case 3:
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

        cmds.parent(self.lower_loc_grp, self.lower_full_grp)
        cmds.parent(self.helper_jnt_grp, self.upper_full_grp)
        cmds.parent(self.upper_loc_grp, self.upper_full_grp)
        cmds.parent(self.lower_full_grp, self.upper_full_grp, _group)

        if cmds.objExists("Deformers"):
            if "Limb_Twist_Grp" not in cmds.listRelatives("Deformers", children=True):
                cmds.parent(_group, "Deformers")

    def color_twist_system(self, twist_color="White"):
        twist_objects_to_color = (self.upper_twist_joints + self.lower_twist_joints + self.upper_twist_locators +
                                  self.lower_twist_locators)
        twist_objects_to_color += [self.upper_aim_loc, self.upper_target_loc, self.upper_up_loc, self.lower_aim,
                                   self.lower_target_loc, self.lower_up_loc]
        change_color(twist_color, twist_objects_to_color)

    def color_helpers(self, helper_color="Black"):
        helper_objects_to_color = [self.helper_joint1, self.helper_joint2, self.helper_top_joint_correcter]
        if self.get_limb() == "Arm":
            helper_objects_to_color.append(self.helper_pv_locator)
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
                                selection[3], twist_count=twist_count)

    def perform_r_arm(selection, twist_count=1):
        return LimbTwistManager("R_Arm", "R_Upper_Arm", "R_ForeArm", selection[0], selection[1], selection[2],
                                selection[3], twist_count=twist_count)

    def perform_l_leg(selection, twist_count=1):
        return LimbTwistManager("L_Leg", "L_Upper_Leg", "L_Lower_Leg", selection[0], selection[1], selection[2],
                                selection[3], twist_count=twist_count)

    def perform_r_leg(selection, twist_count=1):
        return LimbTwistManager("R_Leg", "R_Upper_Leg", "R_Lower_Leg", selection[0], selection[1], selection[2],
                                selection[3], twist_count=twist_count)

    def perform_func_call(excluded=None):
        excluded = [] if not excluded else excluded

        run_parameters = {"arm": {'correct_percent': 10},
                          "leg": {'correct_percent': 10}}

        functions = [partial(perform_l_arm,
                             ["L_Arm_01_RK_Jnt", "L_Arm_02_RK_Jnt", "L_Arm_03_RK_Jnt", "L_Hand_FK_Jnt"],
                             twist_count=1),
                     partial(perform_r_arm,
                             ["R_Arm_01_RK_Jnt", "R_Arm_02_RK_Jnt", "R_Arm_03_RK_Jnt", "R_Hand_FK_Jnt"],
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

    # perform_func_call([0, 1])
    # perform_func_call()
    toggle_twist_grp_visibility()

    print(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED {module_name()}  DUNDER MAIN {' ' * 4 + '|' + '-' * 25}\n")
