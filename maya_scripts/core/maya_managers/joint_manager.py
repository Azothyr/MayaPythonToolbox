import maya.cmds as cmds
from pprint import pprint
from collections import defaultdict
import re
from core.maya_managers.selection_manager import Select as sl
"""
This seems to only manage counts and naming conventions for joints. With one method to duplicate and clean up a joint 
chain.
"""


class JointManager:
    class_allow_print = False
    TYPES = {
        'twist': 'Twist',
        'ik': 'IK',
        'fk': 'FK',
        'rk': 'RK',
        'helper': 'HELPER',
        'cog': 'COG',
    }

    def __init__(self, selection=None, combine=False, get=None, debug=False, bypass=False):
        """

        :param selection: list of joints to be analyzed
        :param combine: bool to combine joints with numerical suffixes
        :param get: str to filter the selection by joint type
        :param debug: bool to allow printing of instance
        :param kwargs:
        """
        self.instance_allow_print = debug
        self.selection = sl(bypass=True).filter_selection(joints=True) if not selection and bypass else \
            sl(selection).filter_selection(joints=True)
        self.combine = combine
        if get:
            if get.lower() not in self.TYPES.keys():
                raise ValueError(f"get must be one of {', '.join(self.TYPES)}. Got {get} instead.")
            self.selection = [
                joint for joint in self.selection if re.search(self.TYPES.get(get.lower()), joint, re.IGNORECASE)]
        self.splitter = [value.lower() for key, value in self.TYPES.items()]

        self.data = self.joint_count()

    def __repr__(self):
        return dict(self.data)

    def __str__(self):
        if self.combine:
            output = []
            for joint_type, info in self.data.items():
                output.append(f"For {joint_type} Joint Type:")
                output.append(
                    f"|\n|--->  {joint_type} Joints appear {info['count']} times.\n|------->  Joints: {info['joints']}")
                output.append("\n")
            return "\n".join(output)
        else:
            self.print_data()
            return ""

    def __getitem__(self, item):
        item_str = str(item)
        data = dict(self.data)
        for key in data.keys():
            if re.search(item_str, key, re.IGNORECASE):
                return data[key]
        raise KeyError(f"Key '{item}' not found.")

    def print_data(self):
        pprint(dict(self.data))

    def joint_count(self):
        """
        Count the number of joints in the selection and return a dictionary with the count and the joints

        :returns: Dictionary with the count and the joints
        """
        count_dict = defaultdict(lambda: {'count': 0, 'joints': []})
        if self.combine:
            pattern = re.compile(r"_[0-9]+$")  # Regular expression to remove numerical suffix

        for string in self.selection:
            joint_type = [x for x in re.split(f"_", string) if x.lower() in self.splitter][0]
            if joint_type is None:
                joint_type = "Unknown"

            if self.combine:
                string = pattern.sub('', string)

            count_dict[joint_type]['count'] += 1
            count_dict[joint_type]['joints'].append(string)
        return count_dict

    def get_part_names(self):
        exclude = ['helper', 'unknown']
        base_part = [x for x in self.data.keys() if x.lower() not in exclude]
        return base_part

    @staticmethod
    def recursive_joint_clean_till_parameter(node, until):
        finished = False
        children = cmds.listRelatives(node, children=True, path=True)
        if children is not None:
            for child in children:
                if until == child.split("|")[-1][1::]:
                    print(f"DELETING {child}")
                    cmds.select(child)
                    cmds.delete()
                    finished = True
                elif cmds.nodeType(child) != "joint":
                    # print(f"DELETING {child}")
                    cmds.delete(child)
                else:
                    name = child.split("|")[-1]
                    new_name = name.replace("_FK", "_RK")
                    cmds.select(child)
                    child = cmds.rename(new_name)
                    if finished:
                        return
                    node.recursive_joint_clean_till_parameter(child, until)


if __name__ == "__main__":
    def module_name():
        import inspect
        import os
        # Get the current frame and find the file name of the script
        frame = inspect.currentframe()
        filename = inspect.getfile(frame)
        return os.path.basename(filename).split('.')[0]


    print(f"{'-' * 10 + '|' + ' ' * 4} RUNNING {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 10}")
    # Example usage:
    # print(selection)
    manager = JointManager(bypass=True, combine=True, get="twist")
    manager.print_data()
    print(manager["twist"]["joints"])

    print(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 25}")
