import maya.cmds as cmds
from custom_maya_scripts.info.rowColumnLayout_arg_map import rowColumnLayout_arg_map as arg_map
from custom_maya_scripts.utilities import arg_map_utils as map_handler


class RowColumnLayoutBase:
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
		self.widget = cmds.rowColumnLayout(self.name, **kwargs)

	def edit(self, **kwargs):
		cmds.rowColumnLayout(self.name, e=True, **kwargs)

	def query(self, attribute):
		return cmds.rowColumnLayout(self.name, q=True, **{attribute: True})