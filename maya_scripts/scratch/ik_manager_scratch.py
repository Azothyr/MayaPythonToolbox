import maya.cmds as cmds
from math import ceil
import re
from core.components.xform_handler import XformHandler, Calculator3dSpace
from core.maya_managers.control_manager import ControlManager
from core.components.error_handling import safe_select
from functools import partial


class IKFactory:
    def __init__(self, name: str, ik_joints: list[str] | list[object]):
        self.name = name
        self.part = None
        self.base_control: ControlManager
        self.pv_control: ControlManager
        self.tip_control: ControlManager
        self.base_group = None
        self.pv_group = None
        self.pv_offset_group = None
        self.pv_offset_xform = None
        self.tip_group = None
        self.handle = None

        if isinstance(ik_joints, str):
            ik_joints = [ik_joints]
        if not isinstance(ik_joints, list):
            raise ValueError(f"Expected a list of joints. Got {type(ik_joints)} instead.")
        self.joints = ik_joints
        self.count = len(ik_joints)

        self.base, self.pv, self.tip = self._parse_joints()
        self._update_part()
        self.base_xform = XformHandler(self.base, threshold=0.1, precision=1)
        self.pv_xform = XformHandler(self.pv, threshold=0.1, precision=1)
        self.tip_xform = XformHandler(self.tip, threshold=0.1, precision=1)
        self.offset_amount = self.__calculate_offset()

        self.base_control, self.pv_control, self.tip_control = self._parse_control_names_front()

        self._setup_scene()

    def __str__(self):
        return f"IKFactory: {self.name} - {self.base} - {self.pv} - {self.tip}"

    def __repr__(self):
        return self.name

    def __calculate_offset(self):
        from_base_calc = Calculator3dSpace(self.base_xform)
        from_tip_calc = Calculator3dSpace(self.tip_xform)
        upper_dist = from_base_calc.calculate_distance(other_xform=self.tip_xform)
        lower_dist = from_tip_calc.calculate_distance(other_xform=self.tip_xform)
        return self.base_xform.apply_threshold(abs((upper_dist + lower_dist) / 2 + (upper_dist + lower_dist) * 0.25))

    # def _confirm_straight(self):
    #     base_pos = self.base_xform.get_translation()
    #     pv_pos = self.pv_xform.get_translation()
    #     tip_pos = self.tip_xform.get_translation()
    #     base_pv = Calculator3dSpace(base_pos, pv_pos)
    #     pv_tip = Calculator3dSpace(pv_pos, tip_pos)
    #     base_tip = Calculator3dSpace(base_pos, tip_pos)
    #     return base_pv.distance + pv_tip.distance == base_tip.distance

    def _parse_joints(self):
        ik_joints = self.joints
        last_idx = self.count - 1
        mid_idx = ceil(last_idx / 2)
        base_joint = ik_joints[0]
        mid_joint = ik_joints[mid_idx]
        last_joint = ik_joints[-1]

        if not all(["ik" in joint.lower() for joint in ik_joints]):
            raise NameError(
                "IKFACTORY-LINE(50) --- "
                "The joints selected do not seem to be IK joints. It is recommended that you rename them to "
                f"reflect their function. {joints}")

        if "1" not in ik_joints[0]:
            cmds.warning(f"IKFACTORY-LINE(55) --- The base joint should be the first joint in the selection. "
                         f"CURRENT ORDER: {joints}")

        if self.count >= 2:
            if f"{last_idx+1}" not in last_joint:
                cmds.warning(
                    "IKFACTORY-LINE(61) --- The tip joint should be the last joint in the selection."
                    f" CURRENT ORDER: {joints}"
                )
            if self.count >= 3:
                if f"{mid_idx+1}" not in mid_joint:
                    cmds.warning(
                        "IKFACTORY-LINE(67) --- The pole vector joint should be the middle joint in the selection."
                        f" CURRENT ORDER: {joints}"
                    )
                return base_joint, mid_joint, last_joint
            else:
                return base_joint, None, last_joint
        else:
            raise ValueError(f"Expected at least 2 joints. Got {self.count} instead.")

    def _update_part(self):
        self.part = self._get_obj_part(self.base)
    
    @staticmethod
    def _get_obj_part(name):
        ik_pattern = re.compile(r"_ik", re.IGNORECASE)
        ik_pattern_num_start = re.compile(r"_[0-9][0-9]_ik", re.IGNORECASE)
        ik_pattern_num_end = re.compile(r"_ik_[0-9][0-9]", re.IGNORECASE)
        
        if ik_pattern_num_start.search(name):
            return ik_pattern_num_start.split(name)[0].strip()
        elif ik_pattern_num_end.search(name):
            return ik_pattern_num_end.split(name)[0].strip()
        else:
            return ik_pattern.split(name)[0].strip()

    def _parse_control_names_front(self):
        ik_pattern = re.compile(r"_ik", re.IGNORECASE)
        underscore_pattern = re.compile(r"_", re.IGNORECASE)

        if not ik_pattern.search(self.base):
            raise NameError("IKFACTORY-LINE(84) --- One of the joints does not have the expected naming convention."
                            f" {self.joints}")

        schema = underscore_pattern.split(self.part)[1]
        base_parts = f"{self.part} ik base"
        pv_parts = f"{self.part} ik pv"
        tip_parts = f"{self.part} ik tip"
        case = "lower"
        if not schema.islower():
            if schema.isupper():
                base_parts = base_parts.upper()
                pv_parts = pv_parts.upper()
                tip_parts = tip_parts.upper()
                case = "upper"
            elif schema.istitle():
                base_parts = base_parts.title()
                pv_parts = pv_parts.title()
                tip_parts = tip_parts.title()
                case = "title"
            else:
                base_parts = base_parts.capitalize()
                pv_parts = pv_parts.capitalize()
                tip_parts = tip_parts.capitalize()
                case = "mixed"

        if case != "lower":
            ik = re.compile(r"ik", re.IGNORECASE)
            base_parts = ik.sub("IK", base_parts)
            pv_parts = ik.sub("IK", re.sub("pv", "PV", pv_parts, flags=re.IGNORECASE))
            tip_parts = ik.sub("IK", tip_parts)

        base = base_parts.replace(" ", "_")
        pv = pv_parts.replace(" ", "_")
        tip = tip_parts.replace(" ", "_")

        return base, pv, tip

    def _setup_scene(self):
        if self.base_control and not cmds.objExists(self.base_control):
            self.base_control = ControlManager(self.base_control, create=True, m=self.base)
        if self.pv_control and not cmds.objExists(self.pv_control):
            self.pv_control = ControlManager(self.pv_control, create=True, m=self.pv)
        if self.tip_control and not cmds.objExists(self.tip_control):
            self.tip_control = ControlManager(self.tip_control, create=True, m=self.tip)

        if not isinstance(self.base_control, ControlManager):
            self.base_control: str
            self.base_control = ControlManager(self.base_control)
        if not isinstance(self.pv_control, ControlManager):
            self.pv_control: str
            self.pv_control = ControlManager(self.pv_control)
        if not isinstance(self.tip_control, ControlManager):
            self.tip_control: str
            self.tip_control = ControlManager(self.tip_control)

        self.controls = [self.base_control, self.pv_control, self.tip_control]

        if not self.base_group and self.base_control:
            self.base_group = self.base_control.group
        if not self.pv_group and self.pv_control:
            self.pv_group = self.pv_control.group
        if not self.tip_group and self.tip_control:
            self.tip_group = self.tip_control.group

        self._set_ctrls_in_heirarchy()

    def _set_ctrls_in_heirarchy(self):
        top_level_group = re.compile(r"^{}_ik_ctrl_grp$".format(self.part.lower()), re.IGNORECASE)

        for obj in cmds.ls(type="transform"):
            if top_level_group.search(obj):
                top_level_group = obj
                break
        if not cmds.objExists(top_level_group):
            return

        if self.base_group and self.pv_group:
            groups = [self.base_group, self.tip_group]
            if self.pv_group:
                groups.append(self.pv_group)

            for group in groups:
                if cmds.objExists(group):
                    cmds.parent(group, top_level_group)

    def create_ik(self, ik_type, **kwargs):
        cmds.select(clear=True)
        match ik_type:
            case "ik":
                self.create_ik_handle(kwargs.get("solver", "ikRPsolver"))
            case "pole":
                self.create_pole_vector()
            case "ik_chain":
                if not kwargs.get("size"):
                    raise ValueError("Expected a size for the ik chain. Got None instead.")
                self.execute_ik_chain(**kwargs)
            case _:
                pass

    def create_ik_handle(self, solver="ikRPsolver"):
        self.handle = cmds.ikHandle(startJoint=self.base, endEffector=self.tip, solver=solver,
                                    name=f"{self.part}_IK_Handle")[0]

    def create_pole_vector(self):
        cmds.poleVectorConstraint(self.pv_control.name, f"{self.part}_IK_Handle")

    def execute_ik_chain(self, size: int = 3, rot_axis="z", _continue=False):
        if not _continue:
            if size < 3:
                raise ValueError(f"Expected a size of 3 or more. Got {size} instead.")
            if not self.base_group or not self.pv_group or not self.tip_group:
                cmds.warning(f"Missing one or more control groups for IKFACTORY: {self.name}.")
            if not cmds.objExists(self.base) or not cmds.objExists(self.pv) or not cmds.objExists(self.tip):
                cmds.warning(f"Missing one or more joints for IKFACTORY in maya: {self.name}.")
            if not self.pv_offset_group and self.pv_control:
                cmds.select(clear=True)
                pv_offset_group = f"{self.part}_pv_offset_ctrl_grp"
                cmds.Group(pv_offset_group, empty=True)
                cmds.rename(self.pv_offset_group, f"{self.part}_pv_offset_ctrl_grp")
                self.pv_offset_xform = XformHandler(pv_offset_group, threshold=0.1, precision=1)
                self.pv_offset_xform.match_xform(self.pv_xform, ["translation", "rotation"])
                cmds.parent(pv_offset_group, self.pv_group)
                cmds.parent(self.pv_control.name, pv_offset_group)
                self.pv_offset_group = pv_offset_group

            rot_dir = 1
            if "-" in rot_axis:
                rot_axis = rot_axis.replace("-", "")
                rot_dir = -1
            if rot_axis not in ["x", "y", "z"]:
                raise ValueError(f"Expected a rotation axis of x, y, or z. Got {rot_axis} instead.")
            x_value = self.offset_amount * rot_dir if rot_axis == "x" else 0
            y_value = self.offset_amount * rot_dir if rot_axis == "y" else 0
            z_value = self.offset_amount * rot_dir if rot_axis == "z" else 0
            self.pv_offset_xform.add_in_local("translate", x=x_value, y=y_value, z=z_value)
            cmds.xform(self.pv_control.name, os=True, translation=(0, 0, 0), rotation=(0, 0, 0))

            self.continue_ui(_continue=True, size=size, rot_axis=rot_axis)
        else:
            self.create_ik("ik",)
            self.create_ik("pole")
            if not self.handle:
                raise ValueError(f"Failed to create an IK handle for {self.name}.")
            cmds.select(clear=True)
            cmds.parent(self.handle, self.tip_control.name)
            cmds.pointConstraint(self.base_control.name, self.base, maintainOffset=False)

            for control in self.controls:
                if control:
                    control = control.name
                    if "base" in control.lower() or "pv" in control.lower():
                        cmds.setAttr(f"{control}.rx", lock=True, channelBox=False, keyable=False)
                        cmds.setAttr(f"{control}.ry", lock=True, channelBox=False, keyable=False)
                        cmds.setAttr(f"{control}.rz", lock=True, channelBox=False, keyable=False)
                    cmds.setAttr(f"{control}.sx", lock=True, channelBox=False, keyable=False)
                    cmds.setAttr(f"{control}.sy", lock=True, channelBox=False, keyable=False)
                    cmds.setAttr(f"{control}.sz", lock=True, channelBox=False, keyable=False)
                    cmds.setAttr(f"{control}.v", lock=True, channelBox=False, keyable=False)

            cmds.setAttr(self.handle + ".v", 0)

    def continue_ui(self, **kwargs):
        passing_kwargs = kwargs
        cmds.select(self.pv_offset_group, replace=True)

        def execute(*_, **kwargs):
            self.execute_ik_chain(**kwargs)
            cmds.deleteUI("wait_for_response_ui", window=True)
        if cmds.window("wait_for_response_ui", exists=True):
            cmds.deleteUI("wait_for_response_ui", window=True)
        cmds.window("wait_for_response_ui", title="IK Factory", widthHeight=(10, 20), resizeToFitChildren=True)
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Please adjust the pivot offset group as needed and then click continue.", bgc=[0, 0, 0])
        cmds.button(label="Continue", bgc=[0.1, 0.3, 0.1], command=partial(execute, **passing_kwargs))
        cmds.showWindow("wait_for_response_ui")


