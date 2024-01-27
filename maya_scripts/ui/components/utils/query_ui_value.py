import maya.cmds as cmds


def query(name: str, type: str):
    """
    returns the value of a UI component based on its type.

    options: optionmenu, checkbox, radiobutton, textfield, floatfield, intfield, textscrolllist, text, rowcolumnlayout,
    columnlayout, framelayout, tablayout, formlayout, shelflayout, scrolllayout
    :param name: name of the UI component
    :param type: type of the UI component
    :return: value of the UI component
    """
    match type.lower():
        case var if var in ["optionmenu", "menu", "m"]:
            return cmds.optionMenu(name, query=True, value=True)
        case var if var in ["checkbox", "check", "c"]:
            return cmds.checkBox(name, query=True, value=True)
        case var if var in ["radiobuttongrp", "radiobutton", "radiogrp", "radio", "rbg", "rb"]:
            return cmds.radioButtonGrp(name, query=True, select=True)
        case var if var in ["textfield", "text", "t"]:
            return cmds.textField(name, query=True, text=True)
        case var if var in ["floatfield", "float", "f"]:
            return cmds.floatField(name, query=True, value=True)
        case var if var in ["intfield", "int", "i"]:
            return cmds.intField(name, query=True, value=True)
        case var if var in ["textscrolllist", "textlist", "tsl"]:
            return cmds.textScrollList(name, query=True, numberOfItems=True)
        case var if var in ["text", "txt", "t"]:
            return cmds.text(name, query=True, label=True)
        case var if var in ["rowcolumnlayout", "rowcolumn", "rcl"]:
            return cmds.rowColumnLayout(name, query=True, numberOfColumns=True)
        case var if var in ["columnlayout", "column", "cl"]:
            return cmds.columnLayout(name, query=True, numberOfColumns=True)
        case var if var in ["framelayout", "frame", "fl"]:
            return cmds.frameLayout(name, query=True, numberOfColumns=True)
        case var if var in ["tablayout", "tab", "tl"]:
            return cmds.tabLayout(name, query=True, numberOfColumns=True)
        case var if var in ["formlayout", "form", "f"]:
            return cmds.formLayout(name, query=True, numberOfColumns=True)
        case var if var in ["shelflayout", "shelf", "sl"]:
            return cmds.shelfLayout(name, query=True, numberOfColumns=True)
