import maya.cmds as cmds
# from utilities.arg_map_utils import refresh_arg_lib
from utilities.arg_lib_reader import LibReader


def perform_maya_test():
    print("working")
    cmds.polyCube()


def run_arg_refresh():
    refresh_arg_lib()


test_ = LibReader()
# test_.helper("nde")
# test_.helper("label")
# test_.helper("title")
# print(test_.visible_description)
# print(test_.vis_description)
# print(test_.w_description)
# print(test_.width_description)
# test_.helper("command")
# print(test_.arg_mapping)
# test_.helper("args")
# test_.helper("all")
