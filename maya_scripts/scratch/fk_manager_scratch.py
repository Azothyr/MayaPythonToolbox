import maya.cmds as cmds
from core.constrainer import Main as constraint_manager
from core.maya_managers.control_manager import ControlManager


class BrokenFkConstraintFactory:
    @staticmethod
    def get_corresponding_joint(control):
        if control is None:
            return None
        joint_name = control.replace("_Ctrl", "_Jnt")
        if cmds.objExists(joint_name):
            return joint_name
        return None

    @staticmethod
    def is_joint_ancestor_or_same_level(leader_ctrl, follower_ctrl):
        if leader_ctrl == "Transform_Ctrl" and follower_ctrl == "COG_Ctrl":
            return False  # Special case for Transform_Ctrl and COG_Ctrl

        if leader_ctrl == follower_ctrl:
            return True  # A control should not constrain itself

        leader_joint = BrokenFkConstraintFactory.get_corresponding_joint(leader_ctrl)
        follower_joint = BrokenFkConstraintFactory.get_corresponding_joint(follower_ctrl)

        # Check if follower_joint is an ancestor of leader_joint
        ancestor_joints = cmds.listRelatives(leader_joint, allParents=True, fullPath=True) or []
        if follower_joint in ancestor_joints:
            return True  # Follower is an ancestor of leader

        # Check if they are siblings (have the same parent)
        leader_parent = cmds.listRelatives(leader_joint, parent=True, type='joint') or [None]
        follower_parent = cmds.listRelatives(follower_joint, parent=True, type='joint') or [None]
        if leader_parent[0] == follower_parent[0]:
            return True  # They are siblings
        return False

    def create_constraints(self, constraint_order, joint_constraints=True, control_constraints=True):
        for values in constraint_order.values():
            leader = values["leading_control"]
            follower = values["follower_control"]
            follower_group = values["follower_group"]

            if self.is_joint_ancestor_or_same_level(leader, follower):
                continue

            if control_constraints:
                self.create_control_to_group_constraints(leader, follower_group, follower)

            if joint_constraints:
                joint = leader.replace("_Ctrl", "_Jnt")
                self.create_control_to_joint_constraints(leader, joint)

    @staticmethod
    def create_control_to_group_constraints(leader, follower_grp, follower):
        print(f"Creating control-to-group constraints for: {leader} -> {follower}")

        # Create constraints
        translate_constraint = cmds.parentConstraint(leader, follower_grp,
                                                     name=f'{leader}__TRANSLATION__parentConstraint', mo=True,
                                                     skipRotate=["x", "y", "z"], weight=1)[0]

        rotate_constraint = cmds.parentConstraint(leader, follower_grp,
                                                  name=f'{leader}__ROTATION__parentConstraint', mo=True,
                                                  skipTranslate=["x", "y", "z"], weight=1)[0]

        scale_constraint = cmds.scaleConstraint(leader, follower_grp,  # noqa
                                                name=f'{leader}__FULL__scaleConstraint', weight=1)[0]

        # Create attributes on the child if not already there
        if not cmds.attributeQuery('FollowTranslate', node=follower, exists=True):
            print(f"Creating FollowTranslate for {follower}")
            cmds.addAttr(follower, ln='FollowTranslate', at='double', min=0, max=1, dv=1)
            cmds.setAttr('%s.FollowTranslate' % follower, e=True, keyable=True)

        if not cmds.attributeQuery('FollowRotate', node=follower, exists=True):
            print(f"Creating FollowRotate for {follower}")
            cmds.addAttr(follower, ln='FollowRotate', at='double', min=0, max=1, dv=1)
            cmds.setAttr('%s.FollowRotate' % follower, e=True, keyable=True)

        # Connect the child's attribute to the rotate constraint weight 0
        cmds.connectAttr('%s.FollowTranslate' % follower, '%s.w0' % translate_constraint, f=True)
        # Connect the attribute to the translation constraint weight 0
        cmds.connectAttr('%s.FollowRotate' % follower, '%s.w0' % rotate_constraint, f=True)

    @staticmethod
    def create_control_to_joint_constraints(control, joint):
        if not cmds.objExists(joint):
            print(f"WARNING: {joint} does not exist.")
            return

        # Create constraints for the joint
        cmds.parentConstraint(control, joint,
                              name=f'{control}__FULL__parentConstraint', mo=True,
                              weight=1)
        cmds.scaleConstraint(control, joint,
                             name=f'{control}__FULL__scaleConstraint', weight=1)


