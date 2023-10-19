import maya.cmds as cmds
from collections import defaultdict
from functools import partial
import re


class JointManager:
    TYPES = {
        'ik': '_IK',
        'fk': '_FK',
        'rk': '_RK',
    }

    def __init__(self, selection=None, combine=True, get=None):
        self.selection = selection if selection is not None else cmds.ls(type="joint")
        self.combine = combine
        if get:
            if get.lower() not in ['fk', 'ik', 'rk']:
                raise ValueError(f"get must be one of 'fk', 'ik', or 'rk'. Got {get} instead.")
            self.selection = [joint for joint in self.selection if self.TYPES.get(get.lower()) in joint]
        self.splitter = [value for key, value in self.TYPES.items()]

        self.data = self.joint_count()

    def __repr__(self):
        output = []
        for joint_type, sub_dict in self.data.items():
            output.append(f"For {joint_type}:")
            for part, info in sub_dict.items():
                output.append(f"|--->  {part} appears {info['count']} times.\n|------->  Joints: {info['joints']}")
        return "\n".join(output)

    def _split(self, string):
        for delimiter in self.splitter:
            if delimiter in string:
                return string.split(delimiter)[0], delimiter[1:]  # Return both the prefix and the matching delimiter
        return None, None

    def joint_count(self):
        # Initialize a defaultdict of defaultdicts
        count_dict = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'joints': []}))
        if self.combine:
            pattern = re.compile(r'_[0-9]+$')  # Regular expression to remove numerical suffix

        for string in self.selection:
            part, joint_type = self._split(string)
            if part is None:
                part = string.split('_')[0]
                joint_type = "Unknown"

            if self.combine:
                part = pattern.sub('', part)

            count_dict[joint_type][part]['count'] += 1
            count_dict[joint_type][part]['joints'].append(string)

        return count_dict


