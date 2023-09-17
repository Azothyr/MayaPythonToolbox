import maya.cmds as cmds
from maya_scripts.components.maya_cmds_base import CmdsBase
from maya_scripts.config.window_arg_map import window_arg_map as _map_src


class WindowBase(CmdsBase):
	def __init__(self, name, **kwargs):
		super().__init__(name, **kwargs)

	def _get_arg_map(self):
		return _map_src

	def initialize(self, use_name=False):
		if use_name:
			cmds.showWindow(self._name)
		else:
			cmds.showWindow(self._widget)
