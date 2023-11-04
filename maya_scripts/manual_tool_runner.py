import sys

# if 'C:\\Users\\Demon\\Documents\\custom_scripts' in sys.path:
#     sys.path.remove('C:\\Users\\Demon\\Documents\\custom_scripts')
if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' not in sys.path:
    sys.path.append('C:/GitRepos/MayaPythonToolbox/maya_scripts')
# print("\n".join([path for path in sys.path]), "\n")
import maya.cmds as cmds
from managers.constraint_management.constraint_removal import ConstraintRemoval
from managers.base_maya_objects.joint_manager import JointManager


class ControlGroup:
    def __init__(self, control_objects):
        self.group, self.control = self._split_to_control_and_group(control_objects)

    @staticmethod
    def _split_to_control_and_group(_object) -> tuple:
        try:
            if cmds.objectType(_object) == "transform":
                if _object.lower().endswith("_ctrl"):
                    ctrl = _object
                    grp = cmds.listRelatives(_object, parent=True, type="transform")[0]
                elif _object.lower().endswith("_grp"):
                    grp = _object
                    ctrl = cmds.listRelatives(_object, children=True, type="transform")[0]
                else:
                    raise ValueError(f"ERROR --- Controls must end with _Ctrl and Groups must end with _Grp. {_object} "
                                     f"Does not follow this.".upper())
                return grp, ctrl
            else:
                raise ValueError(f"ERROR --- Incorrect _object selected {_object} of type "
                                 f"{cmds.objectType(_object)}".upper())
        except ValueError as e:
            raise e


class ConstraintOrder:
    def __init__(self):
        self.constraint_order = {}

    def recursively_set_relationship(self, control_groups):
        if len(control_groups) < 2:
            return
        else:
            leader = control_groups.pop(0)
            follower = control_groups[0]
            result = {
                "leader's_group": leader.group,
                "leading_control": leader.control,
                "follower_group": follower.group,
                "follower_control": follower.control
            }
            self.constraint_order[leader.group] = result
            self.recursively_set_relationship(control_groups)


# Base class for sorting
class SortMethod:
    def sort(self, unsorted_selection):
        raise NotImplementedError("This method should be overridden by subclass")


# Hierarchical sort
class HierarchicalSort(SortMethod):
    def sort(self, unsorted_selection):
        sorted_selection = []

        def find_and_insert(child, unsorted, sorted_list):
            parent = cmds.listRelatives(child, parent=True)
            if parent:
                parent = parent[0]
                if parent in unsorted:
                    find_and_insert(parent, unsorted, sorted_list)
            if child not in sorted_list:
                sorted_list.append(child)

        for obj in unsorted_selection:
            find_and_insert(obj, unsorted_selection, sorted_selection)

        return sorted_selection


# Outliner sort
class OutlinerSort(SortMethod):
    def sort(self, unsorted_selection):
        all_objects = cmds.ls(dag=True, long=True)
        short_all_objects = [x.split('|')[-1] for x in all_objects]
        object_indices = {obj: short_all_objects.index(obj) for obj in unsorted_selection}
        return sorted(unsorted_selection, key=lambda x: object_indices[x])

class SortByJointOutliner(SortMethod):
    def sort(self, unsorted_selection):
        fk_joints = []
        fk_joints.extend(JointManager(get="cog").data["COG"]["joints"])
        fk_joints.extend(JointManager(get="fk").data["FK"]["joints"])
        selection = fk_joints
        print(f"Selection: {selection}")
        exit()

        all_objects = cmds.ls(dag=True, long=True)
        short_all_objects = [x.split('|')[-1] for x in all_objects]
        object_indices = {obj: short_all_objects.index(obj) for obj in unsorted_selection}
        return sorted(unsorted_selection, key=lambda x: object_indices[x])


# No sort
class BasicSort(SortMethod):
    def sort(self, unsorted_selection):
        return unsorted_selection


