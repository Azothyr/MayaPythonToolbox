import maya.cmds as cmds
from custom_maya_scripts.components.maya_cmds_base import CmdsBase
from custom_maya_scripts.info.window_arg_map import window_arg_map as _map_src
from custom_maya_scripts.utilities import arg_map_utils as map_handler
from custom_maya_scripts.utilities import ui_presence_checker as ui_check


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
