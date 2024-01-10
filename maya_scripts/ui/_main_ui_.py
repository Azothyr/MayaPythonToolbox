import maya.cmds as cmds
import os
from functools import partial
from ui import color_change_ui, control_ui, toolbox_ui, utilities_ui
from ui.joint_ui import JointUI
from pathlib import Path


def run_script(script_path, name, script_name, *_):
    ui_build = {
        "toolbox_ui": toolbox_ui.create_ui_window,
        "color_change_ui": color_change_ui.create_ui_window,
        "control_ui": control_ui.create_ui_window,
        "joint_ui": JointUI(name, script_name, "default"),
        "utilities_ui": utilities_ui.create_ui_window
    }
    print(f"---RUNNING:  {script_path}")
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
    script_directory = str(Path(__file__).parent.parent / "ui")
    # print("Script Directory:", script_directory)

    # List all scripts in the directory
    scripts = [script for script in os.listdir(script_directory) if script.endswith(('_ui.mel', '_ui.py'))]

    for script in scripts:
        print("---ADDING TO MAYA: ", script)
        name = script.rsplit("_", 1)[0].replace("_", " ").title()
        script_name = name + " Tool"
        script_path = script.rsplit(".", 1)[0]
        # print("Script name:", script_name)
        # print("Script Path:", script_path)
        command_callback = partial(run_script, script_path, name, script_name)
        # print(command_callback)
        cmds.menuItem(
            label=script_name,
            command=command_callback,
            parent="customToolsMenu"
        )

    # print("Script Directory:", script_directory)


if __name__ == "__main__":
    create_tools_menu()
