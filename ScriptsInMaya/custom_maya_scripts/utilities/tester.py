import maya.cmds as cmds
from custom_maya_scripts.components.window_base import WindowBase
from custom_maya_scripts.components.button_base import ButtonBase
from custom_maya_scripts.components.optionMenu_base import OptionMenuBase


def perform_test():
    print("working")
    cmds.polyCube()


test_ = WindowBase("test class")
test_.helper("nde")
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
