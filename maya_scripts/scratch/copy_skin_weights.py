import maya.cmds as cmds
import maya.mel as mel

"""
get the skin influences
bind influences to all other meshes that are not bound to the skin cluster
    bind to: selected joints
    bind method: closest distance
    skin method: classic linear
    normalize weights: interactive
    weight distribution: distance
    allow multiple bind poses: on
    max influences: 5
    maintain max influences: on
    remove unused influences: off
    colorize skeleton: off
    include hidden selections: off
    deformer node: skin cluster
    
Copy weights from the original skin cluster object to the newly bound objects
"""


def bind_to_skin_cluster(skin_cluster, influences, objects, **kwargs):
    skinned_objects = kwargs.get("skinned_objects", [])
    try:
        for obj in objects:
            print(f"Binding {obj} to {skin_cluster}")
            cmds.select(obj, replace=True)
            new_skin_cluster = cmds.skinCluster(
                influences, obj,
                bindMethod=0,
                skinMethod=0,
                normalizeWeights=1,
                weightDistribution=0,
                maximumInfluences=5,
                removeUnusedInfluence=False,
                lockWeights=False,
                dropoffRate=4,
                name=f"{skin_cluster}_copy",
            )[0]
            cmds.select(clear=True)

            cmds.copySkinWeights(
                sourceSkin=skin_cluster,
                destinationSkin=new_skin_cluster,
                noMirror=True,
                surfaceAssociation="closestPoint",
                influenceAssociation=["closestJoint", "oneToOne"])
            skinned_objects.append(obj)
        cmds.select(clear=True)
    except RuntimeError as e:
        if "already connected" in str(e):
            cmds.warning(f"{e}")
            obj = str(e).split("`")[1].split("`")[0]
            objects = objects[objects.index(obj) + 1:]
            if obj not in skinned_objects:
                skinned_objects.append(obj)
            bind_to_skin_cluster(skin_cluster, influences, objects, skinned_objects=skinned_objects)
        else:
            raise e
    cmds.select(skinned_objects, replace=True)


def main():
    selection = cmds.ls(sl=True)
    find_cmd = f"findRelatedSkinCluster(\"{selection[0]}\")"
    skin_cluster = mel.eval(find_cmd)

    if skin_cluster:
        influences = cmds.skinCluster(skin_cluster, query=True, inf=True)
        # cmds.select(influences, r=True)
    else:
        raise ValueError("No skin cluster found for the selected object.")

    objects = [x for x in cmds.ls(type="transform") if x not in selection and "_geo" in x.lower() and "_grp" not in x.lower()]
    print(f"Objects to bind: {objects}")
    bind_to_skin_cluster(skin_cluster, influences, objects)


if __name__ == "__main__":
    main()
