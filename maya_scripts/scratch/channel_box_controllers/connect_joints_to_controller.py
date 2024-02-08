import maya.cmds as cmds
from core.maya_managers.selection_manager import Select
from core.maya_managers.joint_manager import JointManager
from scratch.channel_box_controllers.connection_cmds import create_attr_proxy, connect_to_controller


def fetch_joint_systems():
    sel_tool = Select(bypass=True)
    fk_joints: list = JointManager(get="fk", bypass=True)["FK"]["joints"]
    ik_joints: list = JointManager(get="ik", bypass=True)["IK"]["joints"]
    rk_joints: list = JointManager(get="rk", bypass=True)["RK"]["joints"]
    joint_parent = sel_tool.filter_selection(maya_object=["Skeleton"])
    return fk_joints, ik_joints, rk_joints, joint_parent


def run_connecting_tool(driver, attr, nodes, proxy=False):
    if not isinstance(nodes, list):
        if isinstance(nodes, str):
            nodes = [nodes]
        else:
            raise ValueError(f"WARNING: {nodes} is not a list or string.")
    for obj in nodes:
        connect_to_controller(driver, obj, attr)
        if proxy:
            create_attr_proxy(obj, driver, attr)


def main():
    driver = "Transform_Ctrl" if cmds.objExists("Transform_Ctrl") else cmds.ls(sl=True)[0]
    if not driver:
        raise ValueError("No driver obj or selection provided.")
    # exit([attr for attr in cmds.listAttr(driver) if "_vis_enum" in attr])
    parent_attr = [attr for attr in cmds.listAttr(driver) if "joints_vis_enum" in attr]
    rig_system_attrs = [attr for attr in cmds.listAttr(driver) if attr in any(["fk_vis_toggle", "ik_vis_toggle",
                                                                               "rk_vis_toggle"]) in attr]
    ik_system_attr = [attr for attr in rig_system_attrs if "ik" in attr]
    fk_system_attr = [attr for attr in rig_system_attrs if "fk" in attr]
    rk_system_attr = [attr for attr in rig_system_attrs if "rk" in attr]
    # print(parent_attr)
    if parent_attr:
        parent_attr = parent_attr[0]
        # exit(attr)
    else:
        raise ValueError(f"No twist_system_vis_enum attribute found for {driver}.")
    fk_sys, ik_sys, rk_sys, parent_node = fetch_joint_systems()
    run_connecting_tool(driver, parent_attr, parent_node)
    run_connecting_tool(driver, ik_system_attr, ik_sys, proxy=True)
    run_connecting_tool(driver, fk_system_attr, fk_sys, proxy=True)
    run_connecting_tool(driver, rk_system_attr, rk_sys, proxy=True)



if __name__ == "__main__":
    main()
