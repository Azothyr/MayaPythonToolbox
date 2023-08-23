import maya.cmds as cmds
from custom_maya_scripts.info.window_arg_map import window_arg_map as arg_map
from custom_maya_scripts.utilities import arg_map_utils as map_handler
from custom_maya_scripts.utilities import ui_presence_checker as ui_check


class WindowBase:
	def __init__(self, name, **kwargs):
		self.widget = None
		self.name = name
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
		ui_check.initialization_check(self.name)
		self.widget = cmds.window(self.name, **kwargs)

	def edit(self, **kwargs):
		cmds.window(self.name, e=True, **kwargs)

	def query(self, attribute):
		return cmds.window(self.name, q=True, **{attribute: True})

	def initialize(self, use_name=False):
		if use_name:
			cmds.showWindow(self.name)
		else:
			cmds.showWindow(self.widget)
