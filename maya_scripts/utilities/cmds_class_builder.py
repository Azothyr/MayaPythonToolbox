"""
Script to automate the creation of Maya commands base classes and their associated argument maps.

last update: 2023-09-12
"""
import os
from maya_scripts.utilities import arg_map_utils as map_handler
from script_tools.components.custom_exception import CustomException
from script_tools.functions.file_tools import read_from_file as reader


def _get_data_from_file(src):
    """
    Parse data from the provided source file. It especially handles multi-line records enclosed in
    parentheses and returns a processed list of these records.

    Expected input file format: if desired output for one line spans multiple lines, code expects that the first
    line will start with a '(' and the last line will start with a ')' and that all lines in between will be merged to
    form one line.

    Args:
        src (str): Path to the source file.

    Returns:
        list: Processed records from the source file.
    """
    result = []
    buffer = ""
    inside_parenthesis = False
    file_contents = reader(src)

    with open(src, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            elif line.startswith("("):
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

    return _process_variables(result)


def _process_variables(text):
    """
    Process the extracted variable text and return organized data.

    Args:
        text (list): Raw extracted data.

    Returns:
        tuple: Organized long names, short names, types, properties, and descriptions.
    """
    prop_values = {
        "createqueryeditmultiuse": "Create|Query|Edit|Multi-use",
        "createqueryedit": "Create|Query|Edit",
        "createquerymultiuse": "Create|Query|Multi-use",
        "createeditmultiuse": "Create|Edit|Multi-use",
        "createquery": "Create|Query",
        "createedit": "Create|Edit",
        "queryedit": "Create|Edit",
        "createmultiuse": "Create|Multi-use",
        "create": "Create",
        "query": "Query",
        "edit": "Edit",
        "multiuse": "Multi-use"
    }

    items = []
    for idx, line in enumerate(text):
        parts = [item.strip() for item in line.split('\t')]
        if len(parts) < 3:
            if idx % 2 == 0:
                error_txt = (f"Error: Line {idx - 2} >>>'{text[idx - 2]}'<<<\n"
                             f"\n>>>\tThis line from the file is causing the error."
                             "If the description in the file spans multiple lines,"
                             "\n>>>\tmake sure to put a '(' at the start of the first"
                             " line and a ')' at the beginning of the last line"
                             "\n>>>\tof the description.")
                raise CustomException(error=error_txt, exit=True)
        else:
            items.append(parts)
    long_names, short_names = zip(*[name.replace(")", "").split('(') for name, _, _ in items])
    types = [type_.strip() for _, type_, _ in items]
    properties = [prop_values[property_.strip()] for _, _, property_ in items]
    descriptions = [desc.strip() for desc in text[1::2]]

    return long_names, short_names, types, properties, descriptions


def class_arg_map_creator(data):
    """
    Create an argument map and class map from the provided data.

    Args:
        data (tuple): Parsed long names, short names, types, properties, and descriptions.

    Returns:
        tuple: Argument map and class map.
    """
    long_names, short_names, types, properties, descriptions = data
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
                    temp.append("\"\n\t\t\"")
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


def write_to_specific_file(txt, ofp, ufp, handler_func, *handler_args, ):
    """
    Writes the given text to a specific file, handling duplicates and file creation if necessary.

    Args:
        txt (str): Text to write.
        ofp (str): Output file path.
        ufp (str): Update file path.
        handler_func (function): Function to handle the content generation.
        *handler_args: Variable list of arguments to be passed to handler_func.

    Returns:
        str: Status message indicating the outcome of the operation.
    """
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

        # Create directory if it doesn't exist
        directory = os.path.dirname(ofp)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(ofp, "w") as file:
            file.write(content)

        return "Completed"


def arg_map_handler(arg_map, cls):
    """
    Generates the content for the argument map file.

    Args:
        arg_map (dict): Argument map data.
        cls (tuple): Class name information.

    Returns:
        str: Generated content for the argument map file.
    """
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
    """
    Generates the content for the base class file.

    Args:
        txt (str): Template or information for the content.
        cls (tuple): Class name information.

    Returns:
        str: Generated content for the base class file.
    """
    class_name = cls[0][0].capitalize() + cls[0][1::] + cls[1].capitalize()
    lower_name = cls[0]
    content = [
        "import maya.cmds as cmds",
        f"from maya_scripts.info.{lower_name}_arg_map import {lower_name}_arg_map as _map_src",
        "from maya_scripts.components.maya_cmds_base import CmdsBase",
        f"\n\nclass {class_name}(CmdsBase):",
        "\tdef __init__(self, name, **kwargs):\n\t\tsuper().__init__(name)\n",
        "\tdef _get_arg_map(self):\n\t\treturn _map_src\n",
    ]
    return "\n".join(content)


def _check_duplicates(path, check_lyst):
    """
    Checks for duplicate lines in a file against a provided list.

    Args:
        path (str): Path to the file to check.
        check_lyst (list): List of lines to check for duplicates.

    Returns:
        tuple: Boolean indicating if duplicates were found, and a related message.
    """
    if not os.path.exists(path):
        return None, f"File {path} does not exist!"

    with open(path, "r") as file:
        lines = {line.strip() for line in file.readlines()}  # Convert to set

    duplicates = lines.intersection(set(check_lyst))

    if duplicates:
        return True, f"DUPLICATE FOUND->{', '.join(duplicates)}"
    return False, "No duplicates found"


def _create_file(file_path):
    """
    Creates an empty file at the given path.

    Args:
        file_path (str): Path where the file should be created.
    """
    with open(file_path, 'w'):
        pass
    print(f"File created at {file_path}")


def write_to_file(ofp, ufp, arg_items, class_items, name):
    """
    Write the generated content for argument maps and class attributes to respective files.

    Args:
        ofp (str): Base output file path.
        ufp (str): Update file path.
        arg_items (dict): Argument map items.
        class_items (dict): Class map items.
        name (str): Name for the class.

    Returns:
        str: Status message indicating the outcome of the operations.
    """
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

    return f"\n\n--- ARGUMENT MAP FILE: {arg_completion} --- CLASS ATTRIBUTE FILE: {class_completion} ---"


def main(output_file_path="", name=""):
    """
    Main function: reads Maya flags, processes the data, and writes the necessary files.

    Args:
        output_file_path (str, optional): Destination path for the output files. Defaults to an inferred path.
        name (str, optional): Name of the class to be generated. Defaults to "test".
    """
    src = os.path.expanduser("~\\Downloads\\mayaflags.txt")
    text_data = _get_data_from_file(src)
    if output_file_path == "":
        if "Demon" in os.path.expanduser("~"):
            output_file_path = "C:\\GitRepos\\MayaPythonToolbox\\maya_scripts\\maya_scripts\\"
        elif "zacst" in os.path.expanduser("~"):
            output_file_path = "/\\maya_scripts\\"
        else:
            raise ValueError("Must give an output file path")
    update_file_path = os.path.expanduser(f"~\\Documents\\maya\\customscripts\\maya_scripts\\")
    print(f"Output path = {output_file_path}\n")
    if name == "":
        name = "test"
    class_name = (name, "base")

    arg_map, class_map = class_arg_map_creator(text_data)

    result = write_to_file(output_file_path, update_file_path, arg_map, class_map, class_name)

    print(result)
    print(map_handler.refresh_arg_lib())


if __name__ == "__main__":
    main(input("Where would you like these files to output?\nPress enter for default...\n>>\t"),
         name=input("What will the name of this class be?\n>>\t"))
