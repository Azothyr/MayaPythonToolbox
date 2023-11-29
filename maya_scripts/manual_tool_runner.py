import sys
if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' in sys.path:
    sys.path.remove('C:/GitRepos/MayaPythonToolbox/maya_scripts')
if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' not in sys.path:
    sys.path.append('C:/GitRepos/MayaPythonToolbox/maya_scripts')
import maya.cmds as cmds
from pprint import pprint
import re
from tools.xform_handler import XformHandler


class LimbTwistManager:
    def __init__(self, upper_name, lower_name, rk_top_jnt, rk_pivot_jnt, rk_bot_jnt, rk_bot2_jnt, twist_count=1,
                 aim_vector=(1,0,0), up_vector=(0,1,0)):
        self.u_name = upper_name
        self.l_name = lower_name
        self.count = twist_count
        self.rk_top_jnt = rk_top_jnt
        self.rk_pivot_jnt = rk_pivot_jnt
        self.rk_bot_jnt = rk_bot_jnt
        self.rk_bot2_jnt = rk_bot2_jnt
        self.top_jnt_xform =XformHandler(self.rk_top_jnt)
        self.pivot_jnt_xform =XformHandler(self.rk_pivot_jnt)
        self.bot_jnt_xform =XformHandler(self.rk_bot_jnt)
        self.bot2_jnt_xform =XformHandler(self.rk_bot2_jnt)
        # Deselecting all created objects
        cmds.select(clear=True)

        self.radius = self._set_radius()

        # # Creating upper locators and group
        # self.u_twist_grp = cmds.group(empty=True, name=f"{self.u_name}_Loc_Grp")
        # self.u_twist_locators = cmds.group(empty=True, name=f"{self.u_name}_Loc_Grp")
        # self.u_aim = cmds.spaceLocator(name=f"{self.u_name}_Aim_Loc")[0]
        # self.u_target = cmds.spaceLocator(name=f"{self.u_name}_Target_Loc")[0]
        # self.u_up = cmds.spaceLocator(name=f"{self.u_name}_Up_Loc")[0]
        # self.u_group_xform =XformHandler(self.u_twist_grp)
        # self.u_aim_xform =XformHandler(self.u_aim)
        # self.u_target_xform =XformHandler(self.u_target)
        # self.u_up_xform =XformHandler(self.u_up)
        # # Deselecting all created objects
        # cmds.select(clear=True)
        #
        # # Creating upper helpers
        # self.helper_grp = cmds.group(empty=True, name=f"{self.u_name}_Twist_IK_Jnt_Grp")
        # self.helper_pv_locator = cmds.spaceLocator(name=f"{self.u_name}_Twist_PV_Loc")[0]
        # self.helper_joint1 = cmds.joint(name=f"{self.u_name}_Twist_IK_01_Jnt", radius=self.radius)
        # self.helper_joint2 = cmds.joint(name=f"{self.u_name}_Twist_IK_02_Jnt", radius=self.radius)
        # self.loc_pv_xform =XformHandler(self.helper_pv_locator)
        # self.help_jnt1_xform =XformHandler(self.helper_joint1)
        # self.help_jnt2_xform =XformHandler(self.helper_joint2)
        # # Deselecting all created objects
        # cmds.select(clear=True)

        # Creating lower locators and group
        self.l_twist_grp = cmds.group(empty=True, name=f"{self.l_name}_Loc_Grp")
        self.l_twist_joints = None
        self.l_twist_locators = None
        self.l_aim = cmds.spaceLocator(name=f"{self.l_name}_Aim_Loc")[0]
        self.l_target = cmds.spaceLocator(name=f"{self.l_name}_Target_Loc")[0]
        self.l_up = cmds.spaceLocator(name=f"{self.l_name}_Up_Loc")[0]
        self.l_group_xform =XformHandler(self.l_twist_grp)
        self.l_aim_xform =XformHandler(self.l_aim)
        self.l_target_xform =XformHandler(self.l_target)
        self.l_up_xform =XformHandler(self.l_up)
        # Deselecting all created objects
        cmds.select(clear=True)

        self.u_aim_vector = aim_vector
        self.u_up_vector = tuple([up_vector[i] * -1 for i in range(len("xyz"))])
        self.l_aim_vector = tuple([aim_vector[i] * -1 for i in range(len("xyz"))])
        self.l_up_vector = up_vector

    def run(self):
        self.create_lower_twist_system()
        # self.create_upper_twist_system()
        # self.clean_up()
        print(f"Twist system created for {self.u_name} and {self.l_name}.")

    def _set_radius(self):
        radius = cmds.getAttr(f"{self.rk_bot_jnt}.radius") * 0.75
        return radius

    def create_upper_twist_system(self):
        self.create_upper_twist_base()
        cmds.select(clear=True)
        self.create_falloff_twist(self.u_name, self.top_jnt_xform, self.u_aim, self.u_target, self.u_twist_grp)
        cmds.select(clear=True)
        self.create_upper_limb_helpers()
        cmds.select(clear=True)
        self.create_twist_joints(self.u_name, self.u_twist_grp, self.u_target, self.rk_top_jnt)
        cmds.select(clear=True)

    def create_upper_twist_base(self):
        # Setting to joint positions
        for obj in [self.u_group_xform, self.u_aim_xform]:
            obj.match_xform(self.rk_top_jnt, "translate")
        for obj in [self.u_target_xform, self.u_up_xform]:
            obj.match_xform(self.rk_pivot_jnt, "translate")
        for obj in [self.u_group_xform, self.u_aim_xform, self.u_target_xform, self.u_up_xform]:
            obj.match_xform(self.rk_top_jnt, "rotate")
        
        # Moving the aim locator -5 units in the y-axis
        self.u_up_xform.add('translate', y=5)
        cmds.parent(self.u_aim, self.u_target, self.u_up, self.u_twist_grp)

        # Creating constraints

        # Locking the position of the group to the top_jnt
        cmds.parentConstraint(self.rk_top_jnt, self.u_twist_grp, maintainOffset=True,
                              name=f'parent_constraint__from_{self.rk_top_jnt}')
        # Locking the scale of the group to the top_jnt
        cmds.scaleConstraint(self.rk_top_jnt, self.u_twist_grp, maintainOffset=True,
                             name=f"scale_constraint__from_{self.rk_top_jnt}")
        # Creating the locator aim constraint
        cmds.aimConstraint(self.u_target, self.u_aim, worldUpType="object", worldUpVector=self.u_up_vector, weight=1,
                           aimVector=self.u_aim_vector, maintainOffset=False, worldUpObject=self.u_up,
                           name=f'aim_constraint__from_{self.u_target}__up_vector_to_{self.u_up}')
        # Point constraint keeping the target locator on the pivot_jnt
        cmds.pointConstraint(self.rk_pivot_jnt, self.u_target, weight=1, maintainOffset=True,
                             name=f'point_constraint__from_{self.u_target}')
        # Parent constraint keeping the up locator's position relative to the 
        # cmds.parentConstraint(self.rk_pivot_jnt, self.u_up, mo=True, name=f'parent_constraint__from_{self.rk_pivot_jnt}')

    def create_upper_limb_helpers(self):
        # Setting the helper joint1 to the position of the top_jnt
        self.help_jnt1_xform.match_xform(self.rk_top_jnt, "translate")
        # Moving the helper joint1 -3 units in the z axis
        self.help_jnt1_xform.add('translate', z=-3)
        # Setting the helper joint2 to the position of the pivot_jnt
        self.help_jnt2_xform.match_xform(self.rk_pivot_jnt, "translate")
        # Moving the helper joint2 to be halfway between helper 1 and the pivot_jnt
        self.help_jnt2_xform.move_relative_to_obj(self.help_jnt1_xform,
                                                  self.help_jnt2_xform.calculate_distance(self.help_jnt1_xform)/2)
        # Orienting the helper joints
        cmds.joint(self.helper_joint1, edit=True, orientJoint="xzy", secondaryAxisOrient="ydown", children=True,
                   zeroScaleOrient=True)
        # Setting the joint orient of the second helper joint to be the same as the first
        self.help_jnt2_xform.set_xform("jointOrient", zero_out=True)
        # Setting the position of the pole vector locator
        self.loc_pv_xform.match_xform(self.help_jnt1_xform, "translate")
        # Moving the pole vector locator 3 units in the y-axis
        self.loc_pv_xform.add('translate', y=3)

        # Creating the group for the helper joints
        jnt_grp = cmds.group(name=f"{self.u_name}_Twist_IK_Jnt_Grp", empty=True)
        jnt_grp_xform =XformHandler(jnt_grp)
        jnt_grp_xform.match_xform(self.help_jnt1_xform, ["translate", "rotate"])
        jnt_grp_xform.set_attribute_x("rotate", 0)
        cmds.parent(self.helper_joint1, jnt_grp)

        # Creating the IK handle for the helper joints
        cmds.ikHandle(startJoint=self.helper_joint1, endEffector=self.helper_joint2, solver="ikRPsolver",
                      name=f"{self.u_name}_Twist_IK_Handle")

        # Deselecting all objects
        cmds.select(clear=True)

        # Creating the pole vector constraint
        cmds.poleVectorConstraint(self.helper_pv_locator, f"{self.u_name}_Twist_IK_Handle", weight=1,
                                    name=f'pole_vector_constraint__from_{self.helper_pv_locator}')

        # Point constraint keeping the ik handle pointing at the pivot_jnt
        cmds.pointConstraint(self.rk_pivot_jnt, f"{self.u_name}_Twist_IK_Handle", weight=1, maintainOffset=False,
                                name=f'point_constraint__from_{self.rk_pivot_jnt}')

        # Setting all pieces of the helper group to be children of the helper group
        cmds.parent(self.helper_pv_locator, self.helper_joint1, self.helper_joint2, f"{self.u_name}_Twist_IK_Handle",
                    jnt_grp, self.helper_grp)

    def create_lower_twist_system(self):
        self.create_lower_twist_base()
        cmds.select(clear=True)
        # self.l_twist_locators = self.create_falloff_twist(self.l_name, self.pivot_jnt_xform, self.l_aim, self.l_target, self.l_twist_grp)
        cmds.select(clear=True)
        # self.l_twist_joints = self.create_twist_joints(self.l_name, self.l_twist_locators, self.l_aim, self.rk_pivot_jnt)
        cmds.select(clear=True)

    def create_lower_twist_base(self):
        # Setting to joint positions
        for obj in [self.l_group_xform, self.l_aim_xform, self.l_up_xform]:
            obj.match_xform(self.rk_bot_jnt, "translate")
        self.l_target_xform.match_xform(self.rk_pivot_jnt, "translate")
        for obj in [self.l_group_xform, self.l_aim_xform, self.l_target_xform, self.l_up_xform]:
            obj.match_xform(self.rk_bot_jnt, "rotate")

        self.l_up_xform.add('translate', y=-5)

        cmds.parent(self.l_aim, self.l_target, self.l_up, self.l_twist_grp)

        # Creating constraints
        cmds.parentConstraint(self.rk_pivot_jnt, self.l_twist_grp, mo=True, name=f'parent_constraint__from_{self.rk_pivot_jnt}')
        cmds.scaleConstraint(self.rk_pivot_jnt, self.l_twist_grp, maintainOffset=True,
                             name=f"scale_constraint__from_{self.rk_pivot_jnt}")
        # Creating the locator aim constraint
        cmds.aimConstraint(self.l_target, self.l_aim, worldUpType="object", worldUpVector=self.l_up_vector,
                           aimVector=self.l_aim_vector, worldUpObject=self.l_up, weight=1,
                           name=f'aim_constraint__from_{self.l_target}')
        # Creating the point constraint keeping the aim locator on the bot2_jnt joint
        cmds.pointConstraint(self.rk_bot2_jnt, self.l_aim, weight=1, maintainOffset=True,
                             name=f'point_constraint__from_{self.rk_bot2_jnt}')
        # Creating the parent constraint of the bot2_jnt joint to the up locator to maintain its position
        cmds.parentConstraint(self.rk_bot2_jnt, self.l_up, mo=True, name=f'parent_constraint__from_{self.rk_bot2_jnt}')

    def create_falloff_twist(self, name, xform_to_match, aim_loc, target_loc, grp):
        if self.count < 1:
            count = 1
        elif self.count > 3:
            count = 3
        else:
            count = self.count

        locators = []

        weight_ratio = {25: (0.75,0.25), 33: (0.67,0.33), 50: (1,1), 66: (0.33,0.67), 75: (0.25,0.75)}
        md_connections = {25: "outputY", 33: "outputX", 50: "outputX", 66: "outputY", 75: "outputZ"}

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
            percent = int(100 / (count+1)) * (i+1)
            percent_string = f"{percent}" if percent != 50 else "Mid"
            locator = cmds.spaceLocator(name=f"{name}_{percent_string}_Loc")[0]
            locators.append(locator)
            loc_xform =XformHandler(locator)
            loc_xform.match_xform(xform_to_match, "translate")
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
            loc_xform.match_xform(twist_joint, "translate")
            cmds.parent(twist_joint, parent_joint)
            cmds.makeIdentity(twist_joint, apply=True, rotate=1)
            twist_jnt_xform.set_attribute_xyz("jointOrient", 0)

            cmds.parentConstraint(locator, twist_joint, maintainOffset=False,
                                  name=f'parent_constraint__from_{locator}')

        return twist_joints

    def clean_up(self):
        _group = cmds.group(name="Limb_Twist_Loc_Grp", empty=True) if not \
            cmds.objExists("Limb_Twist_Loc_Grp") else "Limb_Twist_Loc_Grp"

        cmds.parent(self.l_twist_grp, self.u_twist_grp, _group)

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
    print(f"\n{'-' * 25 + '|' + ' ' * 4} RUNNING {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 25}")

    selection = cmds.ls(selection=True, type="joint")
    creator = LimbTwistManager("L_Upper_Arm", "L_ForeArm", selection[0], selection[1],
                               selection[2], selection[3], twist_count=1, aim_vector=(1,0,0), up_vector=(0,1,0))
    creator.run()

    print(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED {module_name()}  DUNDER MAIN {' ' * 4 + '|' + '-' * 25}\n")

