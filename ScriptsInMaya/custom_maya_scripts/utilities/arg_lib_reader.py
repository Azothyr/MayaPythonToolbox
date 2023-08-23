from custom_maya_scripts.info import arg_lib as lib
from custom_maya_scripts.utilities import arg_map_utils as map_handler


def _get_lib():
    for value in lib:
        print(value)


_get_lib()


class LibReader:
    def __init__(self, **kwargs):
        self.arg_mapping = None

        # Set attributes
        translated_kwargs = map_handler.translate_arg_map_keys(self.arg_mapping, kwargs)
