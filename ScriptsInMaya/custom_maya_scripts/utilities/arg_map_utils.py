import textwrap
import os


def retrieve_metadata(attr, arg_map):
    formatted_meta = []
    if str(attr).lower() == "all":
        for k, v in arg_map.items():
            formatted_meta.append(
                f"Name: {k} -> {v['name']} | Arg: {v['type']} | Use case: {v['property']}\n"
                f"\tDescription: {textwrap.fill(v['description'], width=80)}\n")
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


def translate_arg_map_keys(arg_map, kwargs):
    # Translate kwargs keys if they are in arg_mapping (short or long form)
    translated_kwargs = {}
    for key, value in kwargs.items():
        if key in arg_map:  # short form
            translated_kwargs[arg_map[key]['name']] = value
        elif any(data['name'] == key for data in arg_map.values()):  # long form
            translated_kwargs[key] = value
        else:
            print(f"Warning: Key \'{key}\' not recognized. Skipping...")
    return translated_kwargs


def refresh_arg_lib():
    print("preparing to run")
    file_path = os.path.dirname(os.getcwd()) + r"\info"
    lines_to_write = []
    lines_to_write.extend("arg_lib = {\n")
    for root, _dirs, files in os.walk(file_path):
        for file_name in files:
            if file_name.endswith("_arg_map.py"):
                name = file_name.split("_")[0]
                lines_to_write.extend(f"\"{name}\": {{\n")
                with open(os.path.join(root, file_name), "r") as r_file:
                    r_file.readline()  # Read and discard the first line
                    lines_to_write.extend(r_file.readlines()[0:-1:])
                if file_name == files[-1]:
                    lines_to_write.extend("}\n}\n")
                else:
                    lines_to_write.extend("},\n")

    with open(os.path.join(file_path, "arg_lib.py"), "w") as w_file:
        w_file.write("".join(lines_to_write))
    print("Completed library refresh")


refresh_arg_lib()
