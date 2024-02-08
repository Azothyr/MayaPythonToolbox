import maya.cmds as cmds
from core.maya_managers.selection_manager import Select
from core.maya_managers.joint_manager import JointManager
from scratch.channel_box_controllers.connection_cmds import (create_attr_proxy, connect_visibility,
                                                             connect_display_type, create_display_conditional,
                                                             drawing_overrides_state)


def fetch_joint_systems():
    exclude = ["spine", "cog", "pelvis", "clav", "hip", "root"]

    def process_joints(joints, add_from_list=None, add=False, remove=False):
        swap_fk_to_rk = ["finger", "toe", "hand"]
        result = []
        if remove:
            for jnt in joints:
                if not any(s in jnt.lower() for s in swap_fk_to_rk):
                    result.append(jnt)
        elif add:
            if not add_from_list:
                raise ValueError("No list provided to add from.")
            for jnt in add_from_list:
                for s in swap_fk_to_rk:
                    if s in jnt.lower():
                        result.append(jnt)
        return result

    sel_tool = Select(bypass=True)
    initial_fk_joints: list = [jnt for jnt in JointManager(get="fk", bypass=True)["FK"]["joints"]
                               if not any(s in jnt.lower() for s in exclude)]
    fk_joints: list = process_joints(initial_fk_joints, remove=True)
    ik_joints: list = JointManager(get="ik", bypass=True)["IK"]["joints"]
    rk_joints: list = JointManager(get="rk", bypass=True)["RK"]["joints"]
    rk_joints.extend(process_joints(rk_joints, add_from_list=initial_fk_joints, add=True))

    joint_parent = sel_tool.filter_selection(maya_object=["Skeleton"])
    return fk_joints, ik_joints, rk_joints, joint_parent


def run_connecting_tool(driver, data):
    parent_attr = data["parent"][0]
    if not isinstance(parent_attr, str):
        if isinstance(parent_attr, list):
            if len(parent_attr) > 1:
                raise ValueError(f"WARNING: {parent_attr} is not a string.")
            parent_attr = parent_attr[0]
    uniqifier = parent_attr.split("_")[0]
    condition_node = f"{driver}_{uniqifier}_display_conditional"
    pma_node = f"{driver}_{uniqifier}_adj_to_display_type_PMA"

    for node_type, connect_data in data.items():
        attr, nodes = connect_data
        if not isinstance(attr, str):
            if isinstance(attr, list):
                if len(attr) > 1:
                    raise ValueError(f"WARNING: {attr} is not a string.")
                attr = attr[0]
        if not isinstance(nodes, list):
            if isinstance(nodes, str):
                nodes = [nodes]
            else:
                raise ValueError(f"WARNING: {nodes} is not a list or string.")

        if node_type == "parent":
            for node in nodes:
                drawing_overrides_state(node, 1)
                if not cmds.objExists(condition_node) or not cmds.objExists(pma_node):
                    create_display_conditional(driver, attr)
                connect_display_type(condition_node, "colorIfTrueG", node)
                connect_visibility(condition_node, "colorIfTrueR", node)
                create_attr_proxy(node, driver, attr)
        else:
            for node in nodes:
                connect_visibility(driver, f"{node_type}_vis_toggle", node)


def main():
    driver = "Transform_Ctrl" if cmds.objExists("Transform_Ctrl") else cmds.ls(sl=True)[0]
    if not driver:
        raise ValueError("No driver obj or selection provided.")
    # exit([attr for attr in cmds.listAttr(driver) if "_vis_enum" in attr])
    parent_attr = [attr for attr in cmds.listAttr(driver) if "joints_vis_enum" in attr]
    rig_system_attrs = [attr for attr in cmds.listAttr(driver) if any(s in attr for s in ["fk_vis_toggle",
                                                                                          "ik_vis_toggle",
                                                                                          "rk_vis_toggle"])]
    ik_system_attr = [attr for attr in rig_system_attrs if "ik" in attr]
    fk_system_attr = [attr for attr in rig_system_attrs if "fk" in attr]
    rk_system_attr = [attr for attr in rig_system_attrs if "rk" in attr]

    # exit(f"parent_attr: {parent_attr} ik_system_attr: {ik_system_attr}"
    #      f" fk_system_attr: {fk_system_attr} rk_system_attr: {rk_system_attr}")

    if not parent_attr:
        raise ValueError(f"No joints_vis_enum attribute found for {driver}.")
    if not ik_system_attr:
        raise ValueError(f"No ik_vis_toggle attribute found for {driver}.")
    if not fk_system_attr:
        raise ValueError(f"No fk_vis_toggle attribute found for {driver}.")
    if not rk_system_attr:
        raise ValueError(f"No rk_vis_toggle attribute found for {driver}.")

    fk_sys, ik_sys, rk_sys, parent_node = fetch_joint_systems()

    data = {
        "parent": [parent_attr, parent_node],
        "fk": [fk_system_attr, fk_sys],
        "ik": [ik_system_attr, ik_sys],
        "rk": [rk_system_attr, rk_sys]
    }

    run_connecting_tool(driver, data)


if __name__ == "__main__":
    main()
