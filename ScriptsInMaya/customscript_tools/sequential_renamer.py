import maya.cmds as cmds


def sequential_renamer(txt, lyst):
    """
    Renames selected objects sequentially.
    Returns:
    """
    count = txt.count('#')
    scheme_parts = txt.partition(count * "#")
    objects_changed = 0

    for i in range(len(lyst)):
        new_name = scheme_parts[0] + str(i + 1).zfill(count) + scheme_parts[2]
        cmds.rename(lyst[i], new_name)
        objects_changed += 1

    print("Number of Objects renamed: " + str(objects_changed))
