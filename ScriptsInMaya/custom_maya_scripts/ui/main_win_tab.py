import maya.cmds as cmds
import os


def create_custom_menu():
    # Check if the menu already exists; delete it to avoid duplicates
    print("running custom menu")
    if cmds.menu("customToolsMenu", exists=True):
        cmds.deleteUI("customToolsMenu", menu=True)

    # Create the custom menu
    cmds.menu("customToolsMenu", label="Custom Tools", parent="MayaWindow", tearOff=True, allowOptionBoxes=True)

    # Add a simple menu item as an example
    cmds.menuItem(label="Example Item", command="print('Example Item clicked!')", parent="customToolsMenu")

    print("finished custom menu")
