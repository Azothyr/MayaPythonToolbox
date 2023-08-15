"""
Get all .py files in the directory and subdirectories this script is run from
Return: Writes Maya userSetup.py and places all custom scripts in Maya directory
Set a sys env variable "pythonpath" with script folder path value.
"""
import os
import sys
import platform
import shutil
import subprocess
from textwrap import dedent

# Get the computer's Maya and OS/Platform version
maya_version = os.environ.get("MAYA_VERSION")
if not maya_version:
    maya_version = "2022"  # Set a default value if the environment variable isn't set

# Confirm this is run on a Windows machine, raise an exception if not
if platform.system() == "Windows":
    platform_name = "win64"
    user_name = os.getlogin()
    # defines where maya is installed
    maya_path = f"C:\\Program Files\\Autodesk\\Maya{maya_version}\\bin"
    # Set the path to the scripts folder
    scripts_folder = f"C:\\Users\\{user_name}\\Documents\\maya\\{maya_version}\\scripts"
    # Create a path to the scripts folder, if it already exists, don't raise an error and continue
    os.makedirs(scripts_folder, exist_ok=True)
    # Open command prompt window and echo
    subprocess.Popen(['cmd.exe', '/k', 'echo'])

    # Get the current working directory
    cwd = os.getcwd()

    # Set the path to the userSetup.py file
    user_setup_path = os.path.join(os.path.expanduser("~"), "Documents", "maya", f"{maya_version}", "scripts",
                                   "userSetup.py")

    # Get the current environment variables
    env = os.environ.copy()

    # Add the custom scripts directory to the PYTHONPATH variable
    if scripts_folder not in sys.path:
        sys.path.append(scripts_folder)
    # Add the custom scripts directory to the PYTHONPATH variable
    if 'PYTHONPATH' in os.environ:  # if PYTHONPATH key is in SYS ENV Variables
        os.environ['PYTHONPATH'] = scripts_folder + os.pathsep + os.environ['PYTHONPATH']  # add scripts as item
    else:
        os.environ['PYTHONPATH'] = scripts_folder  # create PYTHONPATH key with script folder as item
    if scripts_folder in (os.environ.get('PYTHONPATH')):
        print('SUCCESSFULLY added Script\'s path to PYTHONPATH')
    else:
        print('FAILED to add Script\'s path to PYTHONPATH')

    # Add Maya bin directory to PATH
    if 'PATH' in os.environ:
        os.environ['PATH'] = maya_path + os.pathsep + os.environ['PATH']
    else:
        os.environ['PATH'] = maya_path
    if maya_path in (os.environ.get('PATH')):
        print('SUCCESSFULLY added Maya path to PATH')
    else:
        print('FAILED to add Maya path to PYTHONPATH')

    # Set the updated environment variables
    os.environ.update(env)

    # Attempt to write to program files, print on permission error
    try:
        # Loops through all files and subdirectories in the cwd (current working directory)
        for root, dirs, files in os.walk(cwd):
            for file_name in files:
                if file_name.endswith(".py"):
                    # Calculate relative path
                    rel_path = os.path.relpath(root, cwd)
                    # Join the relative path with the destination to make a full path
                    dest_folder = os.path.join(scripts_folder, rel_path)

                    # If the destination directory doesn't exist, create it
                    os.makedirs(dest_folder, exist_ok=True)

                    # Calculate source and destination file paths
                    src_file_path = os.path.join(root, file_name)
                    dest_file_path = os.path.join(dest_folder, file_name)

                    # Copy the file from source to destination
                    shutil.copy2(src_file_path, dest_file_path)
                    # print(f"{file_name} has been copied to the scripts folder.")
    except PermissionError:
        print(f"Insufficient permissions to add folder to '{scripts_folder}'.\nPlease run file as admin...")

    # lines of code formatted to be run as a .py in the Maya user setup script
    code = dedent(f"""    import maya.cmds as cmds
    import os

    # Set Maya command line to Pycharm listener
    if not cmds.commandPort(":4434", query=True):
        cmds.commandPort(name=":4434")
    
    # Replace "path_to_scripts_folder" with the actual path to your folder containing scripts
    scripts_folder = "{scripts_folder}"
    """)

    # Write user setup script to Maya scripts location with the above code
    with open(os.path.join(os.path.expanduser("~"), 'Documents', 'maya', 'scripts', 'userSetup.py'), 'w') as f:
        f.write(code)
    # print(f"Successfully created userSetup.py in {user_setup_path}")

    # Keeps the command prompt open and lets the user know to exit
    input('Complete, please exit...')
else:
    raise RuntimeError(f"Unsupported platform: {platform.system()}")
    # Replace "path_to_scripts_folder" with the actual path to your folder containing scripts