class BrokenFkConstraintFactory:
    def create_constraints(self, constraint_order, **kwargs):
        if not constraint_order:
            raise ValueError(f"WARNING: constraint_order is empty.")

        joint_constraints = kwargs.get("joint", True)
        control_constraints = kwargs.get("control", True)

        for keys, values in constraint_order.items():
            if not joint_constraints and not control_constraints:
                print(f"WARNING: constraints were not allowed to be created.")
                return
            else:
                _leader = values["leading_control"]
            if control_constraints:
                _follower_grp = values["follower_group"]
                _follower = values["follower_control"]
                self.create_control_to_group_constraints(_leader, _follower_grp, _follower)
            if joint_constraints:
                _joint = _leader.replace("_Ctrl", "_Jnt")
                self.create_control_to_joint_constraints(_leader, _joint)

    @staticmethod
    def create_control_to_group_constraints(leader, follower_grp, follower):

        # Create constraints
        translate_constraint = cmds.parentConstraint(leader, follower_grp,
                                                     name=f'{leader}__TRANSLATION_'
                                                          f'_parentConstraint', mo=True,
                                                     skipRotate=["x", "y", "z"], weight=1)[0]

        rotate_constraint = cmds.parentConstraint(leader, follower_grp,
                                                  name=f'{leader}__ROTATION'
                                                       f'__parentConstraint', mo=True,
                                                  skipTranslate=["x", "y", "z"], weight=1)[0]

        scale_constraint = cmds.scaleConstraint(leader, follower_grp,  # noqa
                                                name=f'{leader}__SCALE'
                                                     f'__parentConstraint', weight=1)[0]

        # Create attributes on the child if not already there
        if not cmds.attributeQuery('FollowTranslate', node=follower, exists=True):
            cmds.addAttr(follower, ln='FollowTranslate', at='double', min=0, max=1, dv=1)
            cmds.setAttr('%s.FollowTranslate' % follower, e=True, keyable=True)

        if not cmds.attributeQuery('FollowRotate', node=follower, exists=True):
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
                              name=f'{control}__TRANSLATE_ROTATION__parentConstraint', mo=True,
                              weight=1)
        cmds.scaleConstraint(control, joint,
                             name=f'{control}__SCALE_parentConstraint', weight=1)


class BrokenFkManager:
    def __init__(self, _sort_method: SortMethod = OutlinerSort(), **kwargs):
        selection = cmds.ls(sl=True)
        self.unsorted_selection = selection
        if not selection:
            selection = [x for x in cmds.ls(type="transform") if x.lower().endswith("_grp") or
                         x.lower().endswith("_ctrl")]
            # Exclude the last control group from having constraints set
            self.unsorted_selection = selection[:-1]

        self.sort_method = _sort_method
        self.constraint_order_manager = ConstraintOrder()

    def run(self, **kwargs):
        # Remove existing constraints before applying new ones
        for control_group in self.constraint_order_manager.constraint_order.keys():
            ConstraintRemoval.remove_from_control_leader(control_group)
        print(self.unsorted_selection)
        sorted_controls = self.sort_method.sort(self.unsorted_selection)

        control_groups = [ControlGroup(control) for control in sorted_controls]
        self.constraint_order_manager.recursively_set_relationship(control_groups)
        self.create_constraints(do_control=kwargs.get("controls", True), do_joint=kwargs.get("joints", True))

    def create_constraints(self, do_control=True, do_joint=True):
        BrokenFkConstraintFactory().create_constraints(self.constraint_order_manager.constraint_order,
                                                       control=do_control, joint=do_joint)


if __name__ == "__main__":
    print(f"{'-' * 10 + '|' + ' ' * 4} Running Broken FK Constraint Manager {' ' * 4 + '|' + '-' * 10}")
    # ConstraintRemoval().remove_all_constraints()
    cmds.select(clear=True)
    sort_method = SortByJointOutliner()
    brokenfk = BrokenFkManager(sort_method)
    brokenfk.run(controls=True, joints=True)
    print(f"{'-' * 25 + '|' + ' ' * 4} Complete {' ' * 4 + '|' + '-' * 25}")

