import maya.cmds as cmds


def main():
    exclude = ["tooth", "gums", "poly", "shape"]
    meshes = set([
        cmds.listRelatives(mesh, parent=True)[0] for mesh in cmds.ls(type="mesh")
        if not any(
            keyword.lower() in cmds.listRelatives(mesh, parent=True)[0].lower()
            for keyword in exclude
        )
    ])
    meshes = sorted(meshes, key=lambda x: x.split("_")[1] if "l_" in x or "r_" in x else x.split("_")[0])
    print("\n".join(meshes))
    cmds.select(clear=True)
    for mesh in meshes:
        cmds.select(mesh, add=True)


def main2():
    selection = cmds.ls()
    replace = "Imp1:"
    for object in selection:
        try:
            if cmds.lockNode(object, query=True)[0]:
                continue

            new_name = object.replace(replace, "")
            cmds.rename(object, new_name)
        except Exception:
            continue


if __name__ == "__main__":
    main()
    # main2()
