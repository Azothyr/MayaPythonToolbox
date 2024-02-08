import maya.cmds as cmds
from scratch.channel_box_controllers.connection_cmds import (
    create_attr_proxy, connect_display_type, connect_visibility, exists_or_error, drawing_overrides_state,
    create_display_conditional
)


def fetch_parent_if_in_hierarchy(obj: str, potential_parents: list = None):
    """
    Check if 'obj' has any of the 'potential_parents' in its hierarchy.

    :param obj: The name of the object to check.
    :param potential_parents: A list of names for potential parent objects.
                              This can include specific names or generic identifiers.

    :returns: True if 'obj' has any parent from 'potential_parents' in its hierarchy, False otherwise.
    """
    if not potential_parents:
        potential_parents = []
    if not obj or not cmds.objExists(obj):
        return False

    if isinstance(potential_parents, str):
        potential_parents = [potential_parents]

    common_names = ["geometry", "geo", "mesh", "geometry_grp", "geo_grp", "mesh_grp"]
    potential_parents.extend(common_names)

    obj_full_path = cmds.ls(obj, long=True)[0]
    all_ancestors = cmds.listRelatives(obj, allParents=True, fullPath=True) or []
    all_ancestors.append(obj_full_path)
    # how can I make this gen work?? [name for name for ancestor for ancestor in all_ancestors.split("|") if name]
    ancestors = [ancestor for ancestor in "|".join(all_ancestors).split("|") if ancestor]

    for name in ancestors:
        # print(f"name: {name}")
        for parent in potential_parents:
            if parent == name.lower():
                return name

    return None


def connect_mesh_display(driver, mesh, attr):
    exists_or_error(driver, "connect_mesh_display", attr)
    exists_or_error(mesh, "connect_mesh_display")

    uniqifier = attr.split("_")[0]
    condition_node = f"{driver}_{uniqifier}_display_conditional"
    pma_node = f"{driver}_{uniqifier}_adj_to_display_type_PMA"

    geo_parent = fetch_parent_if_in_hierarchy(mesh)

    drawing_overrides_state(mesh, 1)
    if not cmds.objExists(condition_node) or not cmds.objExists(pma_node):
        create_display_conditional(driver, attr)
    connect_display_type(condition_node, "colorIfTrueG", mesh)
    if not geo_parent:
        connect_visibility(condition_node, "colorIfTrueR", mesh)
    else:
        connect_visibility(condition_node, "colorIfTrueR", geo_parent)
        create_attr_proxy(geo_parent, driver, attr)


def attr_to_all_mesh_display(driver, attr, proxy=False):
    for mesh in cmds.ls(type="mesh"):
        connect_mesh_display(driver, mesh, attr)
        if proxy:
            create_attr_proxy(mesh, driver, attr)


def main():
    driver = "Transform_Ctrl" if cmds.objExists("Transform_Ctrl") else cmds.ls(sl=True)[0]
    if not driver:
        raise ValueError("No driver obj or selection provided.")
    # exit([attr for attr in cmds.listAttr(driver) if "_vis_enum" in attr])
    attr = [attr for attr in cmds.listAttr(driver) if "geometry_vis_enum" in attr][0]
    # exit(attr)
    # exit(cmds.getAttr(attr))
    attr_to_all_mesh_display(driver, attr, proxy=True)


if __name__ == "__main__":
    main()
