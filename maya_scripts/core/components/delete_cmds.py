import maya.cmds as cmds


class Delete:
    def __init__(self, obj: str = None, mode: str = None):
        if object:
            match mode.lower():
                case "object", "o", "obj":
                    self.delete_object(obj)
                case "attribute", "a", "attr":
                    self.delete_attribute(obj)
                case _:
                    raise ValueError(f"ERROR: Invalid mode: {mode}. Expected 'object' ('o'), 'constraint' ('c'),"
                                     f" or 'attribute' ('a').")

    @staticmethod
    def delete_object(obj: str):
        cmds.delete(obj)

    @staticmethod
    def delete_attribute(obj: str):
        cmds.deleteAttr(obj)
