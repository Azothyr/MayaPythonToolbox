import maya.cmds as cmds
from pprint import pprint, pformat
from collections import defaultdict
import re


class JointManager:
    class_allow_print = False
    TYPES = {
        'ik': '_IK',
        'fk': '_FK',
        'rk': '_RK',
        'helper': '_HELPER',
        'cog': 'COG',
    }

    def __init__(self, selection=None, combine=True, get=None, debug=False, **kwargs):
        self.instance_allow_print = debug
        self.selection = selection if selection is not None else cmds.ls(type="joint")
        self.combine = combine
        if get:
            if get.lower() not in self.TYPES.keys():
                raise ValueError(f"get must be one of {', '.join(self.TYPES)}. Got {get} instead.")
            self.selection = [joint for joint in self.selection if self.TYPES.get(get.lower()) in joint]
        self.splitter = [value for key, value in self.TYPES.items()]

        self.data = self.joint_count()

    def __repr__(self):
        output = []
        for joint_type, sub_dict in self.data.items():
            output.append(f"For {joint_type} Joint Type:")
            for part, info in sub_dict.items():
                output.append(f"|\n|--->  {part} appears {info['count']} times.\n|------->  Joints: {info['joints']}")
            output.append("\n")
        return "\n".join(output)

    def print_data(self):
        pprint(self.data)

    def _split(self, string):
        for delimiter in self.splitter:
            if delimiter in string:
                if delimiter == "COG":
                    return delimiter, delimiter
                else:  # Return both the prefix and the matching delimiter
                    return string.split(delimiter)[0], delimiter[1:]
        return None, None

    def joint_count(self):
        # Initialize a defaultdict of defaultdicts
        count_dict = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'joints': []}))
        if self.combine:
            pattern = re.compile(r'_[0-9]+$')  # Regular expression to remove numerical suffix

        for string in self.selection:
            part, joint_type = self._split(string)
            if part is None:
                part = string.split('_')[0]
                joint_type = "Unknown"

            if self.combine:
                part = pattern.sub('', part)

            count_dict[joint_type][part]['count'] += 1
            count_dict[joint_type][part]['joints'].append(string)

        return count_dict


if __name__ == "__main__":
    print(f"{'-' * 23 + '|' + ' ' * 4} Joint Manager {' ' * 4 + '|' + '-' * 22}")
    # Example usage:
    joints = JointManager(combine=True)
    print(joints)

    print(f"{'-' * 25 + '|' + ' ' * 4} Complete {' ' * 4 + '|' + '-' * 25}")