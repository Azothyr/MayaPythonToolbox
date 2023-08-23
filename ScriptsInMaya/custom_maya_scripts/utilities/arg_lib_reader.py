from custom_maya_scripts.info.arg_lib import arg_lib as lib
from custom_maya_scripts.utilities import arg_map_utils as map_handler


class LibReader:
    def __init__(self, **kwargs):
        self.__library = lib

        self._retrieve_arg_library_metadata(**kwargs)

    def _retrieve_arg_library_metadata(self, **kwargs):
        for key in kwargs:
            if key == 'all':
                for item in self.__library:
                    meta = map_handler.retrieve_metadata("all", self.__library[key])
                    print(f"\n---{item[0].upper()}---\n", meta)
                break
            if key in self.__library:
                meta = map_handler.retrieve_metadata("all", self.__library[key])
                print(f"\n---{key.upper()}---\n", meta)
            else:
                print(f"-{key.upper()}- not found in the library.")


LibReader(all=True)
