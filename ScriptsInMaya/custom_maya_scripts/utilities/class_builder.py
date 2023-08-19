import os


def _get_text_from_file(src):
    result = []
    buffer = ""
    inside_parenthesis = False

    with open(src, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("("):
                inside_parenthesis = True
                buffer += line
            elif line.startswith(")") and inside_parenthesis:
                buffer += ' ' + line
                result.append(buffer.replace("(", "").replace(")", ""))
                buffer = ""
                inside_parenthesis = False
            elif inside_parenthesis:
                buffer += ' ' + line
            else:
                result.append(line)

    # Catch any remaining items outside parenthesis
    if buffer:
        result.append(buffer)

    return result


def _process_variables(text):
    prop_values = {
        "createqueryedit": "C Q E",
        "createquery": "C Q",
        "createedit": "C E",
        "queryedit": "Q E",
        "create": "C",
        "query": "Q",
        "edit": "E"
    }

    items = []
    for line in text[::2]:
        parts = [item.strip() for item in line.split('\t')]
        if len(parts) < 3:
            print(f"Error: Line '{line}' does not have 3 tab-separated values.")
            continue
        items.append(parts)

    long_names, short_names = zip(*[name.replace(")", "").split('(') for name, _, _ in items])
    types = [type_.strip() for _, type_, _ in items]
    properties = [prop_values[property_.strip()] for _, _, property_ in items]
    descriptions = [desc.strip() for desc in text[1::2]]

    return long_names, short_names, types, properties, descriptions


def class_arg_map_creator(fp):
    long_names, short_names, types, properties, descriptions = _process_variables(_get_text_from_file(fp))
    arg_map = {}
    class_map = []

    for i in range(len(long_names)):
        temp = []
        long_name = long_names[i]
        short_name = short_names[i]
        ret_type = types[i]
        use_case = properties[i]
        description = descriptions[i]
        description = description.replace('"', '\\"')
        count = 0
        for ch in description:
            if count > 85:
                if ch == " ":
                    temp.append("\"\n\"")
                    count = 0
            temp.append(ch)
            count += 1
        description = "".join(temp)

        arg_map[short_name] = {
            "name": long_name,
            "description": description,
            "type": ret_type,
            "property": use_case
        }

    return arg_map, class_map


def write_to_specific_file(txt, ofp, ufp, handler_func, *handler_args):
    duplicate, problem = _check_duplicates(ufp, txt)
    if duplicate is None:
        print(problem)
        _create_file(ufp)
        return write_to_specific_file(txt, ofp, ufp, handler_func, *handler_args)
    elif duplicate is True:
        return problem
    else:
        print(problem, "in file.")
        content = handler_func(txt, *handler_args)

        with open(ofp, "w") as file:
            file.write(content)

        return "Completed"


def arg_map_handler(arg_map, cls):
    content = [f"{cls[0]}_arg_map = {{"]
    for short_name, attribute_data in arg_map.items():
        line = f"\t\"{short_name}\": {{\n"
        line += f"\t\t\"name\": \"{attribute_data['name']}\",\n"
        line += f"\t\t\"description\": \"{attribute_data['description']}\",\n"
        line += f"\t\t\"type\": \"{attribute_data['type']}\",\n"
        line += f"\t\t\"property\": \"{attribute_data['property']}\"\n"
        line += "\t},"
        content.append(line)
    content.append("}\n")
    return "\n".join(content)


def class_handler(txt, cls):
    class_name = cls[0].capitalize() + cls[1].capitalize()
    lower_name = cls[0]
    content = [
        "import maya.cmds as cmds",
        "import textwrap",
        f"from custom_maya_scripts.info.{lower_name}_arg_map import {lower_name}_arg_map as arg_map\n\n",
        f"class {class_name}:",
        "\tdef __init__(self, label, **kwargs):",
        "\t\tself.widget = None",
        "\t\tself.label = label",
        "\t\tself.arg_mapping = arg_map",
        "\n\t\t# Translate kwargs keys if they are in arg_mapping",
        "\t\tfor key in list(kwargs.keys()):",
        "\t\t\tif key in self.arg_mapping:",
        "\t\t\t\tname = self.arg_mapping[key]['name']",
        "\t\t\t\tkwargs[name] = kwargs.pop(key)",
        "\n\t\t# Set attributes",
        "\t\tself.set_attributes(**kwargs)",
        "\t\tself.create(**kwargs)",
        "\n\tdef set_attributes(self, **kwargs):",
        "\t\tfor key, value in self.arg_mapping.items():",
        "\t\t\tsetattr(self, value['name'], kwargs.get(value['name']))",
        "\t\t\tsetattr(self, f\"{value['name']}_description\", value.get('description'))",
        "\t\t\tsetattr(self, f\"{value['name']}_property\", value.get('property'))",
        "\t\t\tsetattr(self, f\"{value['name']}_type\", value.get('type'))"
    ] + txt + [
        "\n\tdef helper(self, attr):",
        "\t\tformatted_meta = []",
        "\t\tif str(attr).lower() == \"all\":",
        "\t\t\tfor k, v in self.arg_mapping.items():",
        "\t\t\t\tformatted_meta.append(f\"Name: {k} -> {v['name']} | Arg: {v['type']} |"
        " Use case: {v['property']}\\n\\tDescription: {textwrap.fill(v['description'], width=80)}\\n\")",
        "\t\t\treturn '\\n'.join(formatted_meta)",
        "\t\telif str(attr).lower() == \"args\":",
        "\t\t\tfor k, v in self.arg_mapping.items():",
        "\t\t\t\tformatted_meta.append(f\"Name: {k} -> {v['name']}\")\n",
        "\t\t\treturn '\\n'.join(formatted_meta)",
        "\t\telif attr in self.arg_mapping:",
        "\t\t\tsn = attr",
        "\t\t\tln = self.arg_mapping[attr]['name']",
        "\t\t\tdesc = self.arg_mapping[attr]['description']",
        "\t\t\ttyp = self.arg_mapping[attr]['type']",
        "\t\t\tprop = self.arg_mapping[attr]['property']",
        "\t\t\treturn f\"Name: {sn} -> {ln} | Arg: {typ} | Use case: {prop}"
        "\\n\\tDescription: {textwrap.fill(desc, width=80)}\\n\"",
        "\t\telse:",
        "\t\t\tfor k, v in self.arg_mapping.items():",
        "\t\t\t\tif attr == v['name']:",
        "\t\t\t\t\tsn = k",
        "\t\t\t\t\tln = attr",
        "\t\t\t\t\tdesc = v['description']",
        "\t\t\t\t\ttyp = v['type']",
        "\t\t\t\t\tprop = v['property']",
        "\t\t\t\t\treturn f\"Name: {sn} -> {ln} | Arg: {typ} | Use case: {prop}"
        "\\n\\tDescription: {textwrap.fill(desc, width=80)}\\n\"",
        "\t\treturn f\"Key {attr} was not found in Arg Map.\"",
        "\n\tdef create(self, **kwargs):",
        f"\t\tself.widget = cmds.{lower_name}(label=self.label, **kwargs)",
        "\n\tdef edit(self, **kwargs):",
        f"\t\tcmds.{lower_name}(self.widget, e=True, **kwargs)",
        "\n\tdef query(self, attribute):",
        f"\t\treturn cmds.{lower_name}(self.widget, q=True, **{{attribute: True}})\n"
    ]
    return "\n".join(content)


def _check_duplicates(path, check_lyst):
    if not os.path.exists(path):
        return None, f"File {path} does not exist!"

    with open(path, "r") as file:
        lines = {line.strip() for line in file.readlines()}  # Convert to set

    duplicates = lines.intersection(set(check_lyst))

    if duplicates:
        return True, f"DUPLICATE FOUND->{', '.join(duplicates)}"
    return False, "No duplicates found"


def _create_file(file_path):
    # Ensure directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w'):
        pass
    print(f"File created at {file_path}")


def write_to_file(ofp, ufp, arg_items, class_items, name):
    files = [f'info\\{name[0]}_arg_map.py', f'components\\{name[0]}_base.py']
    output_paths = []
    update_paths = []
    for file in files:
        output_paths.append(ofp + file)
        update_paths.append(ufp + file)

    arg_completion = write_to_specific_file(arg_items, output_paths[0], update_paths[0],
                                            arg_map_handler, name)
    class_completion = write_to_specific_file(class_items, output_paths[1], update_paths[1],
                                              class_handler, name)

    print(f"\n\n--- ARGUMENT MAP FILE: {arg_completion} --- CLASS ATTRIBUTE FILE: {class_completion} ---")


def main(output_file_path="", name=""):
    input_file_path = os.path.expanduser("~\\Downloads\\mayaflags.txt")
    if output_file_path == "":
        if "Demon" in os.path.expanduser("~"):
            output_file_path = "C:\\GitRepos\\MayaPythonToolbox\\ScriptsInMaya\\custom_maya_scripts\\"
        elif "zacst" in os.path.expanduser("~"):
            output_file_path = "C:\\Repos\\MayaPythonToolbox\\ScriptsInMaya\\custom_maya_scripts\\"
        else:
            raise ValueError("Must give an output file path")
    update_file_path = os.path.expanduser(f"~\\Documents\\maya\\customscripts\\custom_maya_scripts\\")
    print(f"Output path = {output_file_path}\n")
    if name == "":
        name = "default"
    class_name = (name, "base")

    arg_map, class_map = class_arg_map_creator(input_file_path)

    write_to_file(output_file_path, update_file_path, arg_map, class_map, class_name)


if __name__ == "__main__":
    main(input("Where would you like these files to output?"), input("What will the name of this class be?"))
