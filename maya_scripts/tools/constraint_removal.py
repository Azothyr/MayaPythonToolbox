import maya.cmds as cmds
# from utilities.factory.meta_classes.plugin_registry_factory.plugin_meta_factory import PluginRegistryMeta


# class ConstraintRemoval(metaclass=PluginRegistryMeta):
class Removal:
    @staticmethod
    def remove_attrs(obj, attrs: list = None):
        clean_attrs = ['FollowTranslate', 'FollowRotate'] if attrs is None else attrs
        for attr in clean_attrs:
            if cmds.attributeQuery(attr, node=obj, exists=True):
                cmds.deleteAttr(obj + '.' + attr)

    @staticmethod
    def remove_from_all_ctrls():
        controls = [x for x in cmds.ls(type="transform") if x.lower().endswith("_ctrl")]
        for ctrl in controls:
            Removal.remove_attrs(ctrl)
            Removal.remove_from_hierarchy([ctrl])

    @staticmethod
    def remove_from_hierarchy(selection=None):
        if selection is None:
            selection = cmds.ls(sl=True) if cmds.ls(sl=True) else\
                [x for x in cmds.ls(type="transform") if x.lower().endswith("_ctrl")]
        for node in selection:
            Removal._recursive_removal_from_hierarchy(node)

    @staticmethod
    def _recursive_removal_from_hierarchy(_node):
        constraints = cmds.listRelatives(_node, type='constraint')
        if constraints:
            for constraint in constraints:
                cmds.delete(constraint)

        children = cmds.listRelatives(_node, children=True, fullPath=True)
        if children:
            for child in children:
                Removal._recursive_removal_from_hierarchy(child)

    @staticmethod
    def remove_all_constraints():
        for constraint in cmds.ls(type='constraint'):
            cmds.delete(constraint)
        Removal.remove_from_all_ctrls()

    @staticmethod
    def remove_constraints_from_object(object_name, attrs=None):
        # Clean attributes from the object
        Removal.remove_attrs(object_name, attrs)

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
