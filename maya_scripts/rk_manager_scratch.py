import maya.cmds as cmds
from core.maya_objects.joint_manager import JointManager


class RkManager:
    def __init__(self, controller='Transform_Ctrl'):
        if not cmds.objExists(controller):
            raise ValueError(f"ERROR: The CONTROLLER of the RK system {controller} does not exist.")
        self.controller = controller
        self.joint_manager = JointManager(combine=True, get='rk')
        self.rk_joints = self.joint_manager.data['RK'].items()

    def run(self):
        for part, data in self.rk_joints:
            if 'Foot' in part:
                self.create_attributes(f"{part[0]}_Leg")
            else:
                self.create_attributes(part)
            # print(f"Creating constraints for {part}")
            for rk_joint in data['joints']:
                fk_joint = rk_joint.replace("_RK", "_FK")
                ik_joint = rk_joint.replace("_RK", "_IK")
                # print(f"Confirming {rk_joint}, {fk_joint}, and {ik_joint} Exist.")
                if not cmds.objExists(fk_joint) or not cmds.objExists(ik_joint):
                    raise ValueError(f"WARNING: {fk_joint} or {ik_joint} does not exist.")
                else:
                    constraints = self.create_constraints(fk_joint, ik_joint, rk_joint)
                    self.connect_attributes(part, constraints)

    def create_attributes(self, part):
        attr = f"{part}_IKFK"
        # print(f"Creating attribute {attr} to RK CONTROLLER {self.controller}")

        # Create attributes on the RK controller if not already there
        if not cmds.attributeQuery(attr, node=self.controller, exists=True):
            cmds.addAttr(self.controller, ln=attr, at='float', min=0, max=1, dv=1)
            cmds.setAttr('%s.%s' % (self.controller, attr), e=True, keyable=True)

        else:
            print(f"WARNING: {attr} already exists on {self.controller}")

    @staticmethod
    def create_constraints(fk_leader, ik_leader, constrained_rk):
        if not cmds.objExists(fk_leader):
            raise ValueError(f"WARNING: {fk_leader} or {ik_leader} does not exist.")
        name = constrained_rk.split('_RK')[0]
        # print(f"Creating constraints for LEADER {fk_leader}, {ik_leader} to FOLLOWER {constrained_rk}")
        parent_constraint = cmds.parentConstraint(fk_leader, ik_leader, constrained_rk,
                                                  name=f'{name}_IKFK_Constraining_{constrained_rk}_TRANSLATION'
                                                       f'_ROTATION__parent_constraint', mo=False, weight=1)[0]

        scale_constraint = cmds.scaleConstraint(fk_leader, ik_leader, constrained_rk,  # noqa
                                                name=f'{name}_IKFK_Constraining_{constrained_rk}_SCALE_'
                                                     f'_parent_constraint', weight=1)[0]
        # print(f"Created constraints: {fk_parent_constraint}\n{fk_scale_constraint}\n{ik_parent_constraint}\n"
        #       f"{ik_scale_constraint}")

        return parent_constraint, parent_constraint

    def connect_attributes(self, part, constraints):
        if 'Foot' in part:
            attr = f"{part[0]}_Leg_IKFK"
        else:
            attr = f"{part}_IKFK"
        if not cmds.objExists(f"{attr}_Rev"):
            rev_node = cmds.shadingNode('reverse', name=f"{attr}_Rev", asUtility=True)
        else:
            rev_node = f"{attr}_Rev"
        # print(f"Connecting attributes {attr} on {self.controller} to {constraints}")

        for constraint in constraints:
            # print(cmds.listAttr(constraint))
            print(f"Connecting {attr} to {constraint}")

            if not cmds.isConnected('%s.%s' % (self.controller, attr), '%s.w0' % constraint):
                cmds.connectAttr('%s.%s' % (self.controller, attr), '%s.w0' % constraint, f=True)

            if not cmds.isConnected('%s.%s' % (self.controller, attr), '%s.inputX' % rev_node):
                cmds.connectAttr('%s.%s' % (self.controller, attr), '%s.inputX' % rev_node, f=True)

            if not cmds.isConnected('%s.outputX' % rev_node, '%s.w1' % constraint):
                cmds.connectAttr('%s.outputX' % rev_node, '%s.w1' % constraint, f=True)
            if 'Foot' in part:
                continue

            if not cmds.isConnected('%s.%s' % (self.controller, attr), '%s.visibility' % f'{part}_FK_Ctrl_Grp'):
                cmds.connectAttr('%s.%s' % (self.controller, attr), '%s.visibility' % f'{part}_FK_Ctrl_Grp', f=True)

            if not cmds.isConnected('%s.outputX' % rev_node, '%s.visibility' % f'{part}_IK_Ctrl_Grp'):
                cmds.connectAttr('%s.outputX' % rev_node, '%s.visibility' % f'{part}_IK_Ctrl_Grp', f=True)


