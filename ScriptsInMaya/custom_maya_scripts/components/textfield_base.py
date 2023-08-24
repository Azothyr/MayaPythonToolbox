import maya.cmds as cmds
from custom_maya_scripts.info.textField_arg_map import textField_arg_map as _map_src
from custom_maya_scripts.components.maya_cmds_base import CmdsBase


class TextFieldBase(CmdsBase):
	def __init__(self, name, **kwargs):
		super().__init__(name, **kwargs)

	def _get_arg_map(self):
		return _map_src
