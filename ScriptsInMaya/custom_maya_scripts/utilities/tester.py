import maya.cmds as cmds
from custom_maya_scripts.components.button_base import ButtonBase


test_button = ButtonBase("test button", aop=False)
print(test_button.helper('actOnPress'))
print(test_button.actOnPress_property)
print(test_button.helper("all"))
print(test_button.helper("ARGS"))


def perform_test():
    print("working")
    cmds.polyCube()
