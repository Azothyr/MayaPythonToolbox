import maya.cmds as cmds
import sys
from maya_scripts.ui import main_win_tab
from script_tools.cus_funcs.file_tools import get_file_path_from_lib as get_path


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


def set_maya_on_start():
    set_maya_command_port()
    push_scripts_to_sys()
    set_tool_tab_on_start()
