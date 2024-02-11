import maya.cmds as cmds
from core.maya_managers.selection_manager import Select
from scratch.channel_box_controllers.connection_cmds import (create_attr_proxy, connect_visibility,
                                                             connect_display_type, create_display_conditional,
                                                             drawing_overrides_state, is_connected)


def fetch_control_system():
    control_grp = Select(bypass=True).filter_selection(maya_object=["Controls"])
    ctrl_grp_children_grps = [grp for grp in cmds.listRelatives(control_grp, children=True, type="transform") if
                              "transform_ctrl" not in grp.lower()]
    controls = Select(bypass=True).filter_selection(control=True)
    if [ctrl for ctrl in controls if "transform_ctrl" in ctrl.lower()]:
        controls.remove([ctrl for ctrl in controls if "transform_ctrl" in ctrl.lower()][0])
    control_shapes = Select(controls).filter_to_shapes_from_base_object(controls)
    return ctrl_grp_children_grps, control_shapes


def connect_parent_grp_display_type_to_ctrl(driver, ctrl):
    drawing_overrides_state(ctrl, 1)
    if not is_connected(f"{driver}.overrideDisplayType", f"{ctrl}.overrideDisplayType"):
        cmds.connectAttr(f"{driver}.overrideDisplayType", f"{ctrl}.overrideDisplayType", f=True)


def connect_parent_Grp_to_controller(driver, obj, attr):
    uniqifier = attr.split("_")[0]
    condition_node = f"{driver}_{uniqifier}_display_conditional"
    pma_node = f"{driver}_{uniqifier}_adj_to_display_type_PMA"
    # exit(f"DRIVER: {driver}\nCONNECTING TO MAYA OBJECT: {obj}\nATTRIBUTE: {attr}\n"
    #      f"CONDITION NODE: {condition_node}\nPMA NODE: {pma_node}")

    drawing_overrides_state(obj, 1)
    if not cmds.objExists(condition_node) or not cmds.objExists(pma_node):
        create_display_conditional(driver, attr)
    connect_display_type(condition_node, "colorIfTrueG", obj)
    connect_visibility(condition_node, "colorIfTrueR", obj)


def run_connecting_tool(driver, enum_attr, proxy=False):
    top_ctrl_grp, controls = fetch_control_system()

    finger_in_hand = not bool([grp for grp in top_ctrl_grp if "finger" in grp.lower()])
    toe_in_foot = not bool([grp for grp in top_ctrl_grp if "toe" in grp.lower()])
    neck_in_head = not bool([grp for grp in top_ctrl_grp if "neck" in grp.lower()])

    for grp in top_ctrl_grp:
        connect_parent_Grp_to_controller(driver, grp, enum_attr)
        if proxy:
            create_attr_proxy(grp, driver, enum_attr)
        ctrl_section = grp.split("_")[0].lower()
        for ctrl in controls:
            if ctrl_section in ctrl.lower():
                connect_parent_grp_display_type_to_ctrl(grp, ctrl)
            if "arm" in ctrl_section.lower() and "clav" in ctrl.lower():
                connect_parent_grp_display_type_to_ctrl(grp, ctrl)
            if finger_in_hand:
                if "hand" in ctrl_section.lower() and "finger" in ctrl.lower():
                    connect_parent_grp_display_type_to_ctrl(grp, ctrl)

            if "leg" in ctrl_section.lower() and "clav" in ctrl.lower():
                connect_parent_grp_display_type_to_ctrl(grp, ctrl)
            if toe_in_foot:
                if "foot" in ctrl_section.lower() and "toe" in ctrl.lower():
                    connect_parent_grp_display_type_to_ctrl(grp, ctrl)

            if neck_in_head:
                if "head" in ctrl_section.lower() and "neck" in ctrl.lower():
                    connect_parent_grp_display_type_to_ctrl(grp, ctrl)


def main():
    driver = "Transform_Ctrl" if cmds.objExists("Transform_Ctrl") else cmds.ls(sl=True)[0]
    if not driver:
        raise ValueError("No driver obj or selection provided.")
    # exit([attr for attr in cmds.listAttr(driver) if "_vis_enum" in attr])
    attr = [attr for attr in cmds.listAttr(driver) if "controls_vis_enum" in attr]
    if attr:
        attr = attr[0]
        # exit(attr)
    else:
        raise ValueError(f"No twist_system_vis_enum attribute found for {driver}.")
    run_connecting_tool(driver, attr, proxy=True)


if __name__ == "__main__":
    main()
