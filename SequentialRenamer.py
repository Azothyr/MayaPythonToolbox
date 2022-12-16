import maya.cmds as cmds

renameTo = str(input("Desired name scheme: "))

def SequentialRenamer(txt):
    objs = cmds.ls(sl=True)
    count = txt.count('#')
    schemeParts = txt.partition(count * "#")
    objsChanged = 0

    for i in range(len(objs)):
        newName = schemeParts[0] + str(i + 1).zfill(count) + schemeParts[2]
        cmds.rename(objs[i], newName)
        objsChanged += 1

    print("Number of Objects renamed: " + str(objsChanged))

SequentialRenamer(renameTo)
