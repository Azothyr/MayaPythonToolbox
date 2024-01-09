def confirm(name, suffix="_Ctrl"):
    if name.endswith(suffix):
        return True
    return False


def check_and_fix(name, suffix="_Ctrl"):
    if not confirm(name, suffix):
        return name + suffix
    return name
