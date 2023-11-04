import maya.cmds as cmds
# from utilities.factory.meta_classes.plugin_registry_factory.plugin_meta_factory import PluginRegistryMeta


# class ConstraintRemoval(metaclass=PluginRegistryMeta):
class ConstraintRemoval:
    @staticmethod
    def remove_from_hierarchy(selection=None):
        if selection is None:
            selection = cmds.ls(sl=True)
        for node in selection:
            ConstraintRemoval._recursive_removal_from_hierarchy(node)

    @staticmethod
    def _recursive_removal_from_hierarchy(_node):
        constraints = cmds.listRelatives(_node, type='constraint')
        if constraints:
            for constraint in constraints:
                cmds.delete(constraint)

        children = cmds.listRelatives(_node, children=True, fullPath=True)
        if children:
            for child in children:
                ConstraintRemoval._recursive_removal_from_hierarchy(child)

    @staticmethod
    def remove_from_control_leader(control_leader_group):
        constraints = cmds.listRelatives(control_leader_group, type='constraint')
        if constraints:
            for constraint in constraints:
                cmds.delete(constraint)

    @staticmethod
    def remove_all_constraints():
        for constraint in cmds.ls(type='constraint'):
            cmds.delete(constraint)
