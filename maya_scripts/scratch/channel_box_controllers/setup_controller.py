import maya.cmds as cmds
from core.components.validate_cmds import exists_maya


def process_name(name: str) -> str:
    if not isinstance(name, str):
        raise ValueError(f"WARNING: {name} is not a string.")
    if "|" in name:
        name = name.split("|")[-1]
    if ":" in name:
        name = name.replace(":", "_")
    if name.startswith("_"):
        name = name[1:]
    if " " in name:
        name = name.replace(" ", "_")
    return name


def check_or_select(name):
    if not exists_maya.obj(name):
        sel_check = cmds.ls(sl=True)
        if sel_check:
            name = sel_check[0]
        else:
            raise ValueError(f"WARNING-visual divider creation: {name} does not exist.")
    return process_name(name)


def add_to_channel_box(src_node, attr, **kwargs):
    cmds.setAttr(f"{src_node}.{attr}", e=True, channelBox=True, **kwargs)


def add_attr(src_node, attr, **kwargs):
    suffix = kwargs.pop("suffix") if kwargs.get("suffix") else ""
    attr = process_name(attr)
    attr_lower = f"{attr.lower()}{suffix}"
    lock_bool = kwargs.pop("lock", False)

    kwargs["longName"] = attr_lower if not kwargs.get("longName") else kwargs.get("longName")
    kwargs["niceName"] = attr if not kwargs.get("niceName") else kwargs.get("niceName")
    kwargs["attributeType"] = 'float' if not kwargs.get("attributeType") else kwargs.get("attributeType")

    try:
        if not cmds.attributeQuery(attr_lower, node=src_node, exists=True):
            cmds.addAttr(
                src_node,
                **kwargs
            )
            add_to_channel_box(src_node, attr_lower, lock=lock_bool)
    except Exception as e:
        cmds.warning(e)


def create_attr_enum(src_node, attr, options, **kwargs):
    src_node = check_or_select(src_node)
    add_attr(src_node,
             attr,
             attributeType='enum',
             enumName=options,
             **kwargs
             )


def create_attr_visual_divider(src_node, attr, **kwargs):
    if kwargs.get("div_name"):
        name = kwargs.pop("div_name")
    else:
        name = ""
    count = int((30 - len(name)) / 2)
    name = "-" * count + name + "-" * count
    create_attr_enum(src_node,
                     attr,
                     attr.upper(),
                     niceName=name,
                     keyable=False,
                     lock=True,
                     suffix="_divider",
                     **kwargs
                     )


def create_attr_visual_enum(src_node, attr, **kwargs):
    create_attr_enum(src_node,
                     attr,
                     "HIDE:UNLOCKED:WIREFRAME:LOCKED",
                     keyable=True,
                     writable=True,
                     suffix="_vis_enum",
                     **kwargs
                     )


def create_attr_visual_toggle(src_node, attr, **kwargs):
    create_attr_enum(src_node,
                     attr,
                     "HIDE:SHOW",
                     keyable=True,
                     writable=True,
                     suffix="_vis_toggle",
                     **kwargs
                     )


def create_attr_float_toggle(src_node, attr, **kwargs):
    add_attr(
        src_node,
        attr,
        attributeType='float',
        min=0,
        max=1,
        keyable=True,
        writable=True,
        suffix="_float_toggle",
        **kwargs
    )


def create_from_list(divider_name, attr_list, type="", src_node="", **kwargs):
    if isinstance(type, str):
        type = [type]
    elif not isinstance(type, list):
        raise ValueError(f"WARNING-create_from_list: 'type' must be a string or list, got {type}.")
    div_name = kwargs.pop("div_name") if kwargs.get("div_name") else None

    for t in type:
        if t in ["vis_divider", "vis_toggle", "vis_enum", "float_toggle"]:
            if div_name:
                create_attr_visual_divider(src_node, divider_name, div_name=div_name)
            else:
                create_attr_visual_divider(src_node, divider_name, **kwargs)

        if t == "vis_toggle":
            for item in attr_list:
                create_attr_visual_toggle(src_node, item, **kwargs)
        if t == "vis_enum":
            for item in attr_list:
                create_attr_visual_enum(src_node, item, **kwargs)
        elif t == "float_toggle":
            for item in attr_list:
                create_attr_float_toggle(src_node, item, **kwargs)


def main1():
    """
    CONTROLS:
        face: controls the expression and eye control group's visibility
        body: controls the torso/body control group's visibility
        arms: controls the arm control group's visibility
        legs: controls the leg control group's visibility
    VISIBILITY:
        Geometry: controls the visibility of the geometry group
        Blendshapes: controls the visibility of the blendshapes group
        Joints: controls the visibility of the joints
    LOCK:
        Viewport Geometry: sets the selection state of the geometry group (connects to the overrideDisplayType
         attribute) Unlocked: Normal, Wireframe: Template, Locked: Reference
    """
    create_from_list(
        "visibility", ["Geometry", "Blendshapes", "Joints", "Controls"], "vis_enum", div_name="GLOBAL")
    create_attr_visual_divider("controls", "controls", div_name="SECTION")
    for value in ["Face", "Body", "Arms", "Legs"]:
        create_attr_visual_toggle(value, value)
    create_from_list(
        "rig", ["Twist"], "vis_enum", div_name="SYSTEM")
    for value in ["RK", "FK", "IK"]:
        create_attr_visual_toggle(value, value)


def main2():
    float_divs = {
        "IK_FK": ["IK FK Switch"],
        "stretch": ["Stretchiness"]
    }
    # Stretch_Type, "None:Both:Stretch:Squash" ENUM
    # space,
    #   Head:   "float:follow_neck 0:1" "float:orient_Neck -inf:inf"
    #   Eyes:   "World:Head"
    #   IK:     "World:Transform:COG:Clavicle"
    for key, value in float_divs.items():
        create_from_list(key, value, "float")


def test_main():
    create_attr_visual_divider("test", "TEST")
    create_attr_visual_toggle("test", "VIS_TEST1")


if __name__ == "__main__":
    # test_main()
    main1()
    # main2()
