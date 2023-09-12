import maya.cmds as cmds

# def orient_joint_hierarchy(root_joint, primary='x', secondary='z'):
#     """
#     Orient a joint and all its child joints with world orientation on secondary axis.
#
#     :param root_joint: The root joint of the hierarchy.
#     :param primary: Primary axis. Default is 'x'.
#     :param secondary: Secondary axis. Default is 'z'.
#     :return: None
#     """
#
#     # Get all child joints
#     child_joints = cmds.listRelatives(root_joint, ad=True, type='joint')
#
#     # Add root joint to the list
#     if child_joints:
#         joints_to_orient = [root_joint] + child_joints
#     else:
#         joints_to_orient = [root_joint]
#
#     # Create a temporary locator that we will use as our aim target
#     locator = cmds.spaceLocator(name="tempAimLocator")[0]
#     cmds.setAttr(locator + ".translateX", 10)  # Moving the locator in X direction
#
#     # Loop through each joint and orient them
#     for joint in joints_to_orient:
#         # Unparent the children temporarily
#         children = cmds.listRelatives(joint, c=True)
#         if children:
#             cmds.parent(children, w=True)
#
#         # Use an aimConstraint for orientation
#         constraint = cmds.aimConstraint(
#             locator, joint,
#             aimVector=(1, 0, 0),
#             upVector=(0, 1, 0),  # This is a temporary upVector, just to ensure the aim works correctly
#             worldUpType="vector",
#             worldUpVector=(1, 0, 0)
#         )
#
#         # Delete the constraint after setting the orientation
#         cmds.delete(constraint)
#
#         # Reparent the children
#         if children:
#             cmds.parent(children, joint)
#
#     # Delete the temporary locator
#     cmds.delete(locator)
#
#     print("Joints oriented successfully!")
#
#
# orient_joint_hierarchy(cmds.ls(type='joint'))


def set_xform_values(**kwargs):
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("No objects selected.")
        return

    rotation = kwargs.get('rotation', None)
    translation = kwargs.get('translation', None)
    joint_orient = kwargs.get('joint_orient', None)
    x = kwargs.get('x', None)
    y = kwargs.get('y', None)
    z = kwargs.get('z', None)

    for obj in selected_objects:
        # Setting rotations
        if rotation:
            if x is not None:
                cmds.setAttr(obj + '.rotateX', x)
            if y is not None:
                cmds.setAttr(obj + '.rotateY', y)
            if z is not None:
                cmds.setAttr(obj + '.rotateZ', z)

        # Setting translations
        if translation:
            if x is not None:
                cmds.setAttr(obj + '.translateX', x)
            if y is not None:
                cmds.setAttr(obj + '.translateY', y)
            if z is not None:
                cmds.setAttr(obj + '.translateZ', z)

        # Setting joint orientations
        if cmds.objectType(obj) == 'joint' and joint_orient:
            if x is not None:
                cmds.setAttr(obj + '.jointOrientX', x)
            if y is not None:
                cmds.setAttr(obj + '.jointOrientY', y)
            if z is not None:
                cmds.setAttr(obj + '.jointOrientZ', z)

    print("Transformations set successfully.")


def select_all_hierarchy(lyst):
    for obj in lyst:
        children = cmds.listRelatives(obj, allDescendents=True)
        cmds.select(children, add=True)
    cmds.select(lyst[0], add=True)

# set_xform_values(rotation=True, x=0)
select_all_hierarchy(cmds.ls(selection=True))