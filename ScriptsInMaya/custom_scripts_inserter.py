"""
Get all .py files in the directory and subdirectories this script is run from
Return: Writes Maya userSetup.py and places all custom scripts in Maya directory
Set a sys env variable "pythonpath" with script folder path value.
"""
import os
import platform
import shutil
import sys
from textwrap import dedent


def pass_path(var):
    var = os.environ[var].split(";")
    print_list_content(var)


def print_list_content(lyst):
    for value in lyst:
        print(value)


if __name__ == "__main__":
    maya_version = os.environ.get("MAYA_VERSION", "2022")
    if platform.system() == "Windows":
        platform_name = "win64"  # You don't use this variable in this code. Do you need it?
        scripts_folder = os.path.join(os.path.expanduser("~"), "Documents", "customscripts")
        maya_path = f"C:\\Program Files\\Autodesk\\Maya{maya_version}\\bin"
        user_setup_path = os.path.join(os.path.expanduser("~"), "Documents", "maya", f"{maya_version}", "scripts",
                                       "userSetup.py")

        code = dedent(f"""\
            import maya.cmds as cmds
            import os

            # Set Maya command line to Pycharm listener
            if not cmds.commandPort(":4434", query=True):
                cmds.commandPort(name=":4434")

            # Add custom scripts folder to sys.path
            scripts_folder = os.path.join(os.path.expanduser("~"), "Documents", "customscripts")
            if scripts_folder not in sys.path:
                sys.path.append(scripts_folder)
            """)

        os.makedirs(scripts_folder, exist_ok=True)

        cwd = os.getcwd()
        try:
            for root, dirs, files in os.walk(cwd):
                for file_name in files:
                    if file_name.endswith(".py") and file_name != "custom_scripts_inserter.py":
                        rel_path = os.path.relpath(root, cwd)
                        dest_folder = os.path.join(scripts_folder, rel_path)
                        os.makedirs(dest_folder, exist_ok=True)
                        src_file_path = os.path.join(root, file_name)
                        dest_file_path = os.path.join(dest_folder, file_name)
                        shutil.copy2(src_file_path, dest_file_path)
        except PermissionError:
            print(f"Insufficient permissions to add folder to '{scripts_folder}'.\nPlease run file as admin...")

        with open(user_setup_path, 'w') as f:
            f.write(code)
        print(f"Successfully created userSetup.py in {user_setup_path}")
    else:
        raise RuntimeError(f"Unsupported platform: {platform.system()}")
