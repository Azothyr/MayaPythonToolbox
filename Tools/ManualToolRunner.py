import maya.cmds as cmds

rename_to = str(input("Desired name scheme: "))
selections = cmds.ls(sl=True)


def get_selection_center(obj_selection):
    """
    Creates a locator at each selection(s) center of mass.
    Returns: [center_location] (XYZ of the center as a tuple in a list)
    """
    center_location = []

    for selection in obj_selection:
        cluster = cmds.cluster(selection)
        center = cmds.xform(cluster, query=True, rotatePivot=True, worldSpace=True)
        cmds.delete(cluster)
        center_location.append(center)
    return center_location


def create_joints_xyz(xyz_list):
    """
    Creates a joint at each XYZ value from a list.
    Returns: [joints]
    """
    new_joints = []

    for xyz in xyz_list:
        center_position = xyz
        cmds.select(clear=True)
        jnt = cmds.joint()
        new_joints.append(jnt)
        cmds.xform(jnt, worldSpace=True, translation=center_position)
    cmds.select(new_joints, replace=True)
    new_joints.reverse()
    return new_joints


def parent_selected(obj_selection):
    for selection in range(len(obj_selection)):
        cmds.select(clear=True)
        cmds.select(obj_selection[selection])
        if (len(obj_selection) - 1) > selection:
            cmds.select(obj_selection[selection + 1], add=True)
            cmds.parent()


def sequential_renamer(txt, obj_selection):
    """
    Renames selected objects sequentially.
    Returns:
    """
    obj_selection.reverse()
    count = txt.count('#')
    scheme_parts = txt.partition(count * "#")
    objects_changed = 0

    for i in range(len(obj_selection)):
        new_name = scheme_parts[0] + str(i + 1).zfill(count) + scheme_parts[2]
        cmds.rename(obj_selection[i], new_name)
        objects_changed += 1

    print("Number of Objects renamed: " + str(objects_changed))


def orient_joints(obj_selection):
    # obj_selection.reverse()
    last_joint = len(obj_selection) - 1

    for index in range(len(obj_selection)):
        if index == last_joint:
            parent_orientation = cmds.joint(obj_selection[index - 1], query=True, orientation=True)
            cmds.joint(obj_selection[index], edit=True, orientation=parent_orientation)
            break
        cmds.joint(obj_selection[index], edit=True, orientJoint='xyz', secondaryAxisOrient='yup', children=True,
                   zeroScaleOrient=True)


def run_tool():
    center = get_selection_center(selections)
    joints = create_joints_xyz(center)
    parent_selected(joints)
    sequential_renamer(rename_to, joints)


run_tool()
finger_03_knuckle_##_jnt