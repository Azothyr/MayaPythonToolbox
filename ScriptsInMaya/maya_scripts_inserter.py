r"""
**MUST RUN ADMIN CMD AND SET THE SYS VARIABLES do not run it multiple times**
code: setx PYTHONPATH "%PYTHONPATH%;C:\Users\.\Documents\maya\customscripts" /M
setx PATH "%PATH%;C:\Users\.\Documents\maya\customscripts" /M
(to check the path and python path in cmd you need to close the terminal and reopen it
 then using echo %PATH% and echo %PYTHONPATH%)
Get all .py _files in the directory and subdirectories this script is run from
Return: Writes Maya userSetup.py and places all custom scripts in Maya directory
Set a sys env variable "pythonpath" with script folder path value.
"""
import os
import platform
import shutil
from textwrap import dedent
from azothyr_tools.function.file_tools import print_files_at_location, clear_directory


if __name__ == "__main__":
    if platform.system() == "Windows":
        platform_name = "win64"  # You don't use this variable in this code. Do you need it?
        scripts_folder = os.path.join(os.path.expanduser('~\\documents\\custom_scripts\\maya_scripts'))
        maya_version = os.environ.get("MAYA_VERSION", "2024")
        maya_path = f"C:\\Program Files\\Autodesk\\Maya{maya_version}\\bin"
        user_setup_path = os.path.join(os.path.expanduser(f"~\\Documents\\maya\\{maya_version}\\scripts\\userSetup.py"))

        code = dedent(f"""\
            import maya.cmds as cmds
            import sys
            import os
            from custom_maya_scripts.ui import main_win_tab
            
            
            # Set Maya command line to Pycharm listener
            if not cmds.commandPort(":4434", query=True):
                cmds.commandPort(name=":4434")

            # Add custom scripts folder to sys.path
            scripts_folder = os.path.join(os.path.expanduser("~"), "Documents", "custom_scripts", "maya_scripts")
            if scripts_folder not in sys.path:
                sys.path.append(scripts_folder)
            
            # Create Custom Tools tab at the top of the Maya main window for every scene
            cmds.scriptJob(event=("SceneOpened", main_win_tab.create_tools_menu))
            """)
        os.makedirs(scripts_folder, exist_ok=True)

        clear_directory(scripts_folder)

        cwd = os.getcwd()
        file_exceptions = ["maya_scripts_inserter.py", "manual_tool_runner.py"]
        try:
            for _root, _dirs, _files in os.walk(cwd):
                for file_name in _files:
                    if file_name.endswith(".py") and file_name not in file_exceptions:
                        rel_path = os.path.relpath(_root, cwd)
                        dest_folder = os.path.join(scripts_folder, rel_path)
                        os.makedirs(dest_folder, exist_ok=True)
                        src_file_path = os.path.join(_root, file_name)
                        dest_file_path = os.path.join(dest_folder, file_name)
                        shutil.copy2(src_file_path, dest_file_path)
        except PermissionError:
            print(f"Insufficient permissions to add folder to '{scripts_folder}'.\nPlease run file as admin...")
        finally:
            print_files_at_location(scripts_folder)

        with open(user_setup_path, 'w') as f:
            f.write(code)
        print(f"Successfully created userSetup.py in {user_setup_path}")
    else:
        raise RuntimeError(f"Unsupported platform: {platform.system()}")
