from custom_maya_scripts.info.arg_lib import arg_lib
from custom_maya_scripts.utilities import arg_map_utils as map_handler


class LibReader:
    def __init__(self, **kwargs):
        self.__library = arg_lib
        if not kwargs:
            to_return = ',\n'.join([key for key, value in arg_lib.items()])
            raise TypeError(
                f"\nYou must provide arguments to the reader as 'arg=True' or 'arg=False'\nARG OPTIONS:\n{to_return}")

        self._retrieve_arg_library_metadata(**kwargs)

    def _retrieve_arg_library_metadata(self, **kwargs):
        for key, value in kwargs.items():
            if value:
                if key == 'all':
                    for arg_map in self.__library.keys():
                        if arg_map != 'all':
                            self._retrieve_arg_library_metadata(**{arg_map: True})
                    break
                if key in self.__library:
                    meta = map_handler.retrieve_metadata("all", self.__library[key])
                    meta_title = f'---{key.upper()}---'
                    split = "-" * len(meta_title)
                    print(f"\n{split}\n{meta_title}\n{split}\n{split}\n", meta)
                else:
                    print(f"ERROR: ---{key.upper()}--- not found in the library.")
