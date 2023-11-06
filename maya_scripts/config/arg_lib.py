import os

base_path = os.path.expanduser('~/Documents/custom_scripts/maya_scripts/config')
arg_lib = {
    'button': os.path.join(base_path, 'button_arg_map.py'),
    'columnLayout': os.path.join(base_path, 'columnLayout_arg_map.py'),
    'menuItem': os.path.join(base_path, 'menuItem_arg_map.py'),
    'optionMenu': os.path.join(base_path, 'optionMenu_arg_map.py'),
    'rowColumnLayout': os.path.join(base_path, 'rowColumnLayout_arg_map.py'),
    'tabLayout': os.path.join(base_path, 'tabLayout_arg_map.py'),
    'textField': os.path.join(base_path, 'textField_arg_map.py'),
    'text': os.path.join(base_path, 'text_arg_map.py'),
    'window': os.path.join(base_path, 'window_arg_map.py'),
    'all': os.path.join(base_path, 'arg_lib.py'),
}
