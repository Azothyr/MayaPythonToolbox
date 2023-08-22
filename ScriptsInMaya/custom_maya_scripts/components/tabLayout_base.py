import maya.cmds as cmds
from custom_maya_scripts.info.tabLayout_arg_map import tabLayout_arg_map as arg_map
from custom_maya_scripts.utilities import arg_map_utils as map_handler


class TabLayoutBase:
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
		self.widget = cmds.tabLayout(self.name, **kwargs)

	def edit(self, **kwargs):
		cmds.tabLayout(self.name, e=True, **kwargs)

	def query(self, attribute):
		return cmds.tabLayout(self.name, q=True, **{attribute: True})
