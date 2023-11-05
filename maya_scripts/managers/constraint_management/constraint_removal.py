import maya.cmds as cmds
# from utilities.factory.meta_classes.plugin_registry_factory.plugin_meta_factory import PluginRegistryMeta


# class ConstraintRemoval(metaclass=PluginRegistryMeta):
class ConstraintRemoval:
    @staticmethod
    def remove_attrs(ctrl):
        if cmds.attributeQuery('FollowTranslate', node=ctrl, exists=True):
            cmds.deleteAttr(ctrl + '.FollowTranslate')

        if cmds.attributeQuery('FollowRotate', node=ctrl, exists=True):
            cmds.deleteAttr(ctrl + '.FollowRotate')

    @staticmethod
    def remove_from_all_ctrls():
        controls = [x for x in cmds.ls(type="transform") if x.lower().endswith("_ctrl")]
        for ctrl in controls:
            ConstraintRemoval.remove_attrs(ctrl)
            ConstraintRemoval.remove_from_hierarchy([ctrl])

    @staticmethod
    def remove_from_hierarchy(selection=None):
        if selection is None:
            selection = cmds.ls(sl=True) if cmds.ls(sl=True) else\
                [x for x in cmds.ls(type="transform") if x.lower().endswith("_ctrl")]
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
    def remove_all_constraints():
        for constraint in cmds.ls(type='constraint'):
            cmds.delete(constraint)
        ConstraintRemoval.remove_from_all_ctrls()
