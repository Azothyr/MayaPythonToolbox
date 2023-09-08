import textwrap
import os
import importlib.util
from azothyr_tools.cus_funcs.file_tools import write_to_file
from azothyr_tools.cus_funcs.file_tools import get_file_path_from_lib as get_path


def _load_map_from_file_path(file_path):
    _map, path = file_path
    print(f"Loading metadata for {_map} from file.")
    if not os.path.exists(path):
        raise ValueError(f"File does not exist: {path}")
    _map_name = _map + "_arg_map"

    module_spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)

    return getattr(module, _map_name)


def retrieve_metadata(attr, arg_map):
    if isinstance(arg_map, list) or isinstance(arg_map, tuple):
        arg_map = _load_map_from_file_path(arg_map)
    formatted_meta = []
    if str(attr).lower() == "all":
        for k, v in arg_map.items():
            try:
                formatted_meta.append(
                    f"Name: {k} -> {v['name']} | Arg: {v['type']} | Use case: {v['property']}\n"
                    f"\tDescription: {textwrap.fill(v['description'], width=80)}\n")
            except KeyError:
                print(f"KeyError for dictionary: {k}    ->    {v}")
                continue
        return '\n'.join(formatted_meta)
    elif str(attr).lower() == "args":
        for k, v in arg_map.items():
            formatted_meta.append(f"Name: {k} -> {v['name']}")

        return '\n'.join(formatted_meta)
    elif attr in arg_map:
        sn = attr
        ln = arg_map[attr]['name']
        desc = arg_map[attr]['description']
        typ = arg_map[attr]['type']
        prop = arg_map[attr]['property']
        return (f"Name: {sn} -> {ln} | Arg: {typ} | Use case: {prop}\n"
                f"\tDescription: {textwrap.fill(desc, width=80)}\n")
    else:
        for k, v in arg_map.items():
            if attr == v['name']:
                sn = k
                ln = attr
                desc = v['description']
                typ = v['type']
                prop = v['property']
                return (f"Name: {sn} -> {ln} | Arg: {typ} | Use case: {prop}\n"
                        f"\tDescription: {textwrap.fill(desc, width=80)}\n")
    return f"Key \'{attr}\' was not found in Arg Map."


def set_class_kwargs(class_, arg_map, **kwargs):
    for key, value in arg_map.items():
        setattr(class_, value['name'], kwargs.get(value['name']))
        setattr(class_, f"{value['name']}_description", value.get('description'))
        setattr(class_, f"{key}_description", value.get('description'))
        setattr(class_, f"{value['name']}_property", value.get('property'))
        setattr(class_, f"{key}_property", value.get('property'))
        setattr(class_, f"{value['name']}_type", value.get('type'))
        setattr(class_, f"{key}_type", value.get('type'))


def translate_for_arg_map(arg_map, kwargs):
    # Translate kwargs keys if they are in arg_mapping (short or long form)
    translated_kwargs = {}
    for key, value in kwargs.items():
        if key in arg_map:  # if in short form
            translated_kwargs[arg_map[key]['name']] = value
        elif any(data['name'] == key for data in arg_map.values()):  # long form
            translated_kwargs[key] = value
        else:
            print(f"Warning: Key \'{key}\' not recognized. Skipping...")
    return translated_kwargs


def translate_for_kwargs(arg_map, kwargs):
    # Translate kwargs keys if they are in arg_mapping (short or long form)
    translated_kwargs = []

    for key, value in kwargs.items():
        if key in arg_map:  # if in short form
            translated_kwargs.append((key, arg_map[key]['name'], value))
        else:
            # Check if in long form
            for short_name, data in arg_map.items():
                if data['name'] == key:
                    translated_kwargs.append((short_name, key, value))
                    break
            else:
                print(f"Warning: Key \'{key}\' not recognized. Skipping...")
    return translated_kwargs


def refresh_arg_lib():
    print("preparing to refresh Arg Library")
    arg_lib_path, arg_maps = get_path(maya_arg_lib=True, arg_maps=True)
    lines_to_write = ["import os",
                      "from azothyr_tools.cus_funcs.file_tools import get_file_path_from_lib as get_path\n",
                      f"base_path = get_path(maya_info=True)",
                      "arg_lib = {"]
    for key, value in arg_maps:
        lines_to_write.append(f"\t'{key}': {value},")
    lines_to_write.append("}")

    write_to_file(arg_lib_path, "\n".join(lines_to_write))
    return "Completed library refresh"


if __name__ == "__main__":
    refresh_arg_lib()
