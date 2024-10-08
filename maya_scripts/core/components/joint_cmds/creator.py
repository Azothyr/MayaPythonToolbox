import maya.cmds as cmds


def _check_for_root() -> str:
    """
    Checks for a root joint in the scene.
    If none is found, return "world"
    :return:
    """
    root_names = {"skeleton", "root", "skeleton_root", "skeleton_root"}
    objects = cmds.ls(type="transform")

    if not objects:
        return "world"

    for obj in objects:
        if obj.lower() in root_names:
            return obj

    return "world"


def _set_joint_channels(joint: str) -> None:
    joint_orient_attrs = ['jointOrientX', 'jointOrientY', 'jointOrientZ', 'displayLocalAxis']
    for attr_name in joint_orient_attrs:
        cmds.setAttr(f"{joint}.{attr_name}", keyable=False, channelBox=True)


def create_joints_xyz(xyz_list, radius=None, parent_bool=None, parent_name=None) -> list[str]:
    """
    :return: list of joints created
    """
    new_joints = []
    parent_name = (parent_name or _check_for_root()) if parent_bool else None
    radius = radius or 1

    # Start with no selection if no parent is specified, or select the parent if it's provided
    if parent_name:
        cmds.select(parent_name)
    else:
        cmds.select(clear=True)

    for i, position in enumerate(xyz_list):
        jnt = cmds.joint(rad=radius)
        new_joints.append(jnt)
        _set_joint_channels(jnt)
        cmds.xform(jnt, worldSpace=True, translation=position)

        if i == 0 and parent_name:
            current_parent = cmds.listRelatives(jnt, parent=True)
            if current_parent:
                current_parent = current_parent[0]
            if not current_parent or current_parent != parent_name:
                cmds.parent(jnt, parent_name)

    cmds.select(new_joints, replace=True)
    return new_joints

