import maya.cmds as cmds
from core.maya_managers.selection_manager import Select
from core.maya_managers.joint_manager import JointManager
from scratch.channel_box_controllers.connection_cmds import create_attr_proxy, connect_to_controller


def fetch_twist_system():
    sel_tool = Select(bypass=True)
    twist_joints: list = JointManager(get="twist", bypass=True)["twist"]["joints"]
    twist_grp = sel_tool.filter_selection(maya_object=["Limb_Twist_Grp"])
    twist_locators = sel_tool.filter_selection(maya_object=["aim_loc", "up_loc", "mid_loc", "pv_loc", "target_loc"])
    return twist_joints, twist_grp, twist_locators


def run_connecting_tool(driver, attr, proxy=False):
    joints, grps, locators = fetch_twist_system()
    for joint in joints:
        connect_to_controller(driver, joint, attr)
    for grp in grps:
        connect_to_controller(driver, grp, attr)
        if proxy:
            create_attr_proxy(grp, driver, attr)
    for locator in locators:
        connect_to_controller(driver, locator, attr)


def main():
    driver = "Transform_Ctrl" if cmds.objExists("Transform_Ctrl") else cmds.ls(sl=True)[0]
    if not driver:
        raise ValueError("No driver obj or selection provided.")
    # exit([attr for attr in cmds.listAttr(driver) if "_vis_enum" in attr])
    attr = [attr for attr in cmds.listAttr(driver) if "twist_vis_enum" in attr]
    # print(attr)
    if attr:
        attr = attr[0]
        # print(attr)
    else:
        raise ValueError(f"No twist_system_vis_enum attribute found for {driver}.")
    run_connecting_tool(driver, attr, proxy=True)


if __name__ == "__main__":
    main()
