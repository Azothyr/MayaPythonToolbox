import maya.cmds as cmds


class TextFieldBase:
    def __init__(self, name):
        self.name = name
        self.widget = None

    def create(self):
        self.widget = cmds.textField(name=self.name)

    def get_text(self):
        return cmds.textField(self.name, query=True, text=True)
