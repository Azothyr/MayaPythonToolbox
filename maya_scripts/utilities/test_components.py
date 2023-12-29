import unittest
import maya.cmds as cmds
import os
# from utilities.arg_map_utils import refresh_arg_lib
from utilities.arg_lib_reader import LibReader
from ui.components.window_base import WindowBase as Win
from ui.components.button_base import ButtonBase as Button
from ui.components.optionMenu_base import OptionMenuBase as OpMenu
from ui.components.menuItem_base import MenuItemBase as MItem
from ui.components.rowColumnLayout_base import RowColumnLayoutBase as RCLay
from ui.components.tabLayout_base import TabLayoutBase as TabLay
from ui.components.text_base import TextBase as Txt
from ui.components.textField_base import TextFieldBase as TxtF


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
