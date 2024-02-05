import maya.cmds as cmds
from core.maya_managers.joint_manager import JointManager
import re
"""
2/4/204 last used on imp rig: This is jumbled up but has most of the processes needed to connect the FK and IK joints to the RK joints and set an 
IKFK attribute on the RK controller (Transform_Ctrl).
"""


class RkManager:
    def __init__(self, controller='Transform_Ctrl'):
        if not cmds.objExists(controller):
            raise ValueError(f"ERROR: The CONTROLLER of the RK system {controller} does not exist.")
        self.controller = controller
        self.joint_manager = JointManager(combine=True, get='rk', bypass=True)
        self.rk_joints = self.joint_manager.data['RK']["joints"]

    def run(self):
        for rk_joint in self.rk_joints:
            part = re.split("_rk", rk_joint, flags=re.IGNORECASE)[0]
            if 'foot' in rk_joint.lower():
                self.create_attributes(f"{part[0]}_Leg")
            else:
                self.create_attributes(part)
            # print(f"Creating constraints for {part}")
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
    def create_constraints(fk_leader_jnt, ik_leader_jnt, constrained_rk_jnt):
        if not cmds.objExists(fk_leader_jnt):
            raise ValueError(f"WARNING: {fk_leader_jnt} or {ik_leader_jnt} does not exist.")
        name = constrained_rk_jnt.split('_RK')[0]
        # print(f"Creating constraints for LEADER {fk_leader_jnt}, {ik_leader_jnt} to FOLLOWER {constrained_rk_jnt}")
        parent_constraint = cmds.parentConstraint(fk_leader_jnt, ik_leader_jnt, constrained_rk_jnt,
                                                  name=f'{name}_IKFK_Constraining_{constrained_rk_jnt}_TRANSLATION'
                                                       f'_ROTATION__parent_constraint', mo=False, weight=1)[0]

        scale_constraint = cmds.scaleConstraint(fk_leader_jnt, ik_leader_jnt, constrained_rk_jnt,  # noqa
                                                name=f'{name}_IKFK_Constraining_{constrained_rk_jnt}_SCALE'
                                                     f'_constraint', weight=1)[0]
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
            # if 'foot' in part.lower():
            #     continue

            if not cmds.isConnected('%s.%s' % (self.controller, attr), '%s.visibility' % f'{part}_FK_Ctrl_Grp'):
                cmds.connectAttr('%s.%s' % (self.controller, attr), '%s.visibility' % f'{part}_FK_Ctrl_Grp', f=True)

            if not cmds.isConnected('%s.outputX' % rev_node, '%s.visibility' % f'{part}_IK_Ctrl_Grp'):
                cmds.connectAttr('%s.outputX' % rev_node, '%s.visibility' % f'{part}_IK_Ctrl_Grp', f=True)


