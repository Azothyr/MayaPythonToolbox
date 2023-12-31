from config.arg_lib_info.textField_arg_map import textField_arg_map as _map_src
from ui.components.maya_cmds_base import CmdsBase


class TextFieldBase(CmdsBase):
	def __init__(self, name, **kwargs):
		super().__init__(name, **kwargs)

	def _get_arg_map(self):
		return _map_src