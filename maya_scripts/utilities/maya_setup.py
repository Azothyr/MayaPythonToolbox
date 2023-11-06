import maya.cmds as cmds
import sys
from maya_scripts.ui import main_win_tab
from script_tools.functions.file_tools import get_file_path_from_lib as get_path


def set_maya_command_port():
    # Set Maya command line to Pycharm listener
    if not cmds.commandPort(":4434", query=True):
        cmds.commandPort(name=":4434")


def push_scripts_to_sys():
    # Add custom scripts folder to sys.path
    _scripts_folder = get_path(custom_scripts=True)
    if _scripts_folder not in sys.path:
        sys.path.append(_scripts_folder)


def set_tool_tab_on_start():
    # Create Custom Tools tab at the top of the Maya main window for every scene
    cmds.scriptJob(event=("SceneOpened", main_win_tab.create_tools_menu))


def refresh_tools():
    # Refresh the tools menu
    main_win_tab.create_tools_menu()


def get_substance_plugin_working():
    # Houdini Path holds the plugin hostage and makes it, so it will never work
    # Reordering the path fixes the issue, performing below
    print('reorder substance path')
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


if __name__ == "__main__":
    set_maya_on_start()
    refresh_tools()
    