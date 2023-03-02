"""
Get all .py files in the directory and subdirectories this script is run from
Return: Writes Maya userSetup.py and places all custom scripts in Maya directory
userSetup.py will run on opening maya and will set a python path to custom scripts
"""
import subprocess
import os
import platform
import textwrap
import shutil
# import keyboard

# Open command prompt
subprocess.Popen(['cmd.exe', '/k', 'echo Running my script...'])

# Get the current working directory
cwd = os.getcwd()

# Set the path to the userSetup.py file
user_setup_path = os.path.join(os.path.expanduser("~"), "Documents", "maya", "scripts", "userSetup.py")

# Get the computer's Maya and OS/Platform version
maya_version = os.environ.get("MAYA_VERSION")
if not maya_version:
    maya_version = "2022"  # Set a default value if the environment variable isn't set

scripts_folder = "N/A"

if platform.system() == "Windows":
    platform_name = "win64"
    # Set the path to your scripts folder
    scripts_folder = f"C:\Program Files\Autodesk\Maya{maya_version}\custom scripts"
    os.makedirs(scripts_folder, exist_ok=True)
elif platform.system() == "Darwin":
    platform_name = "mac"
    raise RuntimeError(f"Unsupported platform: {platform_name}")
else:
    raise RuntimeError(f"Unsupported platform: {platform.system()}")

# Attempt to write to program files, print on permission error
try:
    # Loops through all files and subdirectories in the cwd (current working directory)
    for root, dirs, files in os.walk(cwd):
        # Loop through all files in the current subdirectory
        for file_name in files:
            # Check if the file is a Python file
            if file_name.endswith(".py"):
                # Get the full path of the file
                file_path = os.path.join(root, file_name)
                # Check if a file with the same name already exists in the destination directory
                shutil.copy(file_path, scripts_folder)
                print(f"{file_name} has been copied to the scripts folder.")
except PermissionError:
    print(f"Insufficient permissions to add folder to '{scripts_folder}'.\nPlease re-run as admin.")

# lines of code formatted to be run as a .py in the Maya user setup script
code = textwrap.dedent(f"""    import os
    import maya.cmds as cmds
    
    # Set Maya command line to Pycharm listener
    if not cmds.commandPort(":4434", query=True):
        cmds.commandPort(name=":4434")
    
    # OS type
    platform_name = "{platform_name}"
    # Script folder path
    scripts_folder = "{scripts_folder}"
    
    # Set the path of the Maya.env file
    if platform_name == "win64":
        maya_env_path = os.path.join(
            f"C:/Program Files/Autodesk/Maya{maya_version}/Maya.env"
        )
    else:
        maya_env_path = os.path.join(
            os.path.expanduser(f"~/Library/Preferences/Autodesk/maya/{maya_version}/Maya.env")
        )
    
    # Create the Maya.env file if it doesn't already exist, which will set a path to custom .py scripts for use in Maya
    if not os.path.exists(maya_env_path):
        with open(maya_env_path, "w") as file:
            file.write(f"PYTHONPATH={{scripts_folder}}:$PYTHONPATH\\n")
""")

# Write user setup script to <aya scripts location with the above code
with open(os.path.join(os.path.expanduser("~"), 'Documents', 'maya', 'scripts', 'userSetup.py'), 'w') as f:
    f.write(code)

print(f"Successfully created userSetup.py in {user_setup_path}")


# Keeps the command prompt open and lets the user know to exit
input('Press Enter to exit...')

'''def input_with_exit(prompt=''):
    print(prompt, end='', flush=True)
    user_input = ''
    keyboard.add_hotkey('enter', lambda: keyboard.write('\n'))
    keyboard.wait('enter')
    keyboard.remove_hotkey('enter')
    return user_input


input_with_exit('Press Enter to exit...')'''
