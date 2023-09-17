from maya_scripts.config.rowColumnLayout_arg_map import rowColumnLayout_arg_map as _map_src
from maya_scripts.components.maya_cmds_base import CmdsBase


class RowColumnLayoutBase(CmdsBase):
	def __init__(self, name, **kwargs):
		super().__init__(name, **kwargs)

	def _get_arg_map(self):
		return _map_src
