import maya.cmds as cmds


class Button:
    def __init__(self, label, command):
        self.label = label
        self.command = command
        self.widget = None

    def create(self):
        self.widget = cmds.button(label=self.label, command=self.command)
