import maya.cmds as cmds
import os
from functools import partial
from maya_scripts.ui import color_change_ui, control_ui, joint_ui, toolbox_ui, utilities_ui


def run_script(script_path, *_):
    ui_build = {
        "color_change_ui": color_change_ui.create_ui_window,
        "control_ui": control_ui.create_ui_window,
        "joint_ui": joint_ui.create_ui_window,
        "toolbox_ui": toolbox_ui.create_ui_window,
        "utilities_ui": utilities_ui.create_ui_window
    }
    print(script_path)
    if script_path in ui_build:
        # Call the corresponding function
        ui_build[script_path]()
    else:
        print(f"No UI function found for {script_path}")


def create_tools_menu():
    # Check if the menu already exists; delete it to avoid duplicates
    if cmds.menu("customToolsMenu", exists=True):
        cmds.deleteUI("customToolsMenu", menu=True)

    # Create the custom menu
    cmds.menu("customToolsMenu", label="Custom Tools", parent="MayaWindow", tearOff=True, allowOptionBoxes=True)

    # Define the directory where the custom scripts reside
    script_directory =

    # List all scripts in the directory
    scripts = [script for script in os.listdir(script_directory) if script.endswith(('.mel', '_ui.py'))]

    for script in scripts:
        print("Original Script:", script)
        script_name = script.split("_")[0].capitalize() + " Tool"
        script_path = script.split(".")[0]
        print("Script name:", script_name)
        print("Script Path:", script_path)
        command_callback = partial(run_script, script_path)
        print(command_callback)
        cmds.menuItem(
            label=script_name,
            command=command_callback,
            parent="customToolsMenu"
        )

    print("Script Directory:", script_directory)
