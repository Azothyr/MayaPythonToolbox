import maya.cmds as cmds
import os
from functools import partial
from ui import toolbox_ui
from ui.components.control import control_ui
from ui.components.utils import utilities_ui, color_change_ui
from ui.components.joint.joint_ui import JointUI
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
    ui_directory = Path(__file__).parent
    print("UI Directory:", ui_directory)
    joint_ui = ui_directory / "components/joint/joint_ui.py"
    util_ui = ui_directory / "components/utils/utilities_ui.py"
    control_ui = ui_directory / "components/control/control_ui.py"

    # List all scripts in the directory
    scripts = [str(item) for item in [joint_ui, util_ui, control_ui]]

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


if __name__ == "__main__":
    ui_directory = Path(__file__).parent
    joint_ui = ui_directory / "components/joint/joint_ui.py"
    util_ui = ui_directory / "components/utils/utilities_ui.py"
    control_ui = ui_directory / "components/control/control_ui.py"
    print(f"UI Directory: {ui_directory}", f"EXISTS: {ui_directory.exists()}")
    print(f"Joint UI: {joint_ui}", f"EXISTS: {joint_ui.exists()}")
    print(f"Util UI: {util_ui}", f"EXISTS: {util_ui.exists()}")
    print(f"Control UI: {control_ui}", f"EXISTS: {control_ui.exists()}")
    scripts = [str(item) for item in [joint_ui, util_ui, control_ui]]
    print("Scripts:", scripts)
