import maya.cmds as cmds
from core.maya_managers.selection_manager import Select
from core.maya_managers.joint_manager import JointManager
from scratch.channel_box_controllers.connection_cmds import (create_attr_proxy, connect_visibility,
                                                             connect_display_type, create_display_conditional,
                                                             drawing_overrides_state, exists_or_error,)


def fetch_control_system():
    sel_tool = Select(bypass=True)
    control_grp = sel_tool.filter_selection(maya_object=["Controls"])
    return control_grp


def connect_to_controller(driver, obj, attr):

    uniqifier = attr.split("_")[0]
    condition_node = f"{driver}_{uniqifier}_display_conditional"
    pma_node = f"{driver}_{uniqifier}_adj_to_display_type_PMA"

    drawing_overrides_state(obj, 1)
    if not cmds.objExists(condition_node) or not cmds.objExists(pma_node):
        create_display_conditional(driver, attr)
    connect_display_type(condition_node, "colorIfTrueG", obj)
    connect_visibility(condition_node, "colorIfTrueR", obj)


def run_connecting_tool(driver, attr, proxy=False):
    top_ctrl_grp = fetch_control_system()
    for grp in top_ctrl_grp:
        connect_to_controller(driver, grp, attr)
        if proxy:
            create_attr_proxy(grp, driver, attr)


def main():
    driver = "Transform_Ctrl" if cmds.objExists("Transform_Ctrl") else cmds.ls(sl=True)[0]
    if not driver:
        raise ValueError("No driver obj or selection provided.")
    # exit([attr for attr in cmds.listAttr(driver) if "_vis_enum" in attr])
    attr = [attr for attr in cmds.listAttr(driver) if "controls_vis_enum" in attr]
    # print(attr)
    if attr:
        attr = attr[0]
        # print(attr)
    else:
        raise ValueError(f"No twist_system_vis_enum attribute found for {driver}.")
    run_connecting_tool(driver, attr, proxy=True)


if __name__ == "__main__":
    main()
