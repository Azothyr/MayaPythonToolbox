import maya.cmds as cmds
import os

# Define the directory where your custom scripts are located
custom_scripts_dir = "C:/Program Files/Autodesk/Maya2022/custom scripts"

# Get a list of all .py files in the custom scripts directory
script_files = [file for file in os.listdir(custom_scripts_dir) if file.endswith(".py")]

# Create a main window with a form layout
window = cmds.window(title="Custom Scripts", widthHeight=(300, 100))
form_layout = cmds.formLayout()

# Create a text label and a drop-down list
text_label = cmds.text(label="Select a script:")
option_menu = cmds.optionMenu()

# Add each script file name as an option in the drop-down list
for script_file in script_files:
    cmds.menuItem(label=script_file, parent=option_menu)

# Position the text label and drop-down list in the form layout
cmds.formLayout(form_layout, edit=True, attachForm=[(text_label, 'left', 10), (text_label, 'top', 10)])
cmds.formLayout(form_layout, edit=True, attachControl=[(option_menu, 'left', 10, text_label), (option_menu, 'top', 10, text_label)])

# Show the window
cmds.showWindow(window)