import maya.cmds as cmds
from custom_maya_scripts.utilities import arg_map_utils as map_handler
from abc import ABC, abstractmethod


class CmdsBase(ABC):
    def __init__(self, name, **kwargs):
        self._name = name
        self._cmd_name = self._get_maya_cmd()
        self._arg_map = self._get_arg_map()
        self._widget = None
        self._repr_kwargs = map_handler.translate_for_kwargs(self._arg_map, kwargs)
        self._translated_kwargs = map_handler.translate_for_arg_map(self._arg_map, kwargs)

        self.__set_attributes(**self._translated_kwargs)
        self.__create(**self._translated_kwargs)

    def __str__(self):
        return self._name

    def __repr__(self):
        input_values_map = "\n".join(f"{sn} | {ln}:\n\t{val}" for sn, ln, val in self._repr_kwargs)
        splitter = '-' * 50
        return f"\t{self._name}   ->   {self.__class__.__name__}\n{splitter}\nPROPERTIES:\n{input_values_map}\n{splitter}"

    @abstractmethod
    def _get_arg_map(self):
        pass
    
    def _get_maya_cmd(self):
        return self.__class__.__name__[0].lower() + self.__class__.__name__[1:-4]

    def helper(self, attr):
        print(map_handler.retrieve_metadata(attr, self._arg_map))

    def __set_attributes(self, **kwargs):
        map_handler.set_class_kwargs(self, self._arg_map, **kwargs)

    def __create(self, **kwargs):
        method_name = self._cmd_name
        if hasattr(cmds, method_name):
            method = getattr(cmds, method_name)
            self._widget = method(self._name, **kwargs)
        else:
            raise ValueError(f"cmds does not have a method named {method_name}")

    def edit(self, **kwargs):
        method_name = self._cmd_name
        if hasattr(cmds, method_name):
            method = getattr(cmds, method_name)
            method(self._name, e=True, **kwargs)
        else:
            raise ValueError(f"cmds does not have a method named {method_name}")

    def query(self, attribute):
        method_name = self._cmd_name
        if hasattr(cmds, method_name):
            method = getattr(cmds, method_name)
            return method(self._name, q=True, **{attribute: True})
        else:
            raise ValueError(f"cmds does not have a method named {method_name}")
