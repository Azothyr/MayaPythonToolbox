import maya.cmds as cmds
from functools import partial
from ui import toolbox_ui
from ui.components.utils import utilities_ui, color_change_ui
from ui.components import JointUI, control_ui_create
from pathlib import Path


def run_script(script_path, script_name, name, *_):
    ui_build = {
        "toolbox_ui": toolbox_ui.create_ui_window,
        "color_change_ui": color_change_ui.create_ui_window,
        "control_ui": control_ui_create,
        "joint_ui": partial(JointUI, name, width=500, height=525, create=True),
        "utilities_ui": utilities_ui.create_ui_window
    }
    print(f"---RUNNING:  {script_path}")
    if script_name in ui_build:
        # Call the corresponding function
        ui_build[script_name]()
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
        script_name = script.rsplit("\\", 1)[1].rsplit(".", 1)[0]
        name = script_name.replace("ui", "tool").replace("_", " ").title()
        print("---ADDING TO MAYA: ", script_name)
        # print("Script name:", script_name)
        command_callback = partial(run_script, script, script_name, name)
        print(command_callback)
        cmds.menuItem(
            label=name,
            command=command_callback,
            parent="customToolsMenu"
        )


def _menu_debug_print():
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
    for script in scripts:
        name = script.rsplit("\\", 1)[1].replace("_ui.py", "").title()
        script_name = name + " Tool"
        print("Script name:", script_name)


if __name__ == "__main__":
    __file__ = Path().home() / "Documents" / "GitRepos" / "MayaPythonToolbox" / "maya_scripts" / "ui" / "_main_ui_.py"
    create_tools_menu()
    # _menu_debug_print()

