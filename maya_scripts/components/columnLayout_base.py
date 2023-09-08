import maya.cmds as cmds
from maya_scripts.info.columnLayout_arg_map import columnLayout_arg_map as _map_src
from maya_scripts.components.maya_cmds_base import CmdsBase


class ColumnLayoutBase(CmdsBase):
	def __init__(self, name, **kwargs):
		super().__init__(name, **kwargs)

	def _get_arg_map(self):
		return _map_src
