from config.arg_lib_info.button_arg_map import button_arg_map as _map_src
from ui.components.ui_cmds.maya_cmds_base import CmdsBase


class ButtonBase(CmdsBase):
	def __init__(self, name, command=None, **kwargs):
		super().__init__(name, **kwargs)
		self._command = command

	def _get_arg_map(self):
		return _map_src
