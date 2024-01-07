import maya.cmds as cmds
from core.components.validate_cmds.maya_existence import Exists as ex


def create_attr(node, attr_name, attr_type="float", min_val=0, max_val=1, default_val=0):
    if not cmds.attributeQuery(attr_name, node=node, exists=True):
        cmds.addAttr(node, longName=attr_name, attributeType=attr_type, defaultValue=default_val, minValue=min_val,
                     maxValue=max_val, keyable=True)
    else:
        raise RuntimeError(f"Attribute {attr_name} already exists on {node}")


def get_attr(_attr):
    if ex.obj(_attr):
        return cmds.getAttr(_attr)


def unlock_and_unhide(_attr):
    if ex.obj(_attr):
        cmds.setAttr(_attr, keyable=True)
        cmds.setAttr(_attr, channelBox=True)
        cmds.setAttr(_attr, lock=False)


def lock_and_hide(_attr):
    if ex.obj(_attr):
        cmds.setAttr(_attr, keyable=False)
        cmds.setAttr(_attr, channelBox=False)
        cmds.setAttr(_attr, lock=True)


def set_attr(_attr, value):
    if ex.obj(_attr):
        cmds.setAttr(_attr, value)


if __name__ == "__main__":
    attrs = [
        "translateX",
        "translateY",
        "translateZ",
        "scaleX",
        "scaleY",
        "scaleZ",
        "rotateX",
        "rotateY",
        "rotateZ",
        "visibility",
    ]

    objects = [
        "R_Weight_Target_Ctrl",
        "L_Weight_Target_Ctrl",
    ]

    for obj in objects:
        for attr in attrs:
            attr = f"{obj}.{attr}"
            print(get_attr(attr))
            # set_attr(attr, 0)
            # lock_and_hide(attr)
    print("\nDone")
