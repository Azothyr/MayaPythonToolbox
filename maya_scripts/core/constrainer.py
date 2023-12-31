from core.components.constraint_cmds.removal import Remove as rem
from core.components.constraint_cmds.creation import Create as cr


class Main:
    def __init__(self, mode: str = None, create_method: str = None, **kwargs):
        create_method = create_method if create_method else "cm" if kwargs.get("cm") else ""
        match mode.lower():
            case opt if opt in ["remove", "r", "rem"]:
                self.remove_constraints(**kwargs)
            case opt if opt in ["create", "c", "cr"]:
                match create_method.lower():
                    case "cm":
                        self.create_constraints(**kwargs)
                    case "", _:
                        self.create_constraints(**kwargs)
            case _:
                raise ValueError(f"ERROR: Invalid mode: {mode}. Expected 'remove' ('r', 'rem') or"
                                 f" 'create' ('c', 'cr').")

    @staticmethod
    def create_constraints(**kwargs):
        """
        :param Required kwargs:
            name, n: str
            leader, l: str
            follower, f: str
            type, t: str
        :return:
            NA
        """
        name = kwargs.get("name", kwargs.get("n", None))
        leader = kwargs.get("leader", kwargs.get("l", None))
        follower = kwargs.get("follower", kwargs.get("f", None))
        type = kwargs.get("type", kwargs.get("t", None))
        if not all([name, leader, follower, type]):
            raise ValueError(f"ERROR: Missing required arguments: name, leader, follower, type.")
        cr(name, leader, follower, type).create_constraint()  # noqa

    @staticmethod
    def remove_constraints(**kwargs):
        """
        :param Required kwargs:
            object, o: str
        :return:
            NA
        """
        obj = kwargs.get("object", kwargs.get("o", None))
        if not obj:
            raise ValueError(f"ERROR: Missing required argument: object.")
        rem.remove_constraints_from_object(obj)
