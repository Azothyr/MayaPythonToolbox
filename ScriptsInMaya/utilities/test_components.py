import unittest
import maya.cmds as cmds
import os
from custom_maya_scripts.utilities.arg_map_utils import refresh_arg_lib
from custom_maya_scripts.utilities.arg_lib_reader import LibReader
from custom_maya_scripts.components.window_base import WindowBase as Win
from custom_maya_scripts.components.button_base import ButtonBase as Button
from custom_maya_scripts.components.optionMenu_base import OptionMenuBase as OpMenu
from custom_maya_scripts.components.menuItem_base import MenuItemBase as MItem
from custom_maya_scripts.components.rowColumnLayout_base import RowColumnLayoutBase as RCLay
from custom_maya_scripts.components.tabLayout_base import TabLayoutBase as TabLay
from custom_maya_scripts.components.text_base import TextBase as Txt
from custom_maya_scripts.components.textField_base import TextFieldBase as TxtF


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
