r"""
**MUST RUN ADMIN CMD AND SET THE SYS VARIABLES do not run it multiple times**
code: setx PYTHONPATH "%PYTHONPATH%;C:\Users\.\Documents\custom_scripts" /M
setx PATH "%PATH%;C:\Users\.\Documents\custom_scripts" /M
(to check the path and python path in cmd you need to close the terminal and reopen it
 then using echo %PATH% and echo %PYTHONPATH%)
Get all .py _files in the directory and subdirectories this script is run from
Return: Writes Maya userSetup.py and places all custom scripts in Maya directory
Set a sys env variable "pythonpath" with script folder path value.
"""
import os
import platform
from textwrap import dedent
from azothyr_tools.cus_funcs.file_tools import get_file_path_from_lib as get_path
from azothyr_tools.cus_funcs.file_tools import (clear_directory,
                                                transfer_py_dir_in_current, write_to_file)

if __name__ == "__main__":
    if platform.system() == "Windows":
        repo, maya_scripts_folder, maya_path, user_setup_path = get_path(maya_repo=True,
                                                                         maya=True,
                                                                         maya_exe=True,
                                                                         user_setup=True)
        if repo is None:
            print("No repo found")
            exit()
        code = dedent(f"""\
            import maya.cmds as cmds
            import sys
            from maya_scripts.ui import main_win_tab
            from azothyr_tools.cus_funcs.file_tools import get_file_path_from_lib as get_path
            
            
            # Set Maya command line to Pycharm listener
            if not cmds.commandPort(":4434", query=True):
                cmds.commandPort(name=":4434")

            # Add custom scripts folder to sys.path
            scripts_folder = get_path(custom_scripts=True)
            if scripts_folder not in sys.path:
                sys.path.append(scripts_folder)
            
            # Create Custom Tools tab at the top of the Maya main window for every scene
            cmds.scriptJob(event=("SceneOpened", main_win_tab.create_tools_menu))
            """)
        os.makedirs(maya_scripts_folder, exist_ok=True)

        clear_directory(maya_scripts_folder)
        _exceptions = ["maya_scripts_inserter.py", "manual_tool_runner.py", "Scratch.py"]

        transfer_py_dir_in_current(repo, maya_scripts_folder, _exceptions)

        write_to_file(user_setup_path, code, completion_txt=f"UserSetup.py created successfully at: {user_setup_path}")
    else:
        raise RuntimeError(f"Unsupported platform: {platform.system()}")
