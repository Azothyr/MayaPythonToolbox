import maya.cmds as cmds
from functools import partial
from ui import toolbox_ui
from ui.components.utils import utilities_ui, color_change_ui
from ui.components import JointUI, control_ui_create
from pathlib import Path


def run_script(script_name, tool_name, *_):
    ui_build = {
        "toolbox_ui": toolbox_ui.create_ui_window,
        "color_ui": color_change_ui.create_ui_window,
        "control_ui": control_ui_create,
        "joint_ui": partial(JointUI, tool_name, width=500, height=525, create=True),
        "utilities_ui": utilities_ui.create_ui_window
    }
    if script_name in ui_build:
        # Call the corresponding function
        ui_build[script_name]()
        print(f"Running script: {script_name}")
    else:
        print(f"Script: {script_name} not found.")


def create_tools_menu():
    # Check if the menu already exists; delete it to avoid duplicates
    if cmds.menu("customToolsMenu", exists=True):
        cmds.deleteUI("customToolsMenu", menu=True)

    # Create the custom menu
    cmds.menu("customToolsMenu", label="Custom Tools", parent="MayaWindow", tearOff=True, allowOptionBoxes=True)

    # Define the directory where the custom scripts reside
    ui_directory = Path(__file__).parent
    print("UI Directory:", ui_directory)
    joint_ui = "joint_ui"
    control_ui = "control_ui"
    color_ui = "color_ui"
    util_ui = "utilities_ui"

    # List all scripts in the directory
    scripts = [str(item) for item in [joint_ui, color_ui, control_ui, util_ui]]

    for script in scripts:
        tool_name = script.replace("ui", "tool").replace("_", " ").title()
        print(f"---ADDING {script.upper()} TO MAYA TOOL MENU")
        command_callback = partial(run_script, script, tool_name)
        print(command_callback)
        cmds.menuItem(
            label=tool_name,
            command=command_callback,
            parent="customToolsMenu"
        )


if __name__ == "__main__":
    __file__ = Path().home() / "Documents" / "GitRepos" / "MayaPythonToolbox" / "maya_scripts" / "ui" / "_main_ui_.py"
    create_tools_menu()

