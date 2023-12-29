from maya import cmds
from components.display_layer import LayerCmds

print_allowed = False


def print_list(list_to_print):
    to_print = "\n".join(list_to_print)
    print_if_allowed(f"{to_print}\n", print_allowed)


def print_if_allowed(message, allow=False):
    if allow:
        print(message)


class Main(LayerCmds):
    def __init__(self, mode: str = None, **kwargs):
        match mode.lower():
            case "geo": self.set_geo_layer()
            case "joint": self.set_joint_layer()
            case "ctrl": self.set_ctrl_layer()
            case _: raise ValueError(f"Invalid mode: {mode}\n Valid modes are: 'geo', 'joint', 'ctrl'")
       
    def set_geo_layer(self):
        selection = self.walk_up("mesh")
        print_list(selection)
        self.add_list_to_layer("Geo_Layer", object_list=selection)

    def set_joint_layer(self):
        # print_allowed = True
        def set_dynamic_display_order():
            # Define the layers in their desired priority
            layer_priority = [
                'MAIN_JOINT_LAYER',
                'RK_Jnt_Sub_Layer',
                'IK_Jnt_Sub_Layer',
                'FK_Jnt_Sub_Layer'
            ]

            # Collect existing displayOrders and sort them
            existing_orders = []
            for layer in layer_priority:
                if cmds.objExists(layer):
                    existing_order = cmds.getAttr(f"{layer}.displayOrder")
                    existing_orders.append(existing_order)
                else:
                    print_if_allowed(f"Warning: {layer} does not exist in the scene.", print_allowed)

            existing_orders.sort()

            # If the list is empty, we start our displayOrder from 1
            if not existing_orders:
                existing_orders = [0]

            # Set the new displayOrders based on priority
            for i, layer in enumerate(layer_priority):
                if cmds.objExists(layer):
                    new_order = existing_orders[0] + i + 1
                    cmds.setAttr(f"{layer}.displayOrder", new_order)

        exclude_list = ["COG", "Clav", "Pelvis", "Spine", "Head"]

        selection = cmds.ls(type="joint")
        ik_joints = []
        fk_joints = []
        rk_joints = []
        center_joints = []
        remaining_joints = []

        for joint in selection:
            if any(value in joint for value in exclude_list):
                print_if_allowed(f"Excluding {joint} from Joint_Layer.", print_allowed)
                center_joints.append(joint)
                self.add_object_to_layer(joint, "MAIN_JOINT_LAYER")
            elif "RK" in joint or "Hand" in joint or "Finger" in joint:
                print_if_allowed(f"Adding {joint} to RK_Jnt_Sub_Layer.", print_allowed)
                rk_joints.append(joint)
                self.connect_joint_layer(joint, "RK_Jnt_Sub_Layer")
            elif "IK" in joint:
                print_if_allowed(f"Adding {joint} to IK_Jnt_Sub_Layer.", print_allowed)
                ik_joints.append(joint)
                self.connect_joint_layer(joint, "IK_Jnt_Sub_Layer")
            elif "FK" in joint:
                print_if_allowed(f"Adding {joint} to FK_Jnt_Sub_Layer.", print_allowed)
                fk_joints.append(joint)
                self.connect_joint_layer(joint, "FK_Jnt_Sub_Layer")
            else:
                print_if_allowed(f"Adding {joint} to Joint_Layer.", print_allowed)
                remaining_joints.append(joint)
                self.add_object_to_layer(joint, "MAIN_JOINT_LAYER")

        print_if_allowed("\nCenter Joints:", print_allowed)
        print_list(center_joints)
        print_if_allowed("\nIK Joints:", print_allowed)
        print_list(ik_joints)
        print_if_allowed("\nFK Joints:", print_allowed)
        print_list(fk_joints)
        print_if_allowed("\nRK Joints:", print_allowed)
        print_list(rk_joints)
        print_if_allowed("\nRemaining Joints:", print_allowed)
        print_list(remaining_joints)

        set_dynamic_display_order()

    def set_ctrl_layer(self):
        selection = self.walk_up("nurbsCurve")
        print_list(selection)
        self.add_list_to_layer("Control_Layer", object_list=selection)


if __name__ == "__main__":
    Main("geo")
    Main("joint")
    Main("ctrl")
    cmds.select(clear=True)
    print("\n--------------------------------------- COMPLETED DUNDER RUN ---------------------------------------\n\n")