if __name__ == '__main__':
    # sel = cmds.ls(allPaths=True)
    # for item in sel:
    #     if "IKFK" in item:
    #         cmds.delete(item)

    # cmds.parent("R_Foot_01_IK_Jnt", "R_Leg_IK_03_Jnt")
    # cmds.parent("L_Foot_01_IK_Jnt", "L_Leg_IK_03_Jnt")
    # cmds.parent("R_Leg_01_IK_Jnt", "R_Leg_Clav_FK_Jnt")
    # cmds.parent("L_Leg_01_IK_Jnt", "L_Leg_Clav_FK_Jnt")
    # cmds.parent("R_Arm_01_IK_Jnt", "R_Clav_FK_Jnt")
    # cmds.parent("L_Arm_01_IK_Jnt", "L_Clav_FK_Jnt")

    """
    # DUPLICATE FK JOINT CHAIN AND PROCESS IT TO BE THE RK JOINT CHAIN 
    def recursive_duplicate_joint_chain_clean_till_parameter(node, until):
        finished = False
        children = cmds.listRelatives(node, children=True, path=True)
        if children is not None:
            for child in children:
                if until == child.split("|")[-1][1::]:
                    print(f"DELETING {child}")
                    cmds.select(child)
                    cmds.delete()
                    finished = True
                elif cmds.nodeType(child) != "joint":
                    # print(f"DELETING {child}")
                    cmds.delete(child)
                else:
                    name = child.split("|")[-1]
                    new_name = name.replace("_FK", "_RK")
                    cmds.select(child)
                    child = cmds.rename(new_name)
                    if finished:
                        return
                    recursive_duplicate_joint_chain_clean_till_parameter(child, until)

    processing = []
    joints = cmds.ls(type="joint")
    for joint in joints:
        joint = joint.split("|")[-1]
        if "Arm_01_FK_Jnt" in joint or "Leg_01_FK_Jnt" in joint:
            processing.append(joint)
    # print(f"PROCESSING-------{processing}")

    for joint in processing:
        # print(f"WORKING ON {joint}")
        rk_joint = joint.replace("_FK", "_RK")
        cmds.duplicate(joint, name=rk_joint)
        recursive_duplicate_joint_chain_clean_till_parameter(rk_joint, "_Hand_FK_Jnt")
        cmds.select(clear=True)
    """

    """
    # SEPARATE THE FK HAND JOINTS FROM THE FK ARM JOINTS AND PARENT THEM TO THE RK ARM JOINTS
    def remove_constraints_from_object(object_name):
        # List all the constraints on the object
        constraints = cmds.listRelatives(object_name, type='constraint')
    
        # If no constraints found, print a message and return
        if constraints is None:
            print(f"No constraints found on object {object_name}.")
            return
    
        # Delete each constraint
        for constraint in constraints:
            cmds.delete(constraint)
            print(f"Deleted constraint: {constraint}")
    remove_constraints_from_object("L_Hand_FK_Ctrl_Grp")
    remove_constraints_from_object("R_Hand_FK_Ctrl_Grp")

    cmds.parent("L_Hand_FK_Jnt", "L_Arm_RK_03_Jnt")
    cmds.parent("R_Hand_FK_Jnt", "R_Arm_RK_03_Jnt")
    cmds.parent("L_Foot_FK_Ctrl_Grp", "L_Leg_FK_Ctrl_Grp")
    cmds.parent("R_Foot_FK_Ctrl_Grp", "R_Leg_FK_Ctrl_Grp")
    """

    """
    # CONSTRAIN THE FK HAND CONTROLS TO THE RK ARM 03 JOINTS
    cmds.parentConstraint( "L_Arm_RK_03_Jnt", "L_Hand_FK_Ctrl_Grp", mo=True, weight=1)
    cmds.scaleConstraint("L_Arm_RK_03_Jnt", "L_Hand_FK_Ctrl_Grp", weight=1)

    cmds.parentConstraint("R_Arm_RK_03_Jnt", "R_Hand_FK_Ctrl_Grp", mo=True, weight=1)
    cmds.scaleConstraint("R_Arm_RK_03_Jnt", "R_Hand_FK_Ctrl_Grp", weight=1)
    
    # CONSTRAIN THE FK AND IK ARM END JOINTS TO THEIR RESPECTIVE CONTROLS AND NOT THE HAND CONTROLS
    cmds.orientConstraint("L_Arm_IK_Tip_Ctrl", "L_Arm_IK_03_Jnt", mo=True, weight=1)
    cmds.orientConstraint("R_Arm_IK_Tip_Ctrl", "R_Arm_IK_03_Jnt", mo=True, weight=1)

    cmds.orientConstraint("L_Leg_IK_Tip_Ctrl", "L_Leg_IK_03_Jnt", mo=True, weight=1)
    cmds.orientConstraint("R_Leg_IK_Tip_Ctrl", "R_Leg_IK_03_Jnt", mo=True, weight=1)

    cmds.parentConstraint("R_Arm_FK_03_Ctrl", "R_Arm_FK_03_Jnt", mo=True, weight=1)
    cmds.parentConstraint("L_Arm_FK_03_Ctrl", "L_Arm_FK_03_Jnt", mo=True, weight=1)
    cmds.scaleConstraint("R_Arm_FK_03_Ctrl", "R_Arm_FK_03_Jnt", weight=1)
    cmds.scaleConstraint("L_Arm_FK_03_Ctrl", "L_Arm_FK_03_Jnt", weight=1)
    """

    cmds.parentConstraint("R_Foot_FK_02_Ctrl", "R_Foot_FK_02_Jnt", mo=True, weight=1)
    cmds.parentConstraint("L_Foot_FK_02_Ctrl", "L_Foot_FK_02_Jnt", mo=True, weight=1)
    cmds.scaleConstraint("R_Foot_FK_02_Ctrl", "R_Foot_FK_02_Jnt", weight=1)
    cmds.scaleConstraint("L_Foot_FK_02_Ctrl", "L_Foot_FK_02_Jnt", weight=1)

    # from scratch.rig_finish_scratch import rig_polish
    # rig_polish()

    """
    # COMBINE ALL CONTROL GROUPS DOWN INTO THEIR PARTS
    # numbered groups go to a side group and the side groups go to the main group
    def safe_parent(child, parent):
        '''
        Safely parents 'child' to 'parent', avoiding errors if 'child' is already a child of 'parent'.
        '''
        # Check if 'child' is already under 'parent' to avoid redundant parenting.
        current_parent = cmds.listRelatives(child, parent=True)
        if current_parent and cmds.ls(current_parent[0], long=True)[0] == cmds.ls(parent, long=True)[0]:
            print(f"Warning: Object, '{child}', skipped. It is already a child of the parent, '{parent}'.")
            return
        try:
            cmds.parent(child, parent)
        except RuntimeError as e:
            print(f"Error: {e}")

    ctrl_names = {
        "arm": ["arm", "fk", "ik", "rk"],
        "arm_clav": ["arm", "fk"],
        "leg": ["leg", "fk", "ik", "rk"],
        "leg_clav": ["leg", "fk"],
        "foot": ["foot", "fk", "ik", "rk"],
        "toe": ["foot", "fk"],
        "hand": ["hand", "fk"],
        "finger": ["hand", "fk"],
        "tail": ["tail", "fk"],
        "head": ["head", "fk"],
        "neck": ["head", "fk"],
        "spine": ["spine", "fk", "ik", "rk"],
    }
    group_exclude = ["arm_clav", "leg_clav", "neck"]
    special_groups = ["finger", "toe"]
    side_exclude = ["spine", "tail", "head", "neck"]
    for side in ["L", "R"]:
        for key, values in ctrl_names.items():
            key = key.capitalize()
            if not cmds.objExists(f"{values[0].capitalize()}_Ctrl_Grp"):
                cmds.group(name=f"{values[0].capitalize()}_Ctrl_Grp", empty=True)
            if key.lower() in group_exclude:
                continue
            if key.lower() in special_groups:
                for i in range(1, 6):
                    if not cmds.objExists(f"{side}_{key}_0{i}_Ctrl_Grp"):
                        cmds.group(name=f"{side}_{key}_0{i}_Ctrl_Grp", empty=True)
                    if not cmds.objExists(f"{side}_{key}_Ctrl_Grp"):
                        cmds.group(name=f"{side}_{key}_Ctrl_Grp", empty=True)
                    if not cmds.objExists(f"{side}_{key}_{values[1].capitalize()}_Ctrl_Grp"):
                        cmds.group(name=f"{side}_{key}_{values[1].capitalize()}_Ctrl_Grp", empty=True)
                    safe_parent(f"{side}_{key}_0{i}_Ctrl_Grp",
                                f"{side}_{key}_{values[1].capitalize()}_Ctrl_Grp")
                    safe_parent(f"{side}_{key}_{values[1].capitalize()}_Ctrl_Grp", f"{values[0].capitalize()}_Ctrl_Grp")
            for value in values:
                if value == values[0]:
                    continue
                if key.lower() == value.lower():
                    continue
                value = value.upper() if value in ["fk", "ik", "rk"] else value.capitalize()
                if key.lower() in side_exclude:
                    if cmds.objExists(f"{key}_{value}_Ctrl_Grp") and cmds.objExists(f"{key}_Ctrl_Grp"):
                        continue
                    if not cmds.objExists(f"{key}_{value}_Ctrl_Grp"):
                        cmds.group(name=f"{key}_{value}_Ctrl_Grp", empty=True)
                    if not cmds.objExists(f"{key}_Ctrl_Grp"):
                        cmds.group(name=f"{key}_Ctrl_Grp", empty=True)
                    if value.lower() == "fk":
                        safe_parent(f"{key}_{value}_Ctrl_Grp", f"{key}_Ctrl_Grp")
                    elif value.lower() == "ik":
                        safe_parent(f"{key}_{value}_Ctrl_Grp", f"{key}_Ctrl_Grp")
                    elif value.lower() == "rk":
                        safe_parent(f"{key}_{value}_Ctrl_Grp", f"{key}_Ctrl_Grp")
                    else:
                        safe_parent(f"{key}_{value}_Ctrl_Grp", f"{key}_{value}_Ctrl_Grp")
                    safe_parent(f"{key}_Ctrl_Grp", f"{values[0].capitalize()}_Ctrl_Grp")
                else:
                    if cmds.objExists(f"{side}_{key}_{value}_Ctrl_Grp") and cmds.objExists(f"{side}_{key}_Ctrl_Grp"):
                        continue
                    if not cmds.objExists(f"{side}_{key}_{value}_Ctrl_Grp"):
                        cmds.group(name=f"{side}_{key}_{value}_Ctrl_Grp", empty=True)
                    if not cmds.objExists(f"{side}_{key}_Ctrl_Grp"):
                        cmds.group(name=f"{side}_{key}_Ctrl_Grp", empty=True)
                    if value.lower() == "fk":
                        safe_parent(f"{side}_{key}_{value}_Ctrl_Grp", f"{side}_{key}_Ctrl_Grp")
                    elif value.lower() == "ik":
                        safe_parent(f"{side}_{key}_{value}_Ctrl_Grp", f"{side}_{key}_Ctrl_Grp")
                    elif value.lower() == "rk":
                        safe_parent(f"{side}_{key}_{value}_Ctrl_Grp", f"{side}_{key}_Ctrl_Grp")
                    else:
                        safe_parent(f"{side}_{key}_{value}_Ctrl_Grp", f"{side}_{key}_{value}_Ctrl_Grp")
                    safe_parent(f"{side}_{key}_Ctrl_Grp", f"{values[0].capitalize()}_Ctrl_Grp")
    """

    # manager = RkManager()
    # manager.run()

    print("---------_____COMPLETE_____---------")
