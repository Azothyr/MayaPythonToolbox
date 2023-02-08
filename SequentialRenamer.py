import maya.cmds as cmds

rename_to = str(input("Desired name scheme: "))


def sequential_renamer(txt):
    objects = cmds.ls(sl=True)
    count = txt.count('#')
    scheme_parts = txt.partition(count * "#")
    objects_changed = 0

    for i in range(len(objects)):
        new_name = scheme_parts[0] + str(i + 1).zfill(count) + scheme_parts[2]
        cmds.rename(objects[i], new_name)
        objects_changed += 1

    print("Number of Objects renamed: " + str(objects_changed))


sequential_renamer(rename_to)
