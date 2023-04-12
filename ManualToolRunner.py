import maya.cmds as cmds

selection = cmds.ls(sl=True)


def get_center(_input):
    """
    finds the selection(s) center of mass.
    Returns: (center x, center y, center z)
    """
    print(_input)
    bbox = cmds.exactWorldBoundingBox(_input)

    center = (
        (bbox[0] + bbox[3]) / 2,
        (bbox[1] + bbox[4]) / 2,
        (bbox[2] + bbox[5]) / 2
    )

    return center


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


def parent_selected(data):
    for value in range(len(data)):
        cmds.select(clear=True)
        cmds.select(data[value])
        if (len(data) - 1) > value:
            cmds.select(data[value + 1], add=True)
            cmds.parent()


def sequential_renamer(txt, data):
    """
    Renames selected objects sequentially.
    Returns:
    """
    data.reverse()
    count = txt.count('#')
    scheme_parts = txt.partition(count * "#")
    objects_changed = 0

    for i in range(len(data)):
        new_name = scheme_parts[0] + str(i + 1).zfill(count) + scheme_parts[2]
        cmds.rename(data[i], new_name)
        objects_changed += 1

    print("Number of Objects renamed: " + str(objects_changed))


def orient_joints(data):
    last_joint = len(data) - 1

    for index in range(len(data)):
        if index == last_joint:
            parent_orientation = cmds.joint(data[index - 1], query=True, orientation=True)
            cmds.joint(data[index], edit=True, orientation=parent_orientation)
            break
        cmds.joint(data[index], edit=True, orientJoint='xyz', secondaryAxisOrient='yup', children=True,
                   zeroScaleOrient=True)


def run_tool(arg=None):
    global location
    if 'location' not in globals():
        location = []
    center = get_center(cmds.ls(sl=True))
    if arg is None:
        location.append(center)
        return print(location)
    elif arg == 'clear':
        location.clear()
        print('list cleared')
    else:
        rename_to = str(input("Desired name scheme: "))
        joints = create_joints_xyz(location)
        parent_selected(joints)
        sequential_renamer(rename_to, joints)


run_tool()