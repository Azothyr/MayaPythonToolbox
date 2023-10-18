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
        # attribute_to_create = self.CREATE_ON_INIT['attributes']['StretchSwitch']['create']
        # host_name = self.CREATE_ON_INIT['attributes']['StretchSwitch']['host'].format(self.part) if {} in\
        #     self.CREATE_ON_INIT['attributes']['StretchSwitch']['host'] else \
        #     self.CREATE_ON_INIT['attributes']['StretchSwitch']['host']
        # attribute_to_create(host=host_name)

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
                f"{self.part}_IK_Stretch_Negative_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                        partial(self.set_attributes, attr="input2X", value=-1),
                    ],
                    "reversed_connection": [
                        partial(self.connect_attributes, source=f"{self.part}_IK_Stretch_Negative_MD",
                                from_attr="outputX", destination=f"{self.part}_IK_Stretch_Clamp",
                                to_attr="inputR"),
                    ],
                    "purpose": "Reverse the stretch scalar factor for the reverse side",
                },
            },
            "primary_nodes": {
                f"{self.part}_Upper_Length_PMA": {
                    "create": partial(self.create_node, node_type="plusMinusAverage", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                        partial(self.set_attributes, attr="input1D[0]",
                                value=cmds.getAttr(f"{self.pv_joint}.translateX")),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, source=f"{self.part}_Upper_Length_PMA", from_attr="output1D",
                                destination=f"{self.part}_Length_Denominator_PMA", to_attr="input1D[0]"),
                        partial(self.connect_attributes, source=f"{self.part}_Upper_Length_PMA", from_attr="output1D",
                                destination=f"{self.part}_Joint_Length_MD", to_attr="input1X"),
                    ],
                    "purpose": "Calculate the distance between the base and the PV joint",
                },
                f"{self.part}_Lower_Length_PMA": {
                    "create": partial(self.create_node, node_type="plusMinusAverage", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                        partial(self.set_attributes, attr="input1D[0]",
                                value=cmds.getAttr(f"{self.tip_joint}.translateX")),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, to_attr="input1D[1]", from_attr="output1D",
                                destination=f"{self.part}_Length_Denominator_PMA", ),
                        partial(self.connect_attributes, to_attr="input1Y", from_attr="output1D",
                                destination=f"{self.part}_Joint_Length_MD"),
                    ],
                    "purpose": "Calculate the distance between the PV and the tip joint",
                },
                f"{self.part}_Length_Denominator_PMA": {
                    "create": partial(self.create_node, node_type="plusMinusAverage", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, to_attr="input1X", from_attr="output1D",
                                destination=f"{self.part}_IK_Stretch_Scalar_MD"),
                    ],
                    "purpose": "Take the total length of the joint chain and divide it by the sum of the upper and "
                               "lower to get the stretch scalar factor",
                },
                f"{self.part}_IK_Distance": {
                    "create": partial(self.create_node, node_type="distanceBetween", asUtility=True),
                    "primary_connection": [
                        partial(self.connect_attributes, to_attr="input1X", from_attr="distance",
                                destination=f"{self.part}_Stretch_Global_Scale_MD"),
                    ],
                    "purpose": "Get the distance between the base and the tip locators, which the stretchy IK will "
                               "attempt to match",
                },
                f"{self.part}_IK_Stretch_Scalar_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=2),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, to_attr="inputR", from_attr="outputX",
                                destination=f"{self.part}_IK_Stretch_Clamp"),
                    ],
                    "reversed_connection": [
                        partial(self.connect_attributes, to_attr="input1X", from_attr="outputX",
                                destination=f"{self.part}_IK_Stretch_Negative_MD", ),
                    ],
                    "purpose": "To scale the distance between the base and the tip locators to match the length of "
                               "the joint chain",
                },
                f"{self.part}_Stretch_Switch_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, to_attr="input1X", from_attr="outputX",
                                destination=f"{self.part}_IK_Stretch_Scalar_MD"),
                    ],
                    "purpose": "",
                },
                f"{self.part}_Joint_Length_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputX", to_attr="translateX",
                                destination=f"{self.pv_joint}"),
                        partial(self.connect_attributes, from_attr="outputY", to_attr="translateX",
                                destination=f"{self.tip_joint}"),
                    ],

                    "purpose": "",
                },
                f"{self.part}_Segment_Scalar_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=2),
                        partial(self.set_attributes, attr="input2X", value=10),
                        partial(self.set_attributes, attr="input2Y", value=10),
                        partial(self.set_attributes, attr="input2Z", value=10),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, to_attr="input1X", from_attr="outputX",
                                destination=f"{self.part}_IK_Length_Combined_MD"),
                        partial(self.connect_attributes, to_attr="input1Y", from_attr="outputX",
                                destination=f"{self.part}_IK_Length_Combined_MD"),
                        partial(self.connect_attributes, to_attr="input2X", from_attr="outputY",
                                destination=f"{self.part}_IK_Length_Combined_MD"),
                        partial(self.connect_attributes, to_attr="input2Y", from_attr="outputZ",
                                destination=f"{self.part}_IK_Length_Combined_MD"),
                    ],
                    "purpose": "",
                },
                f"{self.part}_IK_Length_Combined_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputX", to_attr="input2X",
                                destination=f"{self.part}_IK_Joint_Length_Ref_MD"),
                        partial(self.connect_attributes, from_attr="outputY", to_attr="input2Y",
                                destination=f"{self.part}_IK_Joint_Length_Ref_MD"),
                    ],
                    "purpose": "",
                },
                f"{self.part}_IK_Joint_Length_Ref_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=1),
                        partial(self.set_attributes, attr="input1X", value=cmds.getAttr(f"{self.pv_joint}.translateX")),
                        partial(self.set_attributes, attr="input1Y", value=cmds.getAttr(f"{self.tip_joint}.translateX"))
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputX",
                                destination=f"{self.part}_Upper_Length_PMA", to_attr="input1D[1]"),
                        partial(self.connect_attributes, from_attr="outputY",
                                destination=f"{self.part}_Lower_Length_PMA", to_attr="input1D[1]"),
                    ],
                    "purpose": "",
                },
                f"{self.part}_Stretch_Global_Scale_MD": {
                    "create": partial(self.create_node, node_type="multiplyDivide", asUtility=True),
                    "set": [
                        partial(self.set_attributes, attr="operation", value=2),
                    ],
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputX",
                                destination=f"{self.part}_Stretch_Switch_MD", to_attr="input1X"),
                    ],
                    "purpose": "",
                },
                f"{self.part}_IK_Stretch_Clamp": {
                    "create": partial(self.create_node, node_type="clamp", asUtility=True),
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="outputR",
                                destination=f"{self.part}_Joint_Length_MD", to_attr="input2X"),
                        partial(self.connect_attributes, from_attr="outputR",
                                destination=f"{self.part}_Joint_Length_MD", to_attr="input2Y"),
                    ],
                    "purpose": "Set a clamp to prevent the stretch to go beyond Max and below Min",
                },
                f"{self.part}_IK_Dist_Base_Loc": {
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="worldMatrix",
                                destination=f"{self.part}_IK_Distance", to_attr="inMatrix1"),
                    ],
                },
                f"{self.part}_IK_Dist_Tip_Loc": {
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="worldMatrix",
                                destination=f"{self.part}_IK_Distance", to_attr="inMatrix2"),
                    ],
                },
                f"{self.tip_ctrl}": {
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="StretchSwitch",
                                destination=f"{self.part}_Stretch_Switch_MD", to_attr="input2X"),
                        partial(self.connect_attributes, from_attr="MaxStretch",
                                destination=f"{self.part}_IK_Stretch_Clamp", to_attr="maxR"),
                        partial(self.connect_attributes, from_attr="TotalStretch",
                                destination=f"{self.part}_Segment_Scalar_MD", to_attr="input1X"),
                        partial(self.connect_attributes, from_attr="UpperStretch",
                                destination=f"{self.part}_Segment_Scalar_MD", to_attr="input1Y"),
                        partial(self.connect_attributes, from_attr="LowerStretch",
                                destination=f"{self.part}_Segment_Scalar_MD", to_attr="input1Z"),
                    ],
                },
                "Transform_Ctrl": {
                    "primary_connection": [
                        partial(self.connect_attributes, from_attr="MasterScale",
                                destination=f"{self.part}_Stretch_Global_Scale_MD", to_attr="input2X"),
                    ],
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
                "StretchSwitch": {
                    "create": partial(self.create_attributes, host=self.tip_ctrl, attr="StretchSwitch",
                                      attribute_type="float", min=0, max=1, defaultValue=0, readable=True,
                                      writable=True, keyable=True)
                },
                "MaxStretch": {
                    "create": partial(self.create_attributes, host=self.tip_ctrl, attr="MaxStretch",
                                      attribute_type="float", min=1, max=10, defaultValue=3, readable=True,
                                      writable=True, keyable=True)
                },
                "TotalStretch": {
                    "create": partial(self.create_attributes, host=self.tip_ctrl, attr="TotalStretch",
                                      attribute_type="float", min=-9.9, max=20, defaultValue=0, readable=True,
                                      writable=True, keyable=True)
                },
                "UpperStretch": {
                    "create": partial(self.create_attributes, host=self.tip_ctrl, attr="UpperStretch",
                                      attribute_type="float", min=-9.9, max=20, defaultValue=0, readable=True,
                                      writable=True, keyable=True)
                },
                "LowerStretch": {
                    "create": partial(self.create_attributes, host=self.tip_ctrl, attr="LowerStretch",
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
        cmds.parentConstraint(self.base_joint, base_locator, mo=True, name=f'{self.base_joint}_to_{base_locator}'
                                                                           f'_TRANSLATION_ROTATION__parent_constraint')
        cmds.parentConstraint(self.tip_joint, tip_locator, mo=True, name=f'{self.tip_joint}_to_{tip_locator}'
                                                                         f'_TRANSLATION_ROTATION__parent_constraint')
        cmds.parent(base_locator, tip_locator, "IK_Dist_Loc_Grp")
        return base_locator, tip_locator

    def run(self):
        for part, data in self.ik_joints:
            if "Foot" in part:
                continue
            self.part = part
            self.tip_ctrl = f"{self.part}_IK_Tip_Ctrl"
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

            self.create_dist_locators(cmds.xform(self.base_joint, query=True, translation=True, worldSpace=True),
                                      cmds.xform(self.tip_joint, query=True, translation=True, worldSpace=True))

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
            print(f"RUNNNING PASS TYPE: {pass_type}")
            working_on = None
            for node_type, hosts in nodes.items():
                if working_on != node_type:
                    print(f"WORKING ON {node_type} and reverse is {include_reverse} with global as {self.include_reverse}-----part is {self.part}")
                    working_on = node_type
                if not include_reverse and node_type == "reversed_nodes":
                    continue
                for host, details in hosts.items():
                    if pass_type == 'create' and details.get('create'):
                        # print(f"CREATING {host} by {details['create']}")
                        details['create'](name=host)
                    elif pass_type == 'set' and details.get('set'):
                        for func in details.get('set'):
                            func(host=host)
                    elif pass_type == 'connect':
                        connection_type = 'reversed_connection' if include_reverse and details.get(
                            'reversed_connection') \
                            else 'primary_connection'
                        # print(f"CONNECTING {host} with {connection_type}")
                        for func in details.get(connection_type, []):
                            # if connection_type == 'reversed_connection':
                                # print(f"CONNECTING {host} with {connection_type} by {func}")
                            func(source=host)

        # First pass: Create nodes
        node_loop('create', _nodes, self.include_reverse)

        # Second pass: Set attributes
        node_loop('set', _nodes, self.include_reverse)

        # Third pass: Make connections
        node_loop('connect', _nodes, self.include_reverse)

        # for node in _nodes:
        #     if not self.include_reverse and node == "reversed_nodes":
        #         continue
        #     for host in _nodes[node]:
        #         _nodes[node][host]['create'](name=host)
        #         if _nodes[node][host].get('set'):
        #             for func in _nodes[node][host]['set']:
        #                 func()
        #         if self.include_reverse and _nodes[node][host].get('reversed_connection'):
        #             for func in _nodes[node][host]['reversed_connection']:
        #                 func()
        #         else:
        #             if _nodes[node][host].get('primary_connection'):
        #                 for func in _nodes[node][host]['primary_connection']:
        #                     func()


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
