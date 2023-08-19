import maya.cmds as cmds


class WindowBase:
    def __init__(self, window_name='default_window', **kwargs):
        self.window_name = window_name

        # Mapping from acronym to full argument name
        self.arg_mapping = {
            "t": "title",  # string
            "wh": "widthHeight",  # [int, int]
            "mb": "menuBar",  # boolean
            "mxb": "maximizeButton",  # boolean
            "mnb": "minimizeButton",  # boolean
            "bgc": "backgroundColor",  # [float, float, float]
            "rfc": "resizeToFitChildren",  # boolean
            "nde": "nestedDockingEnabled",  # boolean
            "p": "parent"  # string
        }

        # Translate kwargs keys if they are in arg_mapping
        for key in list(kwargs.keys()):
            if key in self.arg_mapping:
                kwargs[self.arg_mapping[key]] = kwargs.pop(key)

        # Set attributes
        self.title = kwargs.get("title", "Default Title")
        self.widthHeight = kwargs.get("widthHeight", (200, 100))
        self.menuBar = kwargs.get("menuBar", False)
        self.maximizeButton = kwargs.get("maximizeButton", False)
        self.minimizeButton = kwargs.get("minimizeButton", False)
        self.backgroundColor = kwargs.get("backgroundColor", [1, 1, 1])
        self.resizeToFitChildren = kwargs.get("resizeToFitChildren", False)
        self.nestedDockingEnabled = kwargs.get("nestedDockingEnabled", False)
        self.parent = kwargs.get("parent", None)

    def create(self):
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

        cmds.window(self.window_name,
                    title=self.title,
                    widthHeight=self.widthHeight,
                    menuBar=self.menuBar,
                    maximizeButton=self.maximizeButton,
                    minimizeButton=self.minimizeButton,
                    backgroundColor=self.backgroundColor,
                    resizeToFitChildren=self.resizeToFitChildren,
                    nestedDockingEnabled=self.nestedDockingEnabled,
                    parent=self.parent
                    )
