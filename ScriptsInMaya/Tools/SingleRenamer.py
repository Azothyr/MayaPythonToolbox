import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds


def single_renamer(new_name, obj):
    """
    Renames selected object
    """
    cmds.rename(obj, new_name)
