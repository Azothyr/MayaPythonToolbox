import maya.cmds as cmds
import sys
from ui import _main_ui_  # noqa
from pathlib import Path


def set_maya_command_port():
    # Set Maya command line to Pycharm listener
    if not cmds.commandPort(":4434", query=True):
        cmds.commandPort(name=":4434")


def push_scripts_to_sys():
    # Add custom scripts folder to sys.path
    scripts_folder = str(Path(__file__).parent.parent)
    if scripts_folder not in sys.path:
        sys.path.append(scripts_folder)


def set_tool_tab_on_start():
    # Create Custom Tools tab at the top of the Maya main window for every scene
    cmds.scriptJob(event=("SceneOpened", _main_ui_.create_tools_menu))


def refresh_tools():
    # Refresh the components menu
    _main_ui_.create_tools_menu()


def get_substance_plugin_working():
    # Houdini Path holds the plugin hostage and makes substance unable to load
    # Reordering the path fixes the issue, performing below
    print('reordering substance path')
    import os
    path = os.getenv('PATH')
    path_items = path.split(';')
    houdini_path = ''
    substance_path = ''
    for string in path_items:
        if 'Substance' in string:
            substance_path = string
            continue
        if 'Houdini' in string:
            houdini_path = string
            continue

    if substance_path:
        path_items.remove(substance_path)
    if houdini_path:
        path_items.remove(houdini_path)

    path_items.append(substance_path)
    path_items.append(houdini_path)

    path_reorder = ';'.join(path_items)
    os.environ["PATH"] = path_reorder


def set_maya_on_start():
    get_substance_plugin_working()
    set_maya_command_port()
    push_scripts_to_sys()
    set_tool_tab_on_start()


def create_user_setup(year: str = None):
    user_setup = str(Path(cmds.internalVar(userScriptDir=True) / "userSetup.py")) if \
        cmds.internalVar(userScriptDir=True) else \
        str(Path(Path.home() / f"documents/maya/{year}/scripts/userSetup.py")) if year else None
    try:
        if not Path(user_setup).parent.exists():
            raise FileNotFoundError(f"Could not find userSetup.py at {user_setup}")
    except TypeError:
        raise TypeError("Could not find userSetup.py")
    print(f"Provided Path Validated...\n---ATTEMPT--- Creating userSetup.py at: '{user_setup}'...")
    with open(user_setup, "w") as file:
        file.write("from config.maya_setup import set_maya_on_start\n\n")
        file.write("set_maya_on_start()\n")
    if Path(user_setup).exists():
        print(f"---SUCCESS--- created userSetup.py at {user_setup}")
    else:
        print(f"---FAIL--- to create userSetup.py at {user_setup}")


if __name__ == "__main__":
    set_maya_on_start()
    # refresh_tools()
    # create_user_setup("2024")