class StretchyIkFactory:
    """
    This class will create a stretchy IK system for a given joint chain. It will create the necessary nodes and
    attributes to allow the user to control the stretchy IK system. It will also create the necessary locators to
    measure the distance between the base and tip joints.

    User Input:
        primary_side: The primary side of the rig. This will be used to determine which side of the rig to create the
                        stretchy IK system on. Default is "L" for left.
        **NOTE: The system is currently hard coded to work with rigs set up with the z positive axis as the forward
                direction with the expectation of joints mirrored over xy plane. This may be changed in the future t
                allow for more flexibility.
        AllowStretch: A custom attribute on the IK tip control that will allow the user to turn the stretchy IK on and
                        off. {0: off, 1: on}
        MaxStretch: A custom attribute on the IK tip control that will allow the user to set the maximum stretch
                        distance. Default is 3.
        AddStretchToEach: A custom attribute on the IK tip control that will allow the user to add stretch to each
                        segment of the IK chain. Default is 0.
        AddStretchToUpper: A custom attribute on the IK tip control that will allow the user to add stretch to the
                        upper segment of the IK chain. Default is 0.
        AddStretchToLower: A custom attribute on the IK tip control that will allow the user to add stretch to the
                        lower segment of the IK chain. Default is 0.
        MasterScale: A custom attribute on the Transform_Ctrl that will allow the user to scale the entire rig. Default
                        is 1.
    """

    def __init__(self, primary_side="L", reverse_side="R"):
        self.joint_manager = JointManager(combine=True, get='ik')
        self.ik_joints = self.joint_manager.data['IK'].items()
        self.primary_side = primary_side
        self.reverse_side = reverse_side
        self.include_reverse = False
        self.top_group = self._find_top_group()
        self.nodes = None
        self.part = None
        self.base_joint = None
        self.pv_joint = None
        self.tip_joint = None
        self.tip_ctrl = None
        self.base_ctrl = None

        self.run()
        if cmds.getAttr("IK_Dist_Loc_Grp.visibility") == 1:
            cmds.setAttr("IK_Dist_Loc_Grp.visibility", 0)
        print("-----__________------__________------__________COMPLETE__________------__________------__________-----")

    def __repr__(self):
        return f"StretchyIkFactory(\n\t{self.joint_manager}\n)"

    @staticmethod
    def create_node(node_type, name, **kwargs):
        cmds.shadingNode(node_type, name=name, **kwargs)

    @staticmethod
    def connect_attributes(source, from_attr, destination, to_attr, **kwargs):
        if not cmds.isConnected(f"{source}.{from_attr}", f"{destination}.{to_attr}"):
            cmds.connectAttr(f"{source}.{from_attr}", f"{destination}.{to_attr}", force=True, **kwargs)

    @staticmethod
    def set_attributes(host, attr, value, **kwargs):
        if cmds.attributeQuery(attr, node=host, exists=True):
            cmds.setAttr(f"{host}.{attr}", value, edit=True, keyable=True, **kwargs)

    def generate_nodes(self):
        nodes = {
            "reversed_nodes": {
                f"{self.part}_Mirror_Stretch_Axis_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                        partial(self.set_attributes, attr="input2X", value=-1),
                        partial(self.set_attributes, attr="input2Y", value=1),
                        partial(self.set_attributes, attr="input2Z", value=1),
                    ],
                    "reversed_connection": [
                        partial(self.connect_attributes, from_attr="outputX", to_attr="inputR",
                                destination=f"{self.part}_Stretch_Clamp"),
                    ],
                    "purpose": "Multiplies the stretch scalar factor by -1 to mirror the stretch on the reverse "
                               "side **NOTE: This is currently hard coded to work with rigs set up with the z positive "
                               "axis as the forward direction with the expectation of joints mirrored over xy plane.",
                },
            },
            "primary_nodes": {
                f"{self.part}_Input_Scale_Combined_PMA": {
                    "create": partial(self.create_node, node_type="plusMinusAverage", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="output2Dx", to_attr="input2X",
                                destination=f"{self.part}_Calculate_Segment_Stretch_MD"),
                        partial(self.connect_attributes, from_attr="output2Dy", to_attr="input2Y",
                                destination=f"{self.part}_Calculate_Segment_Stretch_MD"),
                    ],
                    "purpose": "Adds the Result of the Channel Box Input Scalar MD and seperated it to use in scaling "
                               "the upper and lower segments",
                },
                f"{self.part}_Set_Upper_Segment_Length_PMA": {
                    "create": partial(self.create_node, node_type="plusMinusAverage", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="output1D", to_attr="input1D[0]",
                                destination=f"{self.part}_Length_Denominator_PMA"),
                        partial(self.connect_attributes, from_attr="output1D", to_attr="input1X",
                                destination=f"{self.part}_Segment_Stretch_Result_MD"),
                    ],
                    "purpose": "Calculate the original distance between the Base and PV joint Segment, then add it and "
                               "it's scaled value together",
                },
                f"{self.part}_Set_Lower_Segment_Length_PMA": {
                    "create": partial(self.create_node, node_type="plusMinusAverage", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="output1D", to_attr="input1D[1]",
                                destination=f"{self.part}_Length_Denominator_PMA", ),
                        partial(self.connect_attributes, from_attr="output1D", to_attr="input1Y",
                                destination=f"{self.part}_Segment_Stretch_Result_MD"),
                    ],
                    "purpose": "Calculate the original distance between the PV and tip joint Segment, then add it and "
                               "it's scaled value together",
                },
                f"{self.part}_Length_Denominator_PMA": {
                    "create": partial(self.create_node, node_type="plusMinusAverage", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="output1D", to_attr="input2X",
                                destination=f"{self.part}_Total_Stretch_Scalar_MD"),
                    ],
                    "purpose": "Take the total length of the joint chain and divide it by the sum of the upper and "
                               "lower to get the stretch scalar factor",
                },
                f"{self.part}_Attempt_Stretch_Distance": {
                    "create": partial(self.create_node, node_type="distanceBetween", asUtility=True),
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="distance", to_attr="input1X",
                                destination=f"{self.part}_Scale_To_Global_Rig_MD"),
                    ],
                    "purpose": "Get the distance between the base and the tip locators, which the stretchy IK will "
                               "attempt to match",
                },
                f"{self.part}_Total_Stretch_Scalar_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=2),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputX", to_attr="inputR",
                                destination=f"{self.part}_Stretch_Clamp"),
                    ],
                    "reversed_connection": [
                        partial(self.connect_attributes, from_attr="outputX", to_attr="input1X",
                                destination=f"{self.part}_Mirror_Stretch_Axis_MD"),
                    ],
                    "purpose": "Calculates the stretch scalar factor by dividing the total length of the joint chain "
                               "by the scaled length of the upper and lower segments. This value will be mirrored for "
                               "the reverse side",
                },
                f"{self.part}_Allow_Stretch_Switch_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputX", to_attr="input1X",
                                destination=f"{self.part}_Total_Stretch_Scalar_MD"),
                    ],
                    "purpose": "Switch that will allow the stretchy IK to be turned on and off from the IK tip "
                               "control's custom attribute 'AllowStretch' 0: off, 1: on",
                },
                f"{self.part}_Segment_Stretch_Result_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputX", to_attr="translateX",
                                destination=f"{self.tip_joint}"),
                        partial(self.connect_attributes, from_attr="outputY", to_attr="translateX",
                                destination=f"{self.pv_joint}"),
                    ],
                    "purpose": "Calculates the final stretch length of the upper and lower segments by multiplying "
                               "scaled length of each by the clamped stretch value. Then sets the translateX of the "
                               "PV and Tip joints to the result. Thus stretching the IK chain.",
                },
                f"{self.part}_Ch_Box_Input_Scalar_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=2),
                        partial(self.set_attributes, attr="input2X", value=10),
                        partial(self.set_attributes, attr="input2Y", value=10),
                        partial(self.set_attributes, attr="input2Z", value=10),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputX", to_attr="input2D[0].input2Dx",
                                destination=f"{self.part}_Input_Scale_Combined_PMA"),
                        partial(self.connect_attributes, from_attr="outputX", to_attr="input2D[0].input2Dy",
                                destination=f"{self.part}_Input_Scale_Combined_PMA"),
                        partial(self.connect_attributes, from_attr="outputY", to_attr="input2D[1].input2Dx",
                                destination=f"{self.part}_Input_Scale_Combined_PMA"),
                        partial(self.connect_attributes, from_attr="outputZ", to_attr="input2D[1].input2Dy",
                                destination=f"{self.part}_Input_Scale_Combined_PMA"),
                    ],
                    "purpose": "Takes the input from the custom attributes in the IK tip control and combines them "
                               "by 10 to get a scale ratio.",
                },
                f"{self.part}_Calculate_Segment_Stretch_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                        partial(self.set_attributes, attr="input1X", value=cmds.getAttr(f"{self.pv_joint}.translateX")),
                        partial(self.set_attributes, attr="input1Y", value=cmds.getAttr(f"{self.tip_joint}.translateX"))
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputX", to_attr="input1D[1]",
                                destination=f"{self.part}_Set_Upper_Segment_Length_PMA"),
                        partial(self.connect_attributes, from_attr="outputY", to_attr="input1D[1]",
                                destination=f"{self.part}_Set_Lower_Segment_Length_PMA"),
                    ],
                    "purpose": "Multiplies the Segments by the scale ratio to get the stretch scalar factor",
                },
                f"{self.part}_Scale_To_Global_Rig_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=2),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputX", to_attr="input1X",
                                destination=f"{self.part}_Allow_Stretch_Switch_MD"),
                    ],
                    "purpose": "Multiplies the Attempt Stretch Distance to the global scale of the rig to get the "
                               "total distance the stretchy IK will attempt to match",
                },
                f"{self.part}_Stretch_Clamp": {
                    "create": partial(self.create_node, node_type="clamp", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="minR", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputR", to_attr="input2X",
                                destination=f"{self.part}_Segment_Stretch_Result_MD"),
                        partial(self.connect_attributes, from_attr="outputR", to_attr="input2Y",
                                destination=f"{self.part}_Segment_Stretch_Result_MD"),
                    ],
                    "purpose": "Set a clamp to prevent the stretch to go beyond Max and below Min",
                },
                f"{self.part}_IK_Dist_Base_Loc": {
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="worldMatrix", to_attr="inMatrix1",
                                destination=f"{self.part}_Attempt_Stretch_Distance"),
                    ],
                },
                f"{self.part}_IK_Dist_Tip_Loc": {
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="worldMatrix", to_attr="inMatrix2",
                                destination=f"{self.part}_Attempt_Stretch_Distance"),
                    ],
                    "purpose": "Used as the start position where the stretchy IK will attempt to match the distance "
                               "between the base and the tip locators",
                },
                f"{self.tip_ctrl}": {
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="AllowStretch",
                                destination=f"{self.part}_Allow_Stretch_Switch_MD", to_attr="input2X"),
                        partial(self.connect_attributes, from_attr="MaxStretch",
                                destination=f"{self.part}_Stretch_Clamp", to_attr="maxR"),
                        partial(self.connect_attributes, from_attr="AddStretchToEach",
                                destination=f"{self.part}_Ch_Box_Input_Scalar_MD", to_attr="input1X"),
                        partial(self.connect_attributes, from_attr="AddStretchToUpper",
                                destination=f"{self.part}_Ch_Box_Input_Scalar_MD", to_attr="input1Y"),
                        partial(self.connect_attributes, from_attr="AddStretchToLower",
                                destination=f"{self.part}_Ch_Box_Input_Scalar_MD", to_attr="input1Z"),
                    ],
                    "purpose": "Used as the end position where the stretchy IK will attempt to match the distance "
                               "between the base and the tip locators",
                },
                "Transform_Ctrl": {
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="MasterScale",
                                destination=f"{self.part}_Scale_To_Global_Rig_MD", to_attr="input2X"),
                    ],
                    "purpose": "Indicated the global scale of the rig",
                },
            },
        }
        return nodes

    @staticmethod
    def create_attributes(host, attr, attribute_type, **kwargs):
        if not cmds.attributeQuery(attr, node=host, exists=True):
            cmds.addAttr(host, longName=attr, attributeType=attribute_type, **kwargs)

    def generate_attributes(self):
        attributes = {
            "attributes": {
                "AllowStretch": {
                    "create": partial(self.create_attributes, host=self.tip_ctrl, attr="AllowStretch",
                                      attribute_type="float", min=0, max=1, defaultValue=0, readable=True,
                                      writable=True, keyable=True)
                },
                "MaxStretch": {
                    "create": partial(self.create_attributes, host=self.tip_ctrl, attr="MaxStretch",
                                      attribute_type="float", min=1, max=10, defaultValue=3, readable=True,
                                      writable=True, keyable=True)
                },
                "AddStretchToEach": {
                    "create": partial(self.create_attributes, host=self.tip_ctrl, attr="AddStretchToEach",
                                      attribute_type="float", min=-9.9, max=20, defaultValue=0, readable=True,
                                      writable=True, keyable=True)
                },
                "AddStretchToUpper": {
                    "create": partial(self.create_attributes, host=self.tip_ctrl, attr="AddStretchToUpper",
                                      attribute_type="float", min=-9.9, max=20, defaultValue=0, readable=True,
                                      writable=True, keyable=True)
                },
                "AddStretchToLower": {
                    "create": partial(self.create_attributes, host=self.tip_ctrl, attr="AddStretchToLower",
                                      attribute_type="float", min=-9.9, max=20, defaultValue=0, readable=True,
                                      writable=True, keyable=True)
                },
                "MasterScale": {
                    "create": partial(self.create_attributes, host="Transform_Ctrl", attr="MasterScale",
                                      attribute_type="float", defaultValue=1, readable=True, writable=True,
                                      keyable=True)
                },
            }
        }
        return attributes

    @staticmethod
    def _find_top_group():
        sel = cmds.ls(type="joint")[0]
        while cmds.listRelatives(sel, parent=True):
            sel = cmds.listRelatives(sel, parent=True)[0]
        return sel

    def create_dist_locators(self, base_position, tip_position):
        if not cmds.objExists("Deformers") or "Deformers" not in cmds.listRelatives(self.top_group, children=True):
            cmds.group(em=True, name="Deformers")
            cmds.parent("Deformers", self.top_group)
            cmds.group(em=True, name="IK_Dist_Loc_Grp")
            cmds.parent("IK_Dist_Loc_Grp", "Deformers")
        if "IK_Dist_Loc_Grp" not in cmds.listRelatives("Deformers", children=True):
            cmds.group(em=True, name="IK_Dist_Loc_Grp")
            cmds.parent("IK_Dist_Loc_Grp", "Deformers")
        base_locator = cmds.spaceLocator(name=f"{self.part}_IK_Dist_Base_Loc")
        tip_locator = cmds.spaceLocator(name=f"{self.part}_IK_Dist_Tip_Loc")
        cmds.xform(base_locator, translation=base_position, worldSpace=True)
        cmds.xform(tip_locator, translation=tip_position, worldSpace=True)
        cmds.parentConstraint(self.base_ctrl, base_locator, mo=True, name=f'{self.base_ctrl}_to_{base_locator}'
                                                                           f'_TRANSLATION_ROTATION__parent_constraint')
        cmds.parentConstraint(self.tip_ctrl, tip_locator, mo=True, name=f'{self.tip_ctrl}_to_{tip_locator}'
                                                                         f'_TRANSLATION_ROTATION__parent_constraint')
        cmds.parent(base_locator, tip_locator, "IK_Dist_Loc_Grp")
        return base_locator, tip_locator

    def run(self):
        for part, data in self.ik_joints:
            if "Foot" in part:
                continue
            self.part = part
            self.tip_ctrl = f"{self.part}_IK_Tip_Ctrl"
            self.base_ctrl = f"{self.part}_IK_Base_Ctrl"
            self.include_reverse = self.reverse_side in self.part
            found_01 = False
            found_02 = False
            found_03 = False
            for ik_joint in data['joints']:
                if not cmds.objExists(ik_joint):
                    raise ValueError(f"WARNING: {ik_joint} does not exist.")
                if not found_01 and not found_02 and not found_03:
                    self.base_joint = None
                    self.pv_joint = None
                    self.tip_joint = None
                if "01" in ik_joint:
                    self.base_joint = ik_joint
                    found_01 = True
                if "02" in ik_joint:
                    self.pv_joint = ik_joint
                    found_02 = True
                if "03" in ik_joint:
                    self.tip_joint = ik_joint
                    found_03 = True

            if self.base_joint and self.pv_joint and self.tip_joint:
                if self.pv_joint not in cmds.listRelatives(self.base_joint, children=True):
                    raise ValueError(f"WARNING: {self.pv_joint} is not a child of {self.base_joint}.")
                if self.tip_joint not in cmds.listRelatives(self.pv_joint, children=True):
                    raise ValueError(f"WARNING: {self.tip_joint} is not a child of {self.pv_joint}.")

            else:
                raise NotImplementedError(f"WARNING: {self.part} does not have all the required joints.")
            # print(f"CONFIRMED JOINTS OF {self.part} proceeding to create stretchy IK")

            self.create_dist_locators(cmds.xform(self.base_ctrl, query=True, translation=True, worldSpace=True),
                                      cmds.xform(self.tip_ctrl, query=True, translation=True, worldSpace=True))

            self.perform_attr_creation()

            self.perform_node_operations()

    def perform_attr_creation(self):
        attrs = self.generate_attributes()

        for attr in attrs:
            for host in attrs[attr]:
                attrs[attr][host]['create']()

    def perform_node_operations(self):
        _nodes = self.generate_nodes()

        def node_loop(pass_type, nodes, include_reverse=False):
            # print(f"RUNNNING PASS TYPE: {pass_type}")
            working_on = None
            for node_type, hosts in nodes.items():
                if working_on != node_type:
                    # print(f"WORKING ON {node_type} and reverse is {include_reverse} with global as "
                    #       f"{self.include_reverse}-----part is {self.part}")
                    working_on = node_type
                if not include_reverse and node_type == "reversed_nodes":
                    continue
                for host, details in hosts.items():
                    if pass_type == 'create' and details.get('create'):
                        # print(f"CREATING {host} by {details['create']}")
                        details['create'](name=host)
                    elif pass_type == 'set' and details.get('set'):

                        # Cannot set the input1D[0] attribute of the Calculate_Segment_Stretch Set_Lower_Segment and
                        # Set_Upper_Segment nodes directly. Must connect and disconnect it to the translateX of the PV
                        # and Tip joints respectively. Which will leave their translateX values in the input1D[0]
                        # attribute of the Set_Lower_Segment and Set_Upper_Segment nodes. DO NOT OVERWRITE THESE VALUES.
                        if "Set_Lower_Segment" in host:
                            print(f"SETTING {host} INPUT1D[0] to TIP JOINT: {self.tip_joint}'s translateX value "
                                  f"{cmds.getAttr(f'{self.tip_joint}.translateX')}")
                            cmds.connectAttr(f"{self.tip_joint}.translateX", f"{host}.input1D[0]", force=True)
                            cmds.disconnectAttr(f"{self.tip_joint}.translateX", f"{host}.input1D[0]")
                        if "Set_Upper_Segment" in host:
                            print(f"SETTING {host} INPUT1D[0] to PV JOINT: {self.pv_joint}'s translateX value "
                                  f"{cmds.getAttr(f'{self.pv_joint}.translateX')}")
                            cmds.connectAttr(f"{self.pv_joint}.translateX", f"{host}.input1D[0]", force=True)
                            cmds.disconnectAttr(f"{self.pv_joint}.translateX", f"{host}.input1D[0]")
                        if "Calculate_Segment_Stretch" in host:
                            print(f"SETTING {host} INPUT1X to PV JOINT: {self.pv_joint}'s translateX value "
                                  f"{cmds.getAttr(f'{self.pv_joint}.translateX')} and INPUT1Y to TIP JOINT: "
                                  f"{self.tip_joint}'s translateX value {cmds.getAttr(f'{self.tip_joint}.translateX')}")
                            cmds.connectAttr(f"{self.pv_joint}.translateX", f"{host}.input1X", force=True)
                            cmds.connectAttr(f"{self.tip_joint}.translateX", f"{host}.input1Y", force=True)
                            cmds.disconnectAttr(f"{self.pv_joint}.translateX", f"{host}.input1X")
                            cmds.disconnectAttr(f"{self.tip_joint}.translateX", f"{host}.input1Y")


                        for func in details.get('set'):
                            func(host=host)
                    elif pass_type == 'connect':
                        connection_type = 'reversed_connection' if include_reverse and details.get(
                            'reversed_connection') \
                            else 'primary_connection'
                        # print(f"CONNECTING {host} with {connection_type}")
                        for func in details.get(connection_type, []):
                            # if connection_type == 'reversed_connection':
                            #   print(f"CONNECTING {host} with {connection_type} by {func}")
                            func(source=host)

        # First pass: Create nodes
        node_loop('create', _nodes, self.include_reverse)

        # Second pass: Set attributes
        node_loop('set', _nodes, self.include_reverse)

        # Third pass: Make connections
        node_loop('connect', _nodes, self.include_reverse)


