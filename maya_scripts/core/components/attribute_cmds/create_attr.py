import maya.cmds as cmds


def create(node, attr_name, attr_type=None, min_val=None, max_val=None, default_val=None):
    options = {
        "longName": attr_name,
        "attributeType": attr_type,
        "defaultValue": default_val,
        "minValue": min_val,
        "maxValue": max_val,
        "keyable": True,
    }
    if attr_type in ["float", "double", "int"]:
        if not min_val:
            options["minValue"] = 0
        if not max_val:
            options["maxValue"] = 1
        if not default_val:
            options["defaultValue"] = 0

    for key, val in options.items():
        if not val:
            del options[key]

    if not cmds.attributeQuery(attr_name, node=node, exists=True):
        cmds.addAttr(node, **options)
    else:
        raise RuntimeError(f"Attribute {attr_name} already exists on {node}")