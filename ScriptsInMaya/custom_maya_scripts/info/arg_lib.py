import os

base_path = os.path.join(os.path.expanduser("~"), "Documents", "maya", "customscripts", "custom_maya_scripts", "info")
arg_lib = {
	"button": ("button", os.path.join(base_path, "button_arg_map.py")),
	"columnLayout": ("columnLayout", os.path.join(base_path, "columnLayout_arg_map.py")),
	"menuItem": ("menuItem", os.path.join(base_path, "menuItem_arg_map.py")),
	"optionMenu": ("optionMenu", os.path.join(base_path, "optionMenu_arg_map.py")),
	"rowColumnLayout": ("rowColumnLayout", os.path.join(base_path, "rowColumnLayout_arg_map.py")),
	"tabLayout": ("tabLayout", os.path.join(base_path, "tabLayout_arg_map.py")),
	"textField": ("textField", os.path.join(base_path, "textField_arg_map.py")),
	"text": ("text", os.path.join(base_path, "text_arg_map.py")),
	"window": ("window", os.path.join(base_path, "window_arg_map.py")),
	"all": ("all", os.path.join(base_path, "arg_lib.py"))
}