if __name__ == "__main__":
    """
    steps for a 3 joint ik chain:
    3 joints in heirarchy must be completely straight
        (STRAIGHT = only the (primary axis) forward axis (I normally use the x-axis) on all 3 holds a translation value 
        with the base able to have tx ty and tz values as well as , the pv and tip have only tx. And their rotations 
        are 0 0 0 but their joint orient only has a value (secondary axis) rotation axis (I normally use the z-axis)
        with rotation values the others are 0)
    
    create 3 controls with groups
    a base (Ex: shoulder), a pole vector (Ex: elbow), and a tip (Ex: wrist)
    that have 3 primary groups (base and tip (parented: ctrl_grp > ctrl)
    with 1 offset group (PV gets an offset group (parented: ctrl_grp > offset_grp > ctrl))
    
    all control groups should match all transforms of their respective joints and carry those values
    while the controls themselves should have 0 0 0 for their transforms
    
    the pv offset grp should be moved along the rotation axis of the pv joint to the desired position
    (if it is an arm it is normally -rot axis and if it is a leg it is normally +rot axis)
    
    create an ik handle from base to tip joints
        SETTINGS:
            solver: Rotate-Plane Solver (ikRPsolver)
            name: <side>_<body part>_IK_Handle
            Autopriority: False
            Solver enable: True
            Snap enable: True
            Sticky: False
            Priority: 1
            Weight: 1
            POWeight: 1
            
    Point constrain the base control to the base joint (constrains tx ty tz)
    
    Pole vector constraint the pole vector control to the ik handle
        NOTE: if there is shifting in the chain when you execute the constraint, it is because your chain is not straight
    
    Parent the base, pv, and tip controls to their top level control group
    parent the ik handle to the tip control
    end heirarchy should look like:
        |-- <side>_<body part>_IK_ctrl_grp
            |-- <side>_<body part>_base_IK_ctrl_grp
                |-- <side>_<body part>_base_IK_ctrl
            |-- <side>_<body part>_pv_IK_ctrl_grp
                |-- <side>_<body part>_pv_IK_offsest_ctrl_grp
                    |-- <side>_<body part>_pv_IK_ctrl
            |-- <side>_<body part>_tip_IK_ctrl_grp
                |-- <side>_<body part>_tip_IK_ctrl
                    |-- <side>_<body part>_IK_Handle
            
    lock the following attributes on the controls:
        base: rx ry rz sx sy sz vis
        pv: rx ry rz sx sy sz vis
        tip: sx sy sz vis
    """
    def left_arm():
        cmds.select("L_Arm_IK_01_Jnt", replace=True)
        cmds.select("L_Arm_IK_02_Jnt", add=True)
        cmds.select("L_Arm_IK_03_Jnt", add=True)
        joints = cmds.ls(sl=True)
        l_arm = IKFactory("l_arm", joints)
        l_arm.create_ik("ik_chain", size=3, rot_axis="-y")

    def right_arm():
        cmds.select("R_Arm_IK_01_Jnt", replace=True)
        cmds.select("R_Arm_IK_02_Jnt", add=True)
        cmds.select("R_Arm_IK_03_Jnt", add=True)
        joints = cmds.ls(sl=True)
        r_arm = IKFactory("r_arm", joints)
        r_arm.create_ik("ik_chain", size=3, rot_axis="y")

    def left_leg():
        cmds.select("L_Leg_IK_01_Jnt", replace=True)
        cmds.select("L_Leg_IK_02_Jnt", add=True)
        cmds.select("L_Leg_IK_03_Jnt", add=True)
        joints = cmds.ls(sl=True)
        l_leg = IKFactory("l_leg", joints)
        l_leg.create_ik("ik_chain", size=3, rot_axis="-y")

    def right_leg():
        cmds.select("R_Leg_IK_01_Jnt", replace=True)
        cmds.select("R_Leg_IK_02_Jnt", add=True)
        cmds.select("R_Leg_IK_03_Jnt", add=True)
        joints = cmds.ls(sl=True)
        r_leg = IKFactory("r_leg", joints)
        r_leg.create_ik("ik_chain", size=3, rot_axis="y")

    # left_arm()
    # right_arm()
    # left_leg()
    # right_leg()

