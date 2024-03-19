def confirm(name, suffix="_Ctrl"):
    if isinstance(name, str):
        if name.lower().endswith(suffix.lower()):
            return True
    else:
        raise ValueError(f"Expected name to be a string, got {type(name)} instead.")
    return False


def check_and_fix(name, suffix="_Ctrl"):
    if not confirm(name, suffix):
        return name + suffix
    return name
