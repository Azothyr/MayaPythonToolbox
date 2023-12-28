import maya.cmds as cmds
from tools.constraint_cmds import Remove as rem
from tools.constraint_cmds import Create as cr


class Main:
    def __init__(self, mode: str = None, **kwargs):
        match mode.lower():
            case "remove", "r", "rem":
                self.remove_constraints(**kwargs)
            case "create", "c", "cr":
                self.create_constraints(**kwargs)
            case _:
                raise ValueError(f"ERROR: Invalid mode: {mode}. Expected 'remove' ('r', 'rem') or"
                                 f" 'create' ('c', 'cr').")

    @staticmethod
    def create_attributes(**kwargs):
        """
        :param Required kwargs:
        :return:
            NA
        """

    @staticmethod
    def remove_attributes(**kwargs):
        """
        :param Required kwargs:
            object, o: str
        :return:
            NA
        """
