from core.components.validate_cmds.maya_exist_cmds import Exists as check


class Main:
    def __init__(self, obj: str, mode: str = None, **kwargs):
        attr = kwargs.get("attribute", kwargs.get("attr", kwargs.get("a", None)))
        mode = "attribute" if attr else mode
        match mode.lower():
            case _, "", None, "object", "o", "obj":
                self.result = check.obj(obj)
            case "attribute", "a", "attr":
                if not attr:
                    raise ValueError(f"ERROR: Missing required argument: attr.")
                self.result = check.attr(obj, attr)
            case "mesh", "m":
                self.result = check.mesh(obj)
            case "node", "n":
                self.result = check.node(obj)
            case "constraint", "const":
                self.result = check.constraint(obj)
            case "group", "g", "grp":
                self.result = check.group(obj)
            case "joint", "j", "jnt":
                self.result = check.joint(obj)
            case "control", "ctrl":
                self.result = check.control(obj)
            case "locator", "loc":
                self.result = check.locator(obj)
        self.execute()

    def execute(self) -> bool:
        return self.result
