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


def create_attr_visual_divider(attr_holder, attr_name):
    attr_holder = process_name(attr_holder)
    attr_name = process_name(attr_name)
    if not exists_maya.obj(attr_holder):
        sel_check = cmds.ls(sl=True)
        if sel_check:
            attr_holder = sel_check[0]
        else:
            raise ValueError(f"WARNING-visual divider creation: {attr_holder} does not exist.")
    if not cmds.attributeQuery(f"{attr_name}_divider", node=attr_holder, exists=True):
        cmds.addAttr(
            attr_holder,
            longName=f"{attr_name}_divider",
            niceName="-"*20,
            attributeType='enum',
            enumName=attr_name.upper(),
            keyable=False
        )
        cmds.setAttr(f"{attr_holder}.{attr_name}_divider", e=True, channelBox=True, lock=True)
    else:
        cmds.warning(f"WARNING-visual divider creation: {attr_name} already exists on {attr_holder}")


def create_attr_visual_toggle(attr_holder, attr_name):
    attr_holder = process_name(attr_holder)
    attr_name = process_name(attr_name)
    if not cmds.objExists(attr_holder):
        sel_check = cmds.ls(sl=True)
        if sel_check:
            attr_holder = sel_check[0]
        else:
            raise ValueError(f"WARNING-toggle visibility attribute creation: {attr_holder} does not exist.")
    if not cmds.attributeQuery(attr_name, node=attr_holder, exists=True):
        cmds.addAttr(
            attr_holder,
            longName=f"{attr_name}_vis_toggle",
            niceName=attr_name,
            attributeType='enum',
            enumName="HIDE:SHOW",
            keyable=True,
            writable=True
        )
        cmds.setAttr(f"{attr_holder}.{attr_name}_vis_toggle", e=True, channelBox=True, lock=False)
    else:
        cmds.warning(f"WARNING-toggle visibility attribute creation: {attr_name} already exists on {attr_holder}")


def create_attr_float_toggle(attr_holder, attr_name):
    attr_holder = process_name(attr_holder)
    attr_name = process_name(attr_name)
    if not cmds.objExists(attr_holder):
        sel_check = cmds.ls(sl=True)
        if sel_check:
            attr_holder = sel_check[0]
            attr_holder = process_name(attr_holder)
        else:
            raise ValueError(f"WARNING-toggle visibility attribute creation: {attr_holder} does not exist.")
    if not cmds.attributeQuery(attr_name, node=attr_holder, exists=True):
        cmds.addAttr(
            attr_holder,
            longName=f"{attr_name}_float_toggle",
            niceName=attr_name,
            attributeType='float',
            min=0,
            max=1,
            keyable=True,
            writable=True
        )
        cmds.setAttr(f"{attr_holder}.{attr_name}_float_toggle", e=True, channelBox=True, lock=False)
    else:
        cmds.warning(f"WARNING-toggle visibility attribute creation: {attr_name} already exists on {attr_holder}")


def create_


def create_from_list(divider_name, attr_list, type="visual", attr_holder=""):
    if type == "visual":
        create_attr_visual_divider(attr_holder, divider_name)
        for item in attr_list:
            create_attr_visual_toggle(attr_holder, item)
    elif type == "float":
        create_attr_visual_divider(attr_holder, divider_name)
        for item in attr_list:
            create_attr_float_toggle(attr_holder, item)


def create_attr_proxy(proxy_holder, holder_to_copy, attr_name):
    cmds.addAttr(
        proxy_holder,
        longName=attr_name,
        proxy=f"{holder_to_copy}.{attr_name}"
    )


def drawing_overrides_state(obj, state):
    if not exists_maya.obj(obj):
        raise ValueError(f"WARNING: {obj} does not exist.")
    if cmds.getAttr(f"{obj}.overrideEnabled") == state:
        return
    cmds.setAttr(f"{obj}.overrideEnabled", state)


def is_connected(driving_attr, recieving_attr):
    driver = driving_attr.split(".")[0]
    connection = recieving_attr.split(".")[0]
    driving_attr = driving_attr.split(".")[-1]
    recieving_attr = recieving_attr.split(".")[-1]
    if not exists_maya.attr(driver, driving_attr):
        raise ValueError(f"WARNING: {driving_attr} does not exist.")
    if not exists_maya.attr(connection, recieving_attr):
        raise ValueError(f"WARNING: {recieving_attr} does not exist.")
    return cmds.isConnected(driving_attr, recieving_attr)


def connect_display_type(driver, attr, connection):
    if not exists_maya.obj(driver):
        raise ValueError(f"WARNING: {driver} does not exist.")
    if not exists_maya.obj(connection):
        raise ValueError(f"WARNING: {connection} does not exist.")
    if not exists_maya.attr(driver, attr):
        raise ValueError(f"WARNING: {driver} does not have an {attr} attribute.")
    if not exists_maya.attr(connection, "overrideDisplayType"):
        raise ValueError(f"WARNING: {connection} does not have an overrideDisplayType attribute.")
    if not is_connected(f"{driver}.{attr}", f"{connection}.overrideDisplayType"):
        cmds.connectAttr(f"{driver}.{attr}", f"{connection}.overrideDisplayType", f=True)


def connect_visibility(obj, attr):
    if not exists_maya.obj(obj):
        raise ValueError(f"WARNING: {obj} does not exist.")
    if not exists_maya.attr(obj, attr):
        raise ValueError(f"WARNING: {obj} does not have an {attr} attribute.")
    if not is_connected(f"{obj}.{attr}", f"{obj}.visibility"):
        cmds.connectAttr(f"{obj}.{attr}", f"{obj}.visibility", f=True)


def attr_to_all_mesh_display_type(driver, attr, proxy=False):
    for mesh in cmds.ls(type="mesh"):
        drawing_overrides_state(mesh, 1)
        connect_display_type(driver, attr, mesh)
        if proxy:
            create_attr_proxy(mesh, driver, attr)


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
    vis_divs = {
        "controls": ["face", "body", "arms", "legs"],
        "visibility": ["Geometry", "Blendshapes", "Joints"],
        "debug": ["Rig System", "Skeleton"]
    }
    view_divs = {
        "lock": ["Viewport Geometry"],  # noqa MUST ENABLE DRAWING OVERRIDES
    }
    for key, value in vis_divs.items():
        create_from_list(key, value, "visual")


def test_main():
    create_attr_visual_divider("test", "TEST")
    create_attr_visual_toggle("test", "VIS_TEST1")


if __name__ == "__main__":
    # test_main()
    main1()

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
