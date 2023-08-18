import maya.cmds as cmds


class TextField:
    def __init__(self, label):
        self.label = label
        self.widget = None

    def create(self):
        self.widget = cmds.textField(label=self.label)

    def get_text(self):
        return cmds.textField(self.widget, query=True, text=True)