if __name__ == '__main__':
    # sel = cmds.ls(allPaths=True)
    # for item in sel:
    #     if "IKFK" in item:
    #         cmds.delete(item)

    # cmds.parent("R_Foot_01_IK_Jnt", "R_Leg_03_IK_Jnt")
    # cmds.parent("L_Foot_01_IK_Jnt", "L_Leg_03_IK_Jnt")
    # cmds.parent("R_Leg_01_IK_Jnt", "R_Leg_Clav_FK_Jnt")
    # cmds.parent("L_Leg_01_IK_Jnt", "L_Leg_Clav_FK_Jnt")
    # cmds.parent("R_Arm_01_IK_Jnt", "R_Clav_FK_Jnt")
    # cmds.parent("L_Arm_01_IK_Jnt", "L_Clav_FK_Jnt")
    #
    # def remove_constraints_from_object(object_name):
    #     # List all the constraints on the object
    #     constraints = cmds.listRelatives(object_name, type='constraint')
    #
    #     # If no constraints found, print a message and return
    #     if constraints is None:
    #         print(f"No constraints found on object {object_name}.")
    #         return
    #
    #     # Delete each constraint
    #     for constraint in constraints:
    #         cmds.delete(constraint)
    #         print(f"Deleted constraint: {constraint}")
    #
    # def recursive_joint_clean_till_parameter(node, until):
    #     finished = False
    #     children = cmds.listRelatives(node, children=True, path=True)
    #     if children is not None:
    #         for child in children:
    #             if until == child.split("|")[-1][1::]:
    #                 print(f"DELETING {child}")
    #                 cmds.select(child)
    #                 cmds.delete()
    #                 finished = True
    #             elif cmds.nodeType(child) != "joint":
    #                 # print(f"DELETING {child}")
    #                 cmds.delete(child)
    #             else:
    #                 name = child.split("|")[-1]
    #                 new_name = name.replace("_FK", "_RK")
    #                 cmds.select(child)
    #                 child = cmds.rename(new_name)
    #                 if finished:
    #                     return
    #                 recursive_joint_clean_till_parameter(child, until)
    #
    # processing = []
    # joints = cmds.ls(type="joint")
    # for joint in joints:
    #     joint = joint.split("|")[-1]
    #     if "Arm_01_FK_Jnt" in joint or "Leg_01_FK_Jnt" in joint:
    #         processing.append(joint)
    # # print(f"PROCESSING-------{processing}")
    #
    # for joint in processing:
    #     # print(f"WORKING ON {joint}")
    #     rk_joint = joint.replace("_FK", "_RK")
    #     cmds.duplicate(joint, name=rk_joint)
    #     recursive_joint_clean_till_parameter(rk_joint, "_Hand_FK_Jnt")
    #     cmds.select(clear=True)
    #
    # remove_constraints_from_object("L_Hand_FK_Ctrl_Grp")
    # remove_constraints_from_object("R_Hand_FK_Ctrl_Grp")
    #
    # cmds.parent("L_Hand_FK_Jnt", "L_Arm_03_RK_Jnt")
    # cmds.parent("R_Hand_FK_Jnt", "R_Arm_03_RK_Jnt")
    # cmds.parent("L_Foot_Ctrl_Grp", "L_Leg_FK_Ctrl_Grp")
    # cmds.parent("R_Foot_Ctrl_Grp", "R_Leg_FK_Ctrl_Grp")
    #
    # cmds.parentConstraint( "L_Arm_03_RK_Jnt", "L_Hand_FK_Ctrl_Grp", mo=True, weight=1)
    # cmds.scaleConstraint("L_Arm_03_RK_Jnt", "L_Hand_FK_Ctrl_Grp", weight=1)
    #
    # cmds.parentConstraint("R_Arm_03_RK_Jnt", "R_Hand_FK_Ctrl_Grp", mo=True, weight=1)
    # cmds.scaleConstraint("R_Arm_03_RK_Jnt", "R_Hand_FK_Ctrl_Grp", weight=1)
    #
    # cmds.orientConstraint("L_Arm_IK_Tip_Ctrl", "L_Arm_03_IK_Jnt", mo=True, weight=1)
    # cmds.orientConstraint("R_Arm_IK_Tip_Ctrl", "R_Arm_03_IK_Jnt", mo=True, weight=1)
    #
    # cmds.orientConstraint("L_Leg_IK_Tip_Ctrl", "L_Leg_03_IK_Jnt", mo=True, weight=1)
    # cmds.orientConstraint("R_Leg_IK_Tip_Ctrl", "R_Leg_03_IK_Jnt", mo=True, weight=1)
    #
    # cmds.parentConstraint("R_Arm_03_FK_Ctrl", "R_Arm_03_FK_Jnt", mo=True, weight=1)
    # cmds.scaleConstraint("R_Arm_03_FK_Ctrl", "R_Arm_03_FK_Jnt", weight=1)

    # sel = cmds.ls(type="shape")
    # controls = []
    # for item in sel:
    #     if "CtrlShape" in item:
    #         controls.append(item)
    # cmds.select(clear=True)
    # cmds.select(controls)
    # cmds.pickWalk(direction="up")
    # controls = cmds.ls(selection=True)
    # cmds.select(clear=True)
    # for control in controls:
    #     cmds.setAttr(f"{control}.v", lock=True, keyable=False, channelBox=False)
    #     # print(f"CONTROL: {control}\n\tLOCKING AND HIDING ATTRIBUTES")
    # RkManager().run()

    parent_constraints = cmds.ls(type="parentConstraint")
    for constraint in parent_constraints:
        cmds.setAttr(f"{constraint}.interpType", 2)
        print(f"{constraint} set to {cmds.getAttr(f'{constraint}.interpType')}")
    print("---------_____COMPLETE_____---------")

