import maya.cmds as cmds
from core.components.validate_cmds import exists_maya


def exists_or_error(obj, func, attr=None, connection=None):
    if not exists_maya.obj(obj):
        raise ValueError(f"WARNING-{func}: {obj} does not exist.")
    if attr and not exists_maya.attr(obj, attr):
        raise ValueError(f"WARNING-{func}: {obj} does not have an {attr} attribute.")
    if connection and not exists_maya.attr(obj, connection):
        raise ValueError(f"WARNING-{func}: {obj} does not have an {connection} attribute.")


def create_attr_proxy(proxy_holder, holder_to_copy, attr_name):
    # print(f"proxy_holder: {proxy_holder} holder_to_copy: {holder_to_copy} attr_name: {attr_name}")
    exists_or_error(holder_to_copy, "create_attr_proxy", attr_name)
    if not exists_maya.obj(proxy_holder):
        raise ValueError(f"WARNING-create_attr_proxy-LINE(17): {proxy_holder} does not exist.")
    if not exists_maya.attr(proxy_holder, attr_name):
        cmds.addAttr(
            proxy_holder,
            longName=attr_name,
            proxy=f"{holder_to_copy}.{attr_name}"
        )


def drawing_overrides_state(obj, state):
    exists_or_error(obj, "drawing_overrides_state")
    if cmds.getAttr(f"{obj}.overrideEnabled") == state:
        return
    cmds.setAttr(f"{obj}.overrideEnabled", state)


def is_connected(driving_attr, recieving_attr):
    source = driving_attr.split(".")[0]
    desitination = recieving_attr.split(".")[0]
    src_attr = driving_attr.split(".")[-1]
    dest_attr = recieving_attr.split(".")[-1]

    exists_or_error(source, src_attr)
    exists_or_error(desitination, dest_attr)

    return cmds.isConnected(driving_attr, recieving_attr)


def connect_display_type(driver, attr, connection):
    exists_or_error(driver, "connect_display_type", attr)
    exists_or_error(connection, "connect_display_type", "overrideDisplayType")

    if not is_connected(f"{driver}.{attr}", f"{connection}.overrideDisplayType"):
        cmds.connectAttr(f"{driver}.{attr}", f"{connection}.overrideDisplayType", f=True)


def connect_visibility(driver, attr, connection):
    exists_or_error(driver, "connect_visibility", attr)
    exists_or_error(connection, "connect_visibility", "visibility")
    if not is_connected(f"{driver}.{attr}", f"{connection}.visibility"):
        cmds.connectAttr(f"{driver}.{attr}", f"{connection}.visibility", f=True)


def create_display_conditional(driver, attr):
    exists_or_error(driver, "create_display_conditional", attr)
    uniqifier = attr.split("_")[0]
    condition_node = f"{driver}_{uniqifier}_display_conditional"
    pma_node = f"{driver}_{uniqifier}_adj_to_display_type_PMA"

    driver_attr = f"{driver}.{attr}"

    driver_to_condition1 = f"{condition_node}.firstTerm"
    condition2_connection_from_driver_attr = f"{condition_node}.colorIfTrueR"

    driver_to_pma = f"{pma_node}.input2D[0].input2Dx"
    pma_output = f"{pma_node}.output2Dx"
    pma_to_condition = f"{condition_node}.colorIfTrueG"

    if not exists_maya.obj(condition_node):
        cmds.shadingNode("condition", asUtility=True, name=condition_node)
        cmds.setAttr(f"{condition_node}.secondTerm", 0)
        cmds.setAttr(f"{condition_node}.operation", 0)
    if not exists_maya.obj(pma_node):
        cmds.shadingNode("plusMinusAverage", asUtility=True, name=pma_node)
        cmds.setAttr(f"{pma_node}.operation", 2)
        cmds.setAttr(f"{pma_node}.input2D[1].input2Dx", 1)

    if not is_connected(driver_attr, driver_to_condition1):
        cmds.connectAttr(driver_attr, driver_to_condition1, f=True)
    if not is_connected(driver_attr, condition2_connection_from_driver_attr):
        cmds.connectAttr(driver_attr, condition2_connection_from_driver_attr, f=True)
    if not is_connected(driver_attr, driver_to_pma):
        cmds.connectAttr(driver_attr, driver_to_pma, f=True)
    if not is_connected(pma_output, pma_to_condition):
        cmds.connectAttr(pma_output, pma_to_condition, f=True)


if __name__ == "__main__":
    pass
