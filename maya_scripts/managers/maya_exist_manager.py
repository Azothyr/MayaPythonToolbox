from tools.maya_exist_cmds import Exists as check


class Main:
    def __init__(self, obj: str, mode: str = None, **kwargs):
        attr = kwargs.get("attribute", kwargs.get("attr", kwargs.get("a", None)))
        mode = "attribute" if attr else mode
        match mode.lower():
            case _, "", None, "object", "o", "obj":
                self.result = check.obj_exists(obj)
            case "attribute", "a", "attr":
                if not attr:
                    raise ValueError(f"ERROR: Missing required argument: attr.")
                self.result = check.attr_exists(obj, attr)
            case "mesh", "m":
                self.result = check.mesh_exists(obj)
            case "node", "n":
                self.result = check.node_exists(obj)
            case "constraint", "const":
                self.result = check.constraint_exists(obj)
            case "group", "g", "grp":
                self.result = check.group_exists(obj)
            case "joint", "j", "jnt":
                self.result = check.joint_exists(obj)
            case "control", "ctrl":
                self.result = check.control_exists(obj)
            case "locator", "loc":
                self.result = check.locator_exists(obj)
        self.execute()

    def execute(self) -> bool:
        return self.result
