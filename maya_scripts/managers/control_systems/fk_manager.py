import maya.cmds as cmds
from maya_scripts.managers.constraint_management.constraint_removal import ConstraintRemoval


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


# No sort
class NoSort(SortMethod):
    def sort(self, unsorted_selection):
        return unsorted_selection


class BrokenFkConstraintFactory:
    @staticmethod
    def create_constraints(constraint_order):
        for keys, values in constraint_order.items():
            leader = values["leading_control"]
            follower_grp = values["follower_group"]
            follower = values["follower_control"]

            # Create constraints
            translate_constraint = cmds.parentConstraint(leader, follower_grp,
                                                         name=f'{leader}_Constraining_TRANSLATION_'
                                                              f'via_parent_constraint', mo=True,
                                                         skipRotate=["x", "y", "z"], weight=1)[0]

            rotate_constraint = cmds.parentConstraint(leader, follower_grp,
                                                      name=f'{leader}_Constraining_ROTATION_via_parent_constraint',
                                                      mo=True, skipTranslate=["x", "y", "z"], weight=1)[0]

            scale_constraint = cmds.scaleConstraint(leader, follower_grp,  # noqa
                                                    name=f'{leader}_Constraining_SCALE_via_parent_constraint',
                                                    weight=1)[0]

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


class BrokenFkManager:
    def __init__(self, _sort_method=NoSort()):
        self.sort_method = _sort_method
        self.unsorted_selection = cmds.ls(sl=True)
        self.constraint_order_manager = ConstraintOrder()

    def run(self):
        # Remove existing constraints before applying new ones
        for control_group in self.constraint_order_manager.constraint_order.keys():
            ConstraintRemoval.remove_from_control_leader(control_group)

        sorted_controls = self.sort_method.sort(self.unsorted_selection)

        # Exclude the last control group from having constraints set
        # sorted_controls = sorted_controls[:-1]

        control_groups = [ControlGroup(control) for control in sorted_controls]
        self.constraint_order_manager.recursively_set_relationship(control_groups)
        self.create_constraints()

    def create_constraints(self):
        BrokenFkConstraintFactory.create_constraints(self.constraint_order_manager.constraint_order)