class BrokenFkManager:
    def __init__(self, selection=None):
        self.unsorted_selection = selection or cmds.ls(sl=True)
        if not self.unsorted_selection:
            self.unsorted_selection = [x for x in cmds.ls(type="transform") if x.lower().endswith(("_grp", "_ctrl"))][:-1]

    @staticmethod
    def create_constraint_order(control_groups):
        constraint_order = {}
        control_map = {cg.control: cg for cg in control_groups}

        for control_group in control_groups:
            leader_control = control_group.control

            # Handle special case for Transform_Ctrl
            if leader_control == "Transform_Ctrl":
                continue  # Skip as it doesn't follow joint hierarchy

            leader_joint = BrokenFkConstraintFactory.get_corresponding_joint(leader_control)
            if not leader_joint:
                continue

            # Get parent joint of the leader_joint
            parent_joint = cmds.listRelatives(leader_joint, parent=True, type='joint')
            if parent_joint:
                parent_control = parent_joint[0].replace("_Jnt", "_Ctrl")
                if parent_control in control_map:
                    parent_group = control_map[parent_control].group
                    constraint_order[leader_control] = {
                        "leading_control": parent_control,
                        "follower_group": control_group.group,
                        "follower_control": leader_control
                    }

        if "Transform_Ctrl" in control_map and "COG_Ctrl" in control_map:
            cog_group = control_map["COG_Ctrl"].group  # Get the group name for COG_Ctrl
            constraint_order["COG_Ctrl"] = {
                "leading_control": "Transform_Ctrl",
                "follower_group": cog_group,
                "follower_control": "COG_Ctrl"
            }

        if "Transform_Ctrl" in control_map and "Transform_Ctrl" not in constraint_order:
            constraint_order["Transform_Ctrl"] = {
                "leading_control": None,  # No leading control for top level
                "follower_group": control_map["Transform_Ctrl"].group,
                "follower_control": "Transform_Ctrl"
            }

        print("Constraint Order:", constraint_order)
        return constraint_order

    @staticmethod
    def create_constraints(constraint_order, control_map, joint_constraints=True, control_constraints=True):
        for values in constraint_order.values():
            leader = values["leading_control"]
            follower = values["follower_control"]
            follower_group = values["follower_group"]

            if BrokenFkConstraintFactory.is_joint_ancestor_or_same_level(leader, follower):
                continue

            if control_constraints:
                BrokenFkConstraintFactory.create_control_to_group_constraints(leader, follower_group, follower)

        for control in control_map.keys():
            if joint_constraints and control != "Transform_Ctrl":
                joint = BrokenFkConstraintFactory.get_corresponding_joint(control)
                if joint:
                    BrokenFkConstraintFactory.create_control_to_joint_constraints(control, joint)

    def run(self, clean=False, controls=True, joints=True):
        if clean:
            constraint_manager(mode="r")
        sorted_controls = [ControlManager(control) for control in self.unsorted_selection]
        constraint_order = self.create_constraint_order(sorted_controls)
        control_map = {cg.control: cg for cg in sorted_controls}
        self.create_constraints(constraint_order, control_map, control_constraints=controls, joint_constraints=joints)


if __name__ == "__main__":
    def module_name():
        import inspect
        import os
        # Get the current frame and find the file name of the script
        frame = inspect.currentframe()
        filename = inspect.getfile(frame)
        return os.path.basename(filename).split('.')[0]
    print(f"{'-' * 10 + '|' + ' ' * 4} RUNNING {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 10}")
    cmds.select(clear=True)
    broken_fk = BrokenFkManager()
    broken_fk.run(clean=False, controls=True, joints=True)

    print(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 25}")
