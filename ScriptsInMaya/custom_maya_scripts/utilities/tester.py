import maya.cmds as cmds
import os
from custom_maya_scripts.utilities.arg_map_utils import refresh_arg_lib
from custom_maya_scripts.components.window_base import WindowBase
from custom_maya_scripts.components.button_base import ButtonBase
from custom_maya_scripts.components.optionMenu_base import OptionMenuBase
from custom_maya_scripts.components.menuItem_base import MenuItemBase
from custom_maya_scripts.components.rowColumnLayout_base import RowColumnLayoutBase
from custom_maya_scripts.components.tabLayout_base import TabLayoutBase
from custom_maya_scripts.components.text_base import TextBase
from custom_maya_scripts.components.textfield_base import TextFieldBase
from custom_maya_scripts.components.tabLayout_base import TabLayoutBase


def perform_test():
    print("working")
    cmds.polyCube()


def run_arg_refresh():
    refresh_arg_lib()


test_ = MenuItemBase("test class")
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
