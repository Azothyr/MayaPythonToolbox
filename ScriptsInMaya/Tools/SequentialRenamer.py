import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds


def sequential_renamer(txt, data):
    """
    Renames selected objects sequentially.
    Returns:
    """
    count = txt.count('#')
    scheme_parts = txt.partition(count * "#")
    objects_changed = 0

    for i in range(len(data)):
        new_name = scheme_parts[0] + str(i + 1).zfill(count) + scheme_parts[2]
        cmds.rename(data[i], new_name)
        objects_changed += 1

    print("Number of Objects renamed: " + str(objects_changed))