"""
cmds.select("L_Arm_RK_01_Jnt", replace=True)
cmds.select("R_Arm_RK_01_Jnt", add=True)
cmds.select("L_Leg_RK_01_Jnt", add=True)
cmds.select("R_Leg_RK_01_Jnt", add=True)

cmds.select("L_Arm_FK_01_Jnt", replace=True)
cmds.select("R_Arm_FK_01_Jnt", add=True)
cmds.select("L_Leg_FK_01_Jnt", add=True)
cmds.select("R_Leg_FK_01_Jnt", add=True)

cmds.select("L_Arm_IK_01_Jnt", replace=True)
cmds.select("R_Arm_IK_01_Jnt", add=True)
cmds.select("L_Leg_IK_01_Jnt", add=True)
cmds.select("R_Leg_IK_01_Jnt", add=True)
cmds.isolateSelect("modelPanel4", state=True)

cmds.select(clear=True)
cmds.isolateSelect("modelPanel4", state=False)
"""

"""
from collections import deque
import traceback
from traceback import FrameSummary
from typing import Type
import inspect
import re
from maya import cmds
from core.components.error_handling import safe_get_parent, safe_get_children

# This does not create IK joints but instead seems to be my attempt at getting the hierarchy of the selected objects
# for all the objects in the scene and maintain them through a tree queue structure.

debug_level = 0  # 0 - 10
style_presets = {
    "SECTION": {'div': ("|" + "~~" * 50 + "|\n"), 'add_div': True, 'header_function': True, 'section': True},
    "SECTION-END": {'div': ("\n|" + "/\\" * 50 + "|\n|" + "\\/" * 50 + "|"), 'add_end_div': True,
                    'footer_function': True, 'section_end': True},
    "SUBSECTION": {'div': ("|" + f"{' ' * 20}|" + "v" * 65 + "|\n"), 'add_div': True, 'header_function': True,
                   'subsection': True},
    "SUBSECTION-END": {'div': ("|" + f"{' ' * 20}|" + "^" * 65 + "|"), 'add_end_div': True, 'footer_function': True,
                       'subsection_end': True},
    "CONTAINER": {'div': (" " * 25 + "-" * 50 + "\n"), 'end_div': ("\n|" + " " * 25 + "-" * 50) * 1, 'add_div': True,
                  'add_end_div': True, 'header_function': True},
}


def debug_print(message, style=None, **kwargs):
    level = kwargs.get('level', 1)
    if level < debug_level:
        return

    def pretty_print_dict(d, indent=0, is_last_in_parent=True):
        lines = []
        keys = list(d.keys())
        for i, key in enumerate(keys):
            is_last = (i == len(keys) - 1)
            value = d[key]
            if isinstance(value, dict):
                if value:  # If the dictionary is not empty
                    lines.append("\t" * (indent + 1) + str(key) + ": " + pretty_print_dict(value, indent + 1, is_last))
                else:  # If the dictionary is empty
                    lines.append("\t" * (indent + 1) + str(key) + ": {}" + ("," if is_last else ""))
            else:
                lines.append("\t" * (indent + 1) + str(key) + ": " + str(value) + ("" if is_last else ","))

        closing_comma = "" if not is_last_in_parent else ","
        if lines:
            return "{\n" + "\n".join(lines) + "}" + closing_comma
        else:
            return "{}" + closing_comma

    def __get_traceback_line(__stack: traceback) -> str:
        return __stack.line

    def __get_traceback_file(__stack: traceback) -> str:
        return __stack.filename

    def __get_traceback_func(__stack: traceback) -> str:
        return __stack.name

    def __get_traceback_line_num(__stack: traceback) -> str:
        return __stack.lineno

    def __get_traceback_stack() -> dict[str, FrameSummary | str]:
        _result = {}
        __stack = traceback.extract_stack()[-3]
        _result['stack'] = __stack
        _result['line_num'] = __get_traceback_line_num(__stack)
        _result['function'] = __get_traceback_func(__stack)
        _result['file'] = __get_traceback_file(__stack)
        _result['line'] = __get_traceback_line(__stack)
        return _result

    stack = __get_traceback_stack()
    if style:
        kwargs.update(style_presets.get(style, {}))

    div = kwargs.get('div', "-")
    header = kwargs.get('header', stack['function'])
    footer = kwargs.get('footer', stack['function'])
    end_div = kwargs.get('end_div', div)

    if kwargs.get('to_format', None):
        data = kwargs.get('to_format')
        if isinstance(data, dict):
            result = pretty_print_dict(data)
        elif isinstance(data, list or tuple):
            if all(isinstance(item, float or int) for item in data):
                result = "[\n\t\t" + '\n\t\t'.join(
                    [f"X: {item[0]}, Y: {item[1]}, Z: {item[2]}" for item in data]) + "\n\t\t]"
            else:
                result = "[\n\t\t" + '\n\t\t'.join([f"{item}," for item in data]) + "\n\t\t]"
        else:
            result = data
        message = f"{message}\n\t\t{result}"

    if kwargs.get('add_div', False):
        message = f"{div}{message}"

    if kwargs.get('add_end_div', False):
        message = f"{message}{end_div}"

    if kwargs.get('footer', False) or kwargs.get('footer_function', False):
        if kwargs.get('footer_function', False):
            footer = f"|{' ' * (50 - (len(footer)))}{footer}.{stack['function']}".upper()
        if kwargs.get('section_end', False):
            header = f"{header}\n|{' ' * 41}END OF SECTION"
        if kwargs.get('subsection_end', False):
            header = f"{header}\n|{' ' * 41}END OF SUBSECTION"
        message = f"{message}\n|{footer}"

    if kwargs.get('header', False) or kwargs.get('header_function', False):
        if kwargs.get('header_function', False):
            header = f"|{' ' * (50 - (len(header)))}{header}.{stack['function']}".upper()
        if kwargs.get('section', False):
            header = f"{' ' * 41}START OF SECTION\n{header}"
        if kwargs.get('subsection', False):
            header = f"{' ' * 41}START OF SUBSECTION\n{header}"
        message = f"{header}\n{message}"

    if kwargs.get('add_function', False):
        message = f"\t{stack['function']}{message}"

    print(f"|{message}\n|--------File \"{stack['file']}\", line {stack['line_num']}, in {stack['function']}\n|")


class IkManager:
    def __init__(self, _selection=None, root_name="Joints", excluded_types=None, included_types=None,
                 root_type=None, _type=None, _all=False):
        debug_print("START OF IK MANAGER INITIALIZATION", style="SECTION", header="IkManager",
                    level=10)  # DEBUGGER
        if not excluded_types:
            excluded_types = [
                "parentConstraint", "pointConstraint", "orientConstraint", "scaleConstraint", "aimConstraint",
                "ikHandle", "ikEffector", "ikSolver", "ikRPsolver", "ikSCsolver", "ikSplineSolver", "ikSpringSolver",
                "nurbCircle", "nurbCurve", "nurbCylinder", "nurbPlane", "nurbSphere", "nurbSquare", "nurbTorus",

            ]
        self.__selector = MayaSelectionOperator(excluded_types=excluded_types,
                                                included_types=included_types,
                                                root=root_name)
        exit(f"EXIT LINE 139 --- {self.__selector}")
        self.selection = self.__selector.selection

        self.mapped_selection = self.__selector.map_hierarchy(self.selection)
        debug_print("IK MANAGER GETTING SELECTION IN MAYA SCENE", to_format=self.mapped_selection,
                    style="CONTAINER", header="IkManager", level=9)  # DEBUGGER

        self.tree = MayaObjectTree(self.mapped_selection, MayaObject)
        debug_print("IK MANAGER GETTING ALL SELECTED HIERARCHIES IN MAYA SCENE",
                    to_format=self.tree.nodes, style="CONTAINER", header="IkManager", level=9)  # DEBUGGER

        self.data = self.operation_data()
        debug_print("PROCESSED SELECTION TO:", to_format=self.data, style="CONTAINER", header="IkManager",
                    level=11)  # DEBUGGER

        debug_print("END OF IK MANAGER INITIALIZATION", style="SECTION", header="IkManager",
                    level=10)  # DEBUGGER

    def operation_data(self):
        debug_print("START OF OPERATION DATA", style="SECTION", header="IkManager",
                    level=10)
        # Get the selected objects
        # determine their type, and if they are valid

        # determine what joints will be the start and end of the ik chain
        # determine if they are in direct hierarchy of each other
        # if they are, set the start and end of the ik chain
        # if they are not, determine if they are 2 degrees of separation from each other
        # if they are set the start and end of the ik chain
        # if they are not, determine if they are 3 degrees of separation from each other
        # if they are in the parent direction but not the child direction, set the start and end of the ik chain
        # IK chain will always go away from the root

        # set them in a dictionary with the start and end of the ik chain
        # change their names to <prefix> + <name> + <suffix> IE:
        working_data = self.selection
        debug_print("END OF OPERATION DATA", style="SECTION", header="IkManager",
                    level=10)

        def _split_args(_args):
            # Split args into groups of 3 or less and return a list of lists
            _sets_3_or_less = []
            for i in range(0, len(_args), 3):
                _sets_3_or_less.append(_args[i:i + 3])
            return _sets_3_or_less

        def _de_tuple(_tuple, _update_list):
            if isinstance(_tuple, tuple):
                for item in _tuple:
                    _update_list.append(item)
                return _update_list
            else:
                raise Exception(f"Incorrect type given: {_tuple}")

        for _group in _split_args(working_data):
            if len(_group) == 3:
                debug_print(f"GROUP CONSIDERED TO BE A LENGTH OF 3: {_group}",
                            to_format=_group, style="CONTAINER", header="HierarchySorter", level=9)  # DEBUGGER
                _base, _pv, _tip = _group  # Unpack the group into variables
                # DEBUGGER
                # debug_print(f"Checking Hierarchy with BASE JOINT: {_base}, PV JOINT: {_pv}, TIP JOINT: {_tip}",
                #             level=10)
                # if __check_hierarchy(_base, _pv, _tip):
                #     _de_tuple(_group, final_processed_args)
                # else:
                #     raise Exception(f"Something went wrong during Checking Hierarchy with"
                #                     f" BASE JOINT: {_base}, PV JOINT: {_pv}, TIP JOINT: {_tip}", level=10)
            elif len(_group) < 3:
                if len(_group) == 2:
                    debug_print(f"GROUP CONSIDERED TO BE A LENGTH OF 2: {_group}",
                                to_format=_group, style="CONTAINER", header="HierarchySorter", level=9)
                    pass
                if len(_group) == 1:
                    debug_print(f"GROUP CONSIDERED TO BE A LENGTH OF 1: {_group}",
                                to_format=_group, style="CONTAINER", header="HierarchySorter", level=9)
                    pass
                else:
                    raise Exception("This Exception should never be raised."
                                    " _RelationshipManager__check_hierarchy is broken.")
            else:
                raise Exception(f"This Exception should never be raised. for some reason the group has more"
                                f" than 3 items. {_group}, {len(_group)}")

        debug_print("END OF OPERATION DATA", style="SECTION", header="IkManager", level=10)
        return working_data


class NameParser:
    def __init__(self, item: str):
        self.item = item

    def parse_string(self, split_symbol: str = "_", join_symbol: str = None, index: int = 0):
        parts = self.item.split(split_symbol)
        if len(parts) == 1:
            return parts[0]
        if index > len(parts):
            raise Exception(f"Index {index} is out of range for {self.item}")
        if index == 0 or join_symbol is None:
            return parts[index]
        else:
            return join_symbol.join(parts[index:]) if index == -1 else join_symbol.join(parts[index:])


class MayaSelectionOperator:
    selection = cmds.ls(sl=True)

    def __init__(self, excluded_types=None, included_types=None, _type=None, _all=False, **kwargs):
        debug_print("INITIALIZING SELECTION OPERATOR", style="SECTION", header="MayaSelectionOperator",
                    level=10)
        self.hierarchy = None

        if not excluded_types and _type:
            excluded_types = [x for x in cmds.ls(type=_type) if x != _type]
        self.excluded_types = excluded_types
        self.include_types = included_types
        self.forced_root = kwargs.get("root", None)

    def __str__(self):
        return f"\nMayaSelectionOperator: \n\tSELECTED: {self.selection}\n\tHIERRACHY: {self.hierarchy}"

    @staticmethod
    def generic_getter(func):
        def wrapper(self, _object, *args, **kwargs):  # noqa
            expected_args = len(inspect.signature(func).parameters)
            debug_print(f"GETTING: {func} FROM: MayaObject EXPECTS {expected_args} ARGS", level=1)

            # Check if the function expects just one argument, and call accordingly
            if expected_args == 1:
                debug_print(f"CALLING: {func} WITH 1 ARG: {_object}", level=1)
                return func(_object)
            else:
                debug_print(f"CALLING: {func} WITH ARGS: {_object}, {args}, {kwargs}", level=1)
                return func(_object, *args, **kwargs)

        return wrapper

    type_to_arg = {
        "joint": "joint",
        "control": "transform",
        "mesh": "mesh",
        "curve": "nurbsCurve",
        "transform": "transform",
        "all": {"all": True},
        "long": {"long": True},
    }

    @staticmethod
    def strip_path(value):
        return value[0].split("|")[-1] if isinstance(value, list) else value

    @staticmethod
    def __get_selection(_type=None, long=False, _all=False):
        if _type is not None:
            return cmds.ls(exactType=_type)
        else:
            return cmds.ls(sl=True, long=long) if _type is None else cmds.ls(sl=True, type=_type, long=long)

    def get(self, _type: object, _all: bool = False):
        debug_print(f"GETTING: {self.__get_selected_type(_type, _all=_all)}", style="CONTAINER",
                    header="SelectionOperator", level=5)  # DEBUGGER
        return self.__get_selected_type(_type, _all=_all)

    @staticmethod
    def select(item: str, clear=True, add=False, hierarchy=False, only=False, replace=False):
        if clear:
            cmds.select(cl=True)
        else:
            cmds.select(item, add=add, hi=hierarchy, noExpand=only, r=replace)

    def count(self, _type: object):
        return self.get_selected_type_count(_type)

    def __get_selected_type(self, _type=None, _all=None):
        arg = self.type_to_arg.get(_type, None)
        if arg is None:
            return None
        elif isinstance(arg, dict):
            return self.__get_selection(**arg)
        else:
            return self.__get_selection(arg, _all=_all)

    def get_selected_type_count(self, _type):
        arg = self.__get_selected_type(_type)
        if arg is None:
            return None
        else:
            return len(arg) if isinstance(arg, list) else 1

    def map_hierarchy(self, item_list: list | str):
        debug_print(f"MAPPING HIERARCHY OF: {item_list}", style="CONTAINER", header="MayaSelectionOperator",
                    level=5)

        def find_top_parent(_node: str):
            debug_print(f"PASSED: {_node}", header="MayaSelectionOperator", level=5)
            print(f"LINE 357 - object: {_node} of type: {cmds.objectType(_node)}".upper())
            if self.forced_root and _node == self.forced_root:
                debug_print(f"RETURNING: {_node} AS ROOT", header="MayaSelectionOperator", level=5)
                return _node
            if _node is None:
                debug_print(f"RETURNING: None AS ROOT", header="MayaSelectionOperator", level=5)
                return None
            if self.excluded_types:
                if cmds.objectType(_node) in self.excluded_types:
                    debug_print(f"RETURNING: None AS ROOT", header="MayaSelectionOperator", level=5)
                    return None
            if not cmds.objExists(_node):
                debug_print(f"RETURNING: None AS ROOT", header="MayaSelectionOperator", level=5)
                return None
            parent = cmds.listRelatives(_node, parent=True)
            return _node if parent is None else find_top_parent(self.strip_path(parent[0]))

        def get_hierarchy(_root):
            debug_print(f"GETTING HIERARCHY OF: {_root}", style="CONTAINER", header="MayaSelectionOperator",
                        level=5)
            issues = []
            _hierarchy = {}
            queue = deque([(_root, _hierarchy)])
            while queue:
                current, parent_dict = queue.popleft()
                try:
                    children = cmds.listRelatives(current, children=True) or []
                except ValueError as val_err:
                    debug_print(f"ERROR: {val_err}", level=5)
                    issues.append(val_err)
                    if "More than one" in str(val_err):
                        children = []
                    else:
                        raise val_err

                debug_print(f"CHILDREN OF: {current} ARE: {children}\n{current}'S SIBLINGS ARE {parent_dict}",
                            header="MayaSelectionOperator", level=5)
                parent_dict[current] = child_dict = {}
                for child in children:
                    if child is None or not cmds.objExists(child):
                        debug_print(f"SKIPPING: {child} BECAUSE IT DOES NOT EXIST", level=5)
                        continue
                    if self.excluded_types:
                        if cmds.objectType(child) in self.excluded_types:
                            debug_print(f"SKIPPING: {child} BECAUSE IT IS IN EXCLUDED TYPES", level=5)
                            continue
                    queue.append((child, child_dict))
            debug_print(f"HIERARCHY OF: {_root} IS: {_hierarchy}", style="CONTAINER",
                        header="MayaSelectionOperator", level=5)

            return _hierarchy

        result = {}
        if isinstance(item_list, str):
            item_list = [item_list]

        for item in item_list:
            if item is None:
                debug_print("NO ITEM PROVIDED TO TREE", level=6)
                raise Exception("No item or item list provided")

            if cmds.objExists(item):
                debug_print(f"INITIALIZING TREE WITH: {item}", level=4)
                root = find_top_parent(item)
            else:
                raise Exception(f"Item: {item} does not exist in scene")
            hierarchy = get_hierarchy(root)
            result[root] = hierarchy

        if len(result) > 1:
            result = {"multiple_roots": result}
        self.hierarchy = result
        return result


class TreeNode:
    _instances = {}

    def __new__(cls, identity, *args, **kwargs):
        if identity in cls._instances:
            return cls._instances[identity]
        instance = super(TreeNode, cls).__new__(cls)
        cls._instances[identity] = instance
        return instance

    def __init__(self, identity):
        self.children = None
        self._index = None
        self._identity = identity
        self._parent_node = None
        self._children_nodes = []

    def __repr__(self):
        return f"{self.__class__}({self._identity})"

    def __str__(self):
        return f"{self.__class__}({self._identity})"

    def __name__(self):
        return self._identity

    def __call__(self, *args, **kwargs):
        self.__init__(*args, **kwargs)
        return self._identity

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    @property
    def parent_node(self):
        return self._parent_node

    @parent_node.setter
    def parent_node(self, parent_node):
        self.add_parent(parent_node)

    @property
    def children_nodes(self):
        return self._children_nodes

    @children_nodes.setter
    def children_nodes(self, child_node):
        self.add_child(child_node)

    def add_parent(self, parent_node: 'TreeNode'):
        if parent_node is None:
            return None
        debug_print(f"ADDING PARENT: {parent_node} TO: {self._identity}", level=3)
        self._parent_node = parent_node
        parent_node.add_child(self)
        debug_print(f"PARENT OF {self._identity} IS {self._parent_node._identity}:\n", header="TreeNode", level=4)

    def remove_parent(self, parent_node: 'TreeNode'):
        debug_print(f"REMOVING PARENT: {parent_node} FROM: {self._identity}", level=3)
        self._parent_node = None
        parent_node.remove_child(self)

    def add_child(self, child_node: 'TreeNode'):
        if child_node is None:
            return None
        debug_print(f"ADDING CHILD: {child_node} TO: {self}", level=3)  # DEBUGGER
        self._children_nodes.append(child_node)
        child_node._parent_node = self
        debug_print(f"CHILDREN OF {self}:\n",
                    to_format=self._children_nodes, style="CONTAINER", header="TreeNode", level=4)  # DEBUGGER

    def remove_child(self, child_node: 'TreeNode'):
        debug_print(f"REMOVING CHILD: {child_node} FROM: {self}", level=3)  # DEBUGGER
        self._children_nodes.remove(child_node)
        child_node._parent_node = None
        debug_print(f"CHILDREN OF {self}:\n",
                    to_format=self._children_nodes, style="CONTAINER", header="TreeNode", level=4)  # DEBUGGER

    def get(self, param):
        pass


class MayaObject(TreeNode):

    @staticmethod
    def generic_getter(func):
        def wrapper(self, _object, *args, **kwargs):  # noqa
            try:
                # First, check if the object exists to avoid operations on non-existent objects
                if not cmds.objExists(_object):
                    raise ValueError(f"Object {_object} does not exist in the scene.")

                # Then, check if the object's name or type disqualifies it from the operation
                if re.search(r"shape", _object, re.IGNORECASE):
                    debug_print(f"Operation not applicable for shapes: {_object}", level=1)
                    return None  # or an appropriate default value

                # If passed all checks, proceed with the intended operation
                expected_args = len(inspect.signature(func).parameters)
                debug_print(f"GETTING: {func} FROM: MayaObject EXPECTS {expected_args} ARGS", level=1)

                if expected_args == 1:
                    debug_print(f"CALLING: {func} WITH 1 ARG: {_object}", level=1)
                    return func(_object)
                else:
                    debug_print(f"CALLING: {func} WITH ARGS: {_object}, {args}, {kwargs}", level=1)
                    return func(_object, *args, **kwargs)
            except (RuntimeError, ValueError):
                return None

        return wrapper

    def get_parent(self, _object):
        debug_print(f"GETTING PARENT OF: {self.name}", header="MayaObjectTree", level=2)  # DEBUGGER
        parent = safe_get_parent(_object)
        return self.strip_path(parent) if parent else None

    def get_children(self, _object):
        debug_print(f"GETTING CHILDREN OF: {self.name}", header="MayaObjectTree", level=2)  # DEBUGGER
        children = safe_get_children(_object)
        return self.strip_path(children) if children else None

    def center(self):
        debug_print(f"GETTING CENTER OF: {self.name}", header="MayaObjectTree", level=1)  # DEBUGGER
        bbox = self.get("bounding_box")
        return (
            (bbox[0] + bbox[3]) / 2,
            (bbox[1] + bbox[4]) / 2,
            (bbox[2] + bbox[5]) / 2
        )

    setters = {
        "world_position": generic_getter(lambda _object, xyz: cmds.xform(_object, ws=True, t=xyz)),
        "rotation": generic_getter(lambda _object: cmds.xform(_object, q=True, ws=True, ro=True)),
        "scale": generic_getter(lambda _object, _scale: cmds.xform(_object, ws=True, scale=_scale)),
        "parent": generic_getter(lambda _object, _parent: cmds.parent(_object, _parent)),
        "unparent": generic_getter(lambda _object: cmds.parent(_object, world=True)),
    }
    getters = {
        "type": generic_getter(lambda _object: cmds.objectType(_object)),
        "world_position": generic_getter(lambda _object: cmds.xform(_object, ws=True, q=True, t=True)),
        "rotation": generic_getter(lambda _object: cmds.xform(_object, q=True, ws=True, ro=True)),
        "scale": generic_getter(lambda _object: cmds.xform(_object, q=True, ws=True, scale=True)),
        "parent": lambda self, _object: self.get_parent(_object),
        "children": lambda self, _object: self.get_children(_object),
        "descendents": lambda _object: cmds.listRelatives(_object, allDescendents=True),
        "parents": lambda _object: cmds.listRelatives(_object, allParents=True),
        "shapes": lambda _object: cmds.listRelatives(_object, shapes=True),
        "object_exists": generic_getter(lambda _object: cmds.objExists(_object)),
        "bounding_box": lambda _object: cmds.exactWorldBoundingBox(_object),
        "center": generic_getter(lambda self: self.center()),
    }

    def __init__(self, name: str):
        if isinstance(name, list):
            name = self.strip_path(name)
        super().__init__(name)
        self.name = str(name)
        self.type = self.get("type")
        self.world_position = self.get("world_position")
        self.rotation = self.get("rotation")
        self.scale = self.get("scale")
        self.parent = self.get("parent")
        self.children = self.get("children")

    def __repr__(self):
        splitter = "- " * 8
        return (f'\n{splitter}CLASS INSTANCE: <MayaObject id={id(self)} name={self.name}>\n{splitter}'
                f'NAME: {self.name}\n{splitter}TYPE: {self.type}\n{splitter}WORLD POSITION: {self.world_position}'
                f'\n{splitter}ROTATION: {self.rotation}\n{splitter}SCALE: {self.scale}\n{splitter}PARENT: {self.parent}'
                f'\n{splitter}CHILDREN: {self.children}\n{splitter}CLASS ID: {id(self)}\n')

    def __str__(self):
        return self.name if self.name else f"<MayaObject id={id(self)}>" if id(self) else f"<MayaObject>"

    def __name__(self):
        return self.name

    @staticmethod
    def strip_path(value):
        return value[0].split("|")[-1]

    def create(self, _type, name=None):
        if name is None:
            name = self.name
        return cmds.createNode(_type, name=name)

    def get(self, function, *args, **kwargs):
        debug_print(f"GETTING: {function} FROM: {self.name}", level=1)
        func = self.getters.get(function, None)
        if func:
            result = func(self, self.name, *args, **kwargs)
            debug_print(f"FUNCTION: {function} RETURNED: {result}", level=3)
            return result

    def set(self, function, *args, **kwargs):
        debug_print(f"SETTING: {function} FROM: {self.name}", level=1)
        func = self.setters.get(function, None)
        if func:
            result = func(self, self.name, *args, **kwargs)
            debug_print(f"FUNCTION: {function} RETURNED: {result}", level=3)
            return result

    def select(self, add=False, hierarchy=False, only=False, replace=False):
        cmds.select(self.name, add=add, hi=hierarchy, noExpand=only, r=replace)
        return cmds.ls(sl=True)

    def distance_between(self, other):
        return cmds.distanceDimension(sp=self.center, ep=other.get_center())

    def duplicate(self, name: str):
        new_object = MayaObject(name)
        new_object.world_position = self.world_position
        new_object.rotation = self.rotation
        new_object.scale = self.scale
        return new_object.name


class BaseTree:
    def __init__(self, item_list=None, node_class=None, _type=None):
        debug_print("INITIALIZING TREE", style="SECTION", header="base tree", level=10)  # DEBUGGER
        print(item_list)
        self.roots = {}
        self.leaves = {}
        self.nodes = {}
        self.node_class: MayaObject | TreeNode = node_class if node_class else TreeNode
        self.nodes = self.initialize(item_list) if item_list else None
        self._sorted_nodes = None
        debug_print("SORTED NODES:", to_format=self.sorted_nodes, style="CONTAINER", header="base tree",
                    level=7)  # DEBUGGER`
        debug_print("END OF TREE INITIALIZATION", style="SECTION", header="base tree", level=10)  # DEBUGGER

    def initialize(self, item_list):
        pass

    @staticmethod
    def remove_node(node):
        if node.parent is not None:
            node.parent.children.remove(node)

    def sort_input_by_hierarchy(self, _selection):
        sorted_list = []
        queue = deque([(self.nodes, [])])

        while queue:
            current_dict, parent_chain = queue.popleft()

            for key, value in current_dict.items():
                if key in _selection:
                    sorted_list.append((key, parent_chain + [key]))

                queue.append((value, parent_chain + [key]))

        return [joint for joint, _ in sorted(sorted_list, key=lambda x: x[1])]

    def is_contiguous_sublist(self, sub_list):
        try:
            start_index = self.sorted_nodes.index(sub_list[0])
            end_index = self.sorted_nodes.index(sub_list[-1])
        except ValueError:
            return False  # One or more items from the sub_list not found in the main_list

        return self._sorted_nodes[start_index:end_index + 1] == sub_list

    @property
    def sorted_nodes(self):
        if self._sorted_nodes is None:
            self._sorted_nodes = [key for key, value in self.nodes["NODES"].items()]
        return self._sorted_nodes


class MayaObjectTree(BaseTree):
    def __init__(self, item_list: any = None, node_class: Type[MayaObject] = None, _type: str = None):
        debug_print("INITIALIZING TREE", style="SECTION", header="MayaObjectTree", level=10)  # DEBUGGER
        debug_print(f"INITIALIZING TREE WITH THE FOLLOWING: {node_class}, TYPE: {_type}, ITEMS:",
                    style="CONTAINER", to_format=item_list, header="MayaObjectTree", level=2)  # DEBUGGER
        super().__init__(item_list, node_class, _type)

    def __repr__(self):
        return

    def __instance_nodes_list(self, name_list: list):
        debug_print(f"INSTANCING NODES FROM <NODE LIST>: {name_list}", style="CONTAINER", header="MayaObjectTree",
                    level=2)  # DEBUGGER
        return dict((name, self.node_class(name)) for name in name_list if self.node_class(name).get("object_exists"))

    def __instance_nodes_dict(self, node_map: dict, parent_node, collector: dict = None):
        debug_print(f"INSTANCING NODES FROM <NODE DICT>: {node_map}", header="MayaObjectTree",
                    level=1)  # DEBUGGER
        if collector is None:
            debug_print(f"COLLECTOR IS NONE, SETTING TO EMPTY DICT", header="MayaObjectTree",
                        level=2)  # DEBUGGER
            collector = {}

        for node_name, children in node_map.items():
            if node_name == "multiple_roots":
                debug_print(f"NODE: {node_name} IS A MULTIPLE ROOTS DICT", style="CONTAINER",
                            header="MayaObjectTree", level=1)  # DEBUGGER
                for root, _children in node_map["multiple_roots"].items():
                    debug_print(f"NODE: {node_name} HAS ROOT: {root}", header="MayaObjectTree",
                                level=3)  # DEBUGGER
                    self.__instance_nodes_dict(_children, self.node_class(root), collector)
                    if self.node_class(root).get("object_exists"):
                        collector[root] = self.node_class(root)
            else:
                current_node = self.node_class(node_name)
                if parent_node and current_node.get("object_exists"):
                    debug_print(f"NODE: {node_name} HAS PARENT: {parent_node}", header="MayaObjectTree",
                                level=1)  # DEBUGGER
                    parent_node.add_child(current_node)
                elif parent_node:
                    debug_print(f"NODE: {node_name} HAS NO PARENT", header="MayaObjectTree",
                                level=1)
                    current_node.add_parent(self.node_class(current_node.parent))
                    debug_print(f"NODE: {node_name} PARENT IS {current_node.parent}", header="MayaObjectTree",
                                level=1)  # DEBUGGER
                    parent_node.add_child(current_node)

                if current_node.get("object_exists"):
                    debug_print(f"NODE: {node_name} IS A VALID NODE", header="MayaObjectTree",
                                level=1)  # DEBUGGER
                    collector[node_name] = current_node

                if children:
                    debug_print(f"NODE: {node_name} HAS CHILDREN: {children}", header="MayaObjectTree",
                                level=1)  # DEBUGGER
                    self.__instance_nodes_dict(children, current_node, collector)
        debug_print(f"INSTANCED NODES:", to_format=collector, style="CONTAINER", header="MayaObjectTree",
                    level=2)  # DEBUGGER
        return collector

    def __get_node_parent(self, node_name: str):
        debug_print(f"GETTING PARENT OF: {node_name}", header="MayaObjectTree", level=1)  # DEBUGGER
        maya_object = self.node_class(node_name).parent if self.node_class(node_name).parent else None
        debug_print(f"PARENT OF {node_name} IS {maya_object}:\n", header="MayaObjectTree", level=4)  # DEBUGGER
        return maya_object

    def __get_node_children(self, node_name: str):
        debug_print(f"GETTING CHILD OF: {node_name}", header="MayaObjectTree", level=1)  # DEBUGGER
        maya_object = self.node_class(node_name).children if self.node_class(node_name).children else None
        debug_print(f"CHILD OF {node_name} IS {maya_object}:\n", header="MayaObjectTree", level=2)  # DEBUGGER
        return maya_object

    def __set_parent_node(self, node_name: str):
        debug_print(f"GETTING PARENT OF: {node_name}", header="MayaObjectTree", level=1)  # DEBUGGER
        maya_object = self.node_class(node_name)
        if maya_object.parent is None:
            debug_print(f"NODE: {node_name} HAS NO PARENT", header="MayaObjectTree", level=2)  # DEBUGGER
            return None
        parent_node = self.node_class(self.__get_node_parent(node_name))
        if maya_object.parent == parent_node.name:
            debug_print(f"NODE: {node_name} PARENT IS {parent_node}", header="MayaObjectTree",
                        level=2)  # DEBUGGER
            maya_object.add_parent(parent_node)
            return parent_node
        else:
            raise Exception(f"NODE: {node_name} PARENT IS NOT {parent_node}")

    def __set_children_nodes(self, node_name: str):
        debug_print(f"GETTING CHILDREN OF: {node_name}", header="MayaObjectTree", level=1)  # DEBUGGER
        maya_object = self.node_class(node_name)
        if maya_object.children_nodes is None:
            debug_print(f"NODE: {node_name} HAS NO CHILDREN", header="MayaObjectTree", level=2)  # DEBUGGER
            return None
        child_node = self.node_class(self.__get_node_children(node_name))
        if isinstance(child_node, list):
            for child in child_node:
                if maya_object.name == child.parent:
                    debug_print(f"ONE OF NODE: {node_name}'S CHILDREN IS {child}",
                                header="MayaObjectTree", level=2)  # DEBUGGER
                    maya_object.add_child(child)
            return maya_object.children_nodes
        elif maya_object.name == child_node.parent:
            maya_object.add_child(child_node)
            return maya_object.children_nodes
        raise Exception(f"NODE: {node_name} PARENT IS NOT {child_node}")

    def __find_roots_and_leaf_nodes(self, node_list: list):
        debug_print(f"FINDING ROOTS AND LEAVES FROM: {node_list}", style="CONTAINER",
                    header="MayaObjectTree", level=1)  # DEBUGGER
        container_of_root_groups = ["Joints", "Controls", "Meshes", "Curves", "Transforms", "Geometry"]

        for node in node_list:
            debug_print(f"WORKING ON NODE: {node}", header="MayaObjectTree", level=1)  # DEBUGGER
            maya_object = self.node_class(node)
            if maya_object.parent in container_of_root_groups:
                debug_print(f"NODE: {node} PARENT IS A CONTAINER SETTING AS A ROOT", header="MayaObjectTree",
                            level=2)
                self.roots.update({maya_object.name: maya_object})
            if maya_object.parent is None:
                debug_print(f"NODE: {node} PARENT IS THE WORLD/NONE SETTING AS A ROOT",
                            header="MayaObjectTree", level=2)  # DEBUGGER
                self.roots.update({maya_object.name: maya_object})
            if maya_object.children is None:
                debug_print(f"NODE: {node} HAS NO CHILDREN SETTING AS A LEAF", header="MayaObjectTree",
                            level=2)  # DEBUGGER
                self.leaves.update({maya_object.name: maya_object})
            else:
                debug_print(f"NODE: {node} IS NOT A ROOT OR LEAF", header="MayaObjectTree", level=2)
                continue
        debug_print(f"SEARCH COMPLETE\nROOTS: {self.roots}", style="CONTAINER", header="MayaObjectTree",
                    level=2)  # DEBUGGER
        debug_print(f"LEAVES: {self.leaves}", style="CONTAINER", header="MayaObjectTree",
                    level=2)  # DEBUGGER

    def __clean_final_return(self, return_dict):
        debug_print(f"CLEANING RETURN:", to_format=return_dict, style="CONTAINER", header="MayaObjectTree",
                    level=2)  # DEBUGGER
        result = {"NODES": {}, "ENDS": {"LEAVES": {}, "ROOTS": {}}}
        for key, value in return_dict.items():
            result["NODES"].update({key: self.node_class(key)})
            #     result["DATA"]{key: 'parent'} = self.node_class(value).parent_node.name if value.parent_node else None
            #     result["DATA"]{key: 'children'} = [child for child in self.node_class(key).children_nodes]
            #     result["DATA"]{key: 'type'} = value.type
            #     result["DATA"]{key: 'world_position'} = value.world_position
            #     result["DATA"]{key: 'rotation'} = value.rotation
            #     result["DATA"]{key: 'scale'} = value.scale
            if value.parent_node:
                result["NODES"][key].parent_node = value.parent_node.name

        result["ENDS"]["LEAVES"].update(self.leaves.items())
        result["ENDS"]["ROOTS"].update(self.roots.items())
        debug_print(f"CLEANED RETURN:", to_format=result, style="CONTAINER", header="MayaObjectTree",
                    level=1)
        return result

    def __set_relationships(self, _node_instances: dict):
        for node_name, node in _node_instances.items():
            try:
                debug_print(f"WORKING ON ITEM: {node_name} AND NODE: {node}", style="CONTAINER",
                            header="MayaObjectTree", level=4)  # DEBUGGER
                self.__set_parent_node(node_name)
                self.__set_children_nodes(node_name)
            except Exception as e:
                debug_print(f"Error while processing item: {node_name}. Error: {str(e)}", header="MayaObjectTree",
                            level=8)  # DEBUGGER

    def initialize(self, node_map: list | str | dict):  # override
        debug_print(f"INITIALIZING TREE WITH: {node_map}", style="CONTAINER", header="MayaObjectTree",
                    level=2)
        if isinstance(node_map, dict):
            debug_print(f"INSTANCING NODES FROM DICT", level=1)
            instances = self.__instance_nodes_dict(node_map, None)

        elif isinstance(node_map, list):
            debug_print(f"INSTANCING NODES FROM LIST", level=1)
            instances = self.__instance_nodes_list(node_map)
        else:
            debug_print(f"INSTANCING NODES FROM STR", level=1)
            instances = self.__instance_nodes_list([node_map])
        debug_print(f"RETURNED INSTANCES:", to_format=instances, style="CONTAINER", header="MayaObjectTree",
                    level=4) if instances else None  # DEBUGGER
        self.__set_relationships(instances)
        self.__find_roots_and_leaf_nodes([nodes for _, nodes in instances.items()])
        instances = self.__clean_final_return(instances)
        if self.nodes is None:
            debug_print(f"SETTING TREE TO: {instances}", style="CONTAINER", header="MayaObjectTree",
                        level=2)  # DEBUGGER
            debug_print("END OF INITIALIZING TREE", style="END-SECTION", header="MayaObjectTree",
                        level=2)  # DEBUGGER
            self.nodes = instances
        else:
            debug_print(f"ADDING TO TREE: {instances}", style="CONTAINER", header="MayaObjectTree",
                        level=2)  # DEBUGGER

            debug_print("END OF INITIALIZING TREE", style="END-SECTION", header="MayaObjectTree",
                        level=2)  # DEBUGGER
            return instances


if __name__ == "__main__":
    type_to_exclude = ["parentConstraint", "pointConstraint", "orientConstraint", "scaleConstraint", "aimConstraint",
                       "ikHandle", "ikEffector", "ikSolver", "ikRPsolver", "ikSCsolver", "ikSplineSolver"]
    # selection = MayaSelectionOperator().selection
    # ik = IkManager(selection, excluded_types=type_to_exclude)
    joint_list = MayaSelectionOperator().get(_type="joint", _all=True)
    ik = IkManager(joint_list)
    # ChannelBox().create_coor_ui()
"""
