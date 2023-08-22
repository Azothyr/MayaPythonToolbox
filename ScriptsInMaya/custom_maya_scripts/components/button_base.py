import maya.cmds as cmds
from custom_maya_scripts.info.button_arg_map import button_arg_map as arg_map
from custom_maya_scripts.utilities import arg_map_utils as map_handler
from custom_maya_scripts.utilities import ui_presence_checker as ui_check


class ButtonBase:
	def __init__(self, name, command=None, **kwargs):
		self.widget = None
		self.name = name
		self.command = command
		self.arg_mapping = arg_map

		# Set attributes
		translated_kwargs = map_handler.translate_arg_map_keys(self.arg_mapping, kwargs)
		self.set_attributes(**translated_kwargs)
		self._create(**translated_kwargs)

	def set_attributes(self, **kwargs):
		map_handler.set_class_kwargs(self, self.arg_mapping, **kwargs)

	def helper(self, attr):
		print(map_handler.retrieve_metadata(attr, self.arg_mapping))

	def _create(self, **kwargs):
		self.widget = cmds.button(self.name, **kwargs)

	def edit(self, **kwargs):
		cmds.button(self.name, e=True, **kwargs)

	def query(self, attribute):
		return cmds.button(self.name, q=True, **{attribute: True})
