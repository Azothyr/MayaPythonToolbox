from functools import partial
import maya.cmds as cmds


def parent_scale_constrain(data):
    # Check that there is an even number of objects selected
    if len(data) % 2 != 0:
        cmds.warning("Please select an even number of objects")
        return

    # Cut the selection list in half
    half = int(len(data) / 2)
    parent_objs = data[:half]
    child_objs = data[half:]

    # Create parent and scale constraints for each pair of objects
    for i in range(half):
        parent_const = cmds.parentConstraint(parent_objs[i], child_objs[i], mo=True, sr=['x', 'y', 'z'],
                                             n="{}_parentConstraint".format(child_objs[i]))
        scale_const = cmds.scaleConstraint(parent_objs[i], child_objs[i], n="{}_scaleConstraint".format(child_objs[i]))

        # Set override display on constraints
        parent_const_attrs = cmds.listAttr(parent_const[0], k=True)
        scale_const_attrs = cmds.listAttr(scale_const[0], k=True)
        attrs = parent_const_attrs + scale_const_attrs

        for attr in attrs:
            try:
                cmds.setAttr("{}.{}".format(parent_const[0], attr), l=False)
                cmds.setAttr("{}.{}".format(parent_const[0], attr), 2)
            except:
                pass

            try:
                cmds.setAttr("{}.{}".format(scale_const[0], attr), l=False)
                cmds.setAttr("{}.{}".format(scale_const[0], attr), 2)
            except:
                pass


def parent_scale_constrain_ui(parent_ui, tool):
    parent_scale_tab = cmds.columnLayout(f'{tool}_base', adj=True, bgc=[.3, .1, .1], p=parent_ui)

    cmds.rowColumnLayout(f'{tool}_top_row', p=f'{tool}_base', adj=True, bgc=[.5, .5, .5])
    cmds.columnLayout(f'{tool}_bot_button', p=f'{tool}_base', adj=True, w=200)
    cmds.text(l="Parent, Scale constrain between every other selected objects", p=f'{tool}_top_row')

    def on_execute(*args):
        partial(parent_scale_constrain, cmds.ls(sl=True))()

    cmds.button(f'{tool}_button', l="Parent and Scale", p=f'{tool}_bot_button', c=on_execute, bgc=[0, 0, 0])