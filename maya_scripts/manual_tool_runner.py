import maya.cmds as cmds


def main():
    transferAttrNodes = cmds.ls(type='transferAttributes')

    # Delete all listed nodes
    if transferAttrNodes:
        print(transferAttrNodes)
        cmds.delete(transferAttrNodes, constructionHistory=True)


if __name__ == "__main__":
    main()