if __name__ == "_main_":
    broken_fk = BrokenFkManager(outliner_sort())
    sort_method = NoSort()
    fk_manager = BrokenFkManager(NoSort())
    fk_manager.run()

    """def constraint_removal(selection=None):
        if selection is None:
            selection = cmds.ls(sl=True)

        def recursive_removal_from_hierarchy(_node):

            # List all the constraints attached to the node.
            constraints = cmds.listRelatives(_node, type='constraint')

            # If there are constraints, delete them.
            if constraints:
                for constraint in constraints:
                    cmds.delete(constraint)

            # Check children and continue the process recursively.
            children = cmds.listRelatives(_node, children=True, fullPath=True)
            if children:
                for child in children:
                    recursive_removal_from_hierarchy(child)

        for node in selection:
            recursive_removal_from_hierarchy(node)

    def broken_fk(hierarchical_sort=False, outliner_sort=False):
        unsorted_selection: list[object] = cmds.ls(sl=True)
        constraint_order = {}

        def __get_group_from_control(control: object):
            try:
                if cmds.objectType(control) == "transform":
                    group = cmds.listRelatives(control, parent=True, type="transform")[0]
                    if not str(control).lower().endswith("_ctrl"):
                        raise ValueError(f"ERROR --- group must end with _grp, not {group}".upper())
                    return group
                else:
                    raise ValueError(f"ERROR --- control must end with _ctrl, {control}".upper())
            except ValueError as e:
                raise ValueError(e)

        def __get_control_from_group(group: object):
            try:
                if cmds.objectType(group) == "transform":
                    control = cmds.listRelatives(group, children=True, type="transform")[0]
                    if not str(control).lower().endswith("_ctrl"):
                        raise ValueError(f"ERROR --- control must end with _ctrl, {control}".upper())
                    return control
                else:
                    raise ValueError(f"ERROR --- group must end with _grp, not {group}".upper())
            except ValueError as e:
                raise ValueError(e)

        def __recursively_set_relationship(data: list[object]):
            if len(data) < 2:  # if there is only one item left in the list, stop the recursion
                return
            elif data[0] in constraint_order.items():
                return  # if the _leader is already in the constraint order, stop the recursion
            else:
                # pulls the _leader from the list, so it can recursively set the next index as the _follower
                _leader: object = data.pop(0)  # grab and remove the first item in the list
                _follower = data[0]  # _follower is next in list due to the pop
                # find group and ctrl of _leader and _follower
                if str(_leader).lower().endswith("_grp"):
                    _leader_group = _leader
                    _leader = __get_control_from_group(_leader)
                else:
                    _leader_group = __get_group_from_control(_leader)
                if str(_follower).lower().endswith("_grp"):
                    _follower_group = _follower
                    _follower = __get_control_from_group(_follower)
                else:
                    _follower_group = __get_group_from_control(_follower)

                # create a dictionary with the _leader_group as the key and the _follower, _follower_group and
                # _leader_control as the values
                result = {
                    "leader's_group": _leader_group,
                    "leading_control": _leader,
                    "follower_group": _follower_group,
                    "follower_control": _follower
                }
                constraint_order[_leader_group] = result
                __recursively_set_relationship(data)

        # If hierarchy_sort is True, it will sort the selection based on maya outliner hierarchy. If False, it will not.
        if hierarchical_sort:
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

            __recursively_set_relationship(sorted_selection)

        # If outliner_sort is True, it will sort the selection based on maya outliner order. If False, it will not.
        elif outliner_sort:
            def sort_by_outliner_order(unsorted_objects):
                # Get a list of all objects in the Maya scene in their hierarchical and creation order
                all_objects = cmds.ls(dag=True, long=True)

                # Convert long names to short names
                short_all_objects = [x.split('|')[-1] for x in all_objects]

                # Get indices of the selected objects
                object_indices = {_obj: short_all_objects.index(_obj) for _obj in unsorted_objects}

                # Sort the selected objects based on these indices
                return sorted(unsorted_objects, key=lambda x: object_indices[x])

            sorted_selection = sort_by_outliner_order(unsorted_selection)
            __recursively_set_relationship(sorted_selection)

        # If neither hierarchical_sort nor outliner_sort are True, it will sort the selection based on the order of the
        # selection.
        else:
            __recursively_set_relationship(unsorted_selection)

        print("\n".join([f"LEADER --> {v}" for k, v in constraint_order.items()]))

        for keys, values in constraint_order.items():
            leader = values["leading_control"]
            follower_grp = values["follower_group"]
            follower = values["follower_control"]

            # create constraints
            translate_contraint = cmds.parentConstraint(leader, follower_grp, mo=True, skipRotate=["x", "y", "z"],
                                                        weight=1)[0]
            rotate_contraint = cmds.parentConstraint(leader, follower_grp, mo=True, skipTranslate=["x", "y", "z"],
                                                     weight=1)[0]
            scale_constraint = cmds.scaleConstraint(leader, follower_grp, weight=1)[0]  # noqa

            # create attributes on the child if not already there
            if not cmds.attributeQuery('FollowTranslate', node=follower, exists=True):
                cmds.addAttr(follower, ln='FollowTranslate', at='double', min=0, max=1, dv=1)
                cmds.setAttr('%s.FollowTranslate' % follower, e=True, keyable=True)

            if not cmds.attributeQuery('FollowRotate', node=follower, exists=True):
                cmds.addAttr(follower, ln='FollowRotate', at='double', min=0, max=1, dv=1)
                cmds.setAttr('%s.FollowRotate' % follower, e=True, keyable=True)

            # connect the child's attribute to the rotate constraint weight 0
            cmds.connectAttr('%s.FollowTranslate' % follower, '%s.w0' % translate_contraint, f=True)
            # connect the attribute to the translation constraint weight 0
            cmds.connectAttr('%s.FollowRotate' % follower, '%s.w0' % rotate_contraint, f=True)"""
