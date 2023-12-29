from pathlib import Path

base_path = Path(__file__).parent / "arg_lib_info"
arg_lib = {
    "button": Path(base_path, "button_arg_map.py"),
    "columnLayout": Path(base_path, "columnLayout_arg_map.py"),
    "menuItem": Path(base_path, "menuItem_arg_map.py"),
    "optionMenu": Path(base_path, "optionMenu_arg_map.py"),
    "rowColumnLayout": Path(base_path, "rowColumnLayout_arg_map.py"),
    "tabLayout": Path(base_path, "tabLayout_arg_map.py"),
    "textField": Path(base_path, "textField_arg_map.py"),
    "text": Path(base_path, "text_arg_map.py"),
    "window": Path(base_path, "window_arg_map.py"),
    "all": Path(base_path.parent, "arg_lib.py"),
}

if __name__ == "__main__":
    for key, value in arg_lib.items():
        print(f"{key}:", f"FILEPATH: {value}", f"EXISTS: {Path(value).exists()}", sep="\n---->", end="\n\n")
