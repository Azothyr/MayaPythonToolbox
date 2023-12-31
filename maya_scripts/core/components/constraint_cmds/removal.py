import maya.cmds as cmds
from core.components.attribute_cmds import Remove as attr_rem


class RemoveBase:
    pass


class RemoveAdvanced(RemoveBase):
    pass


class Remove(RemoveAdvanced):
    def remove_from_all_ctrls(self):
        controls = [x for x in cmds.ls(type="transform") if x.lower().endswith("_ctrl")]
        for ctrl in controls:
            attr_rem().remove_attrs(ctrl)
            self.remove_from_hierarchy([ctrl])

    @staticmethod
    def remove_from_hierarchy(selection=None):
        if selection is None:
            selection = cmds.ls(sl=True) if cmds.ls(sl=True) else \
                [x for x in cmds.ls(type="transform") if x.lower().endswith("_ctrl")]
        for node in selection:
            Remove.__recursive_removal_from_hierarchy(node)

    @staticmethod
    def __recursive_removal_from_hierarchy(_node):
        constraints = cmds.listRelatives(_node, type='constraint')
        if constraints:
            for constraint in constraints:
                cmds.delete(constraint)

        children = cmds.listRelatives(_node, children=True, fullPath=True)
        if children:
            for child in children:
                Remove.__recursive_removal_from_hierarchy(child)

    @staticmethod
    def remove_constraints_from_object(object_name, attrs=None):
        # Clean attributes from the object
        attr_rem.remove_attrs(object_name, attrs)

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
