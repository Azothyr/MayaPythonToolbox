import maya.cmds as cmds
import textwrap
from custom_maya_scripts.info.button_arg_map import button_arg_map as arg_map


class ButtonBase:
	def __init__(self, label, **kwargs):
		self.widget = None
		self.label = label
		self.arg_mapping = arg_map

		# Translate kwargs keys if they are in arg_mapping
		for key in list(kwargs.keys()):
			if key in self.arg_mapping:
				name = self.arg_mapping[key]['name']
				kwargs[name] = kwargs.pop(key)

		# Set attributes
		self.set_attributes(**kwargs)
		self.create(**kwargs)

	def set_attributes(self, **kwargs):
		for key, value in self.arg_mapping.items():
			setattr(self, value['name'], kwargs.get(value['name']))
			setattr(self, f"{value['name']}_description", value.get('description'))
			setattr(self, f"{value['name']}_property", value.get('property'))
			setattr(self, f"{value['name']}_type", value.get('type'))

	def helper(self, attr):
		formatted_meta = []
		if str(attr).lower() == "all":
			for k, v in self.arg_mapping.items():
				formatted_meta.append(f"Name: {k} -> {v['name']} | Arg: {v['type']} | Use case: {v['property']}\n\tDescription: {textwrap.fill(v['description'], width=80)}\n")
			return '\n'.join(formatted_meta)
		elif str(attr).lower() == "args":
			for k, v in self.arg_mapping.items():
				formatted_meta.append(f"Name: {k} -> {v['name']}")

			return '\n'.join(formatted_meta)
		elif attr in self.arg_mapping:
			sn = attr
			ln = self.arg_mapping[attr]['name']
			desc = self.arg_mapping[attr]['description']
			typ = self.arg_mapping[attr]['type']
			prop = self.arg_mapping[attr]['property']
			return f"Name: {sn} -> {ln} | Arg: {typ} | Use case: {prop}\n\tDescription: {textwrap.fill(desc, width=80)}\n"
		else:
			for k, v in self.arg_mapping.items():
				if attr == v['name']:
					sn = k
					ln = attr
					desc = v['description']
					typ = v['type']
					prop = v['property']
					return f"Name: {sn} -> {ln} | Arg: {typ} | Use case: {prop}\n\tDescription: {textwrap.fill(desc, width=80)}\n"
		return f"Key {attr} was not found in Arg Map."

	def create(self, **kwargs):
		self.widget = cmds.button(label=self.label, **kwargs)

	def edit(self, **kwargs):
		cmds.button(self.widget, e=True, **kwargs)

	def query(self, attribute):
		return cmds.button(self.widget, q=True, **{attribute: True})