if __name__ == '__main__':
    if cmds.objExists("Joints") and not cmds.objExists("Skeleton"):
        cmds.rename("Joints", "Skeleton")

    if not cmds.attributeQuery("MasterScale", node="Transform_Ctrl", exists=True):
        cmds.addAttr("Transform_Ctrl", ln="MasterScale", at='float', dv=1)
        cmds.setAttr('Transform_Ctrl.MasterScale', e=True, keyable=True)
        cmds.connectAttr('Transform_Ctrl.MasterScale', "Transform_Ctrl.scaleX", force=True)
        cmds.connectAttr('Transform_Ctrl.MasterScale', "Transform_Ctrl.scaleY", force=True)
        cmds.connectAttr('Transform_Ctrl.MasterScale', "Transform_Ctrl.scaleZ", force=True)
        cmds.setAttr("Transform_Ctrl.scaleX", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("Transform_Ctrl.scaleY", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("Transform_Ctrl.scaleZ", lock=True, keyable=False, channelBox=False)
        cmds.scaleConstraint("Transform_Ctrl", "Skeleton", mo=True,
                             name='Transform_Ctrl_to_Skeleton_SCALE__scale_constraint', weight=1)

    joints = cmds.ls(type="joint")

    for joint in joints:
        cmds.setAttr(f"{joint}.segmentScaleCompensate", 0)

    StretchyIkFactory()
