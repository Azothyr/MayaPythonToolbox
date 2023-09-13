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
from maya_scripts.utilities.maya_setup import push_scripts_to_sys
from utils.file_ops import get_file_path_from_lib as get_path
from utils.file_ops import (clear_directory, transfer_py_dir_in_current, write_to_file)


def check_if_windows():
    if platform.system() == "Windows":
        return True
    else:
        raise RuntimeError(f"Unsupported platform: {platform.system()}")


def main():
    if not check_if_windows():
        exit()
    repo, maya_scripts_folder, maya_path, user_setup_path = get_path(maya_repo=True,
                                                                     maya=True,
                                                                     maya_exe=True,
                                                                     user_setup=True,
                                                                     debug=True)
    # print(repo, maya_scripts_folder, maya_path, user_setup_path)
    if repo is None:
        print("No repo found")
        exit()
    code = dedent(f"""\
            from maya_scripts.utilities.maya_setup import set_maya_on_start

            set_maya_on_start()
            """)
    os.makedirs(maya_scripts_folder, exist_ok=True)

    clear_directory(maya_scripts_folder)
    _exceptions = ["maya_scripts_inserter.py", "manual_tool_runner.py", "Scratch.py"]

    transfer_py_dir_in_current(repo, maya_scripts_folder, _exceptions)

    write_to_file(user_setup_path, code, completion_txt=f"UserSetup.py created successfully at: {user_setup_path}")

    push_scripts_to_sys()


if __name__ == "__main__":
    main()
