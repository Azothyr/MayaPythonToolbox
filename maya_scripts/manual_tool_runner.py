import maya.cmds as cmds
from collections import defaultdict
from maya_scripts.tools.xform_handler import xform_attributes, check_strange_values, set_xform_values, get_xform_values
import traceback

style_presets = {
    "SECTION": {'div': ("|" + "-"*100 + "|\n")*2, 'add_div': True, 'add_function': True},
    "CONTAINER": {'div': ("-"*100 + "\n")*1, 'add_div': True, 'add_function': True},
}


def debug_print(message, style=None, **kwargs):
    def __get_traceback_line(__stack: traceback) -> str:
        return __stack.line

    def __get_traceback_file(__stack: traceback) -> str:
        return __stack.filename

    def __get_traceback_func(__stack: traceback) -> str:
        return __stack.name

    def __get_traceback_line_num(__stack: traceback) -> str:
        return __stack.lineno

    def __get_traceback_stack() -> dict[str]:
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

    if kwargs.get('to_format', None):
        result = '\n'.join([f"{k}, {v}" for k, v in kwargs.get('to_format').items()])
        message = f"{message}\n{result}\n{div}"

    if kwargs.get('add_div', False):
        message = f"{div}{message}"

    if kwargs.get('add_function', False):
        header = f"{' '*(50-(len(header)//2))}{header}.{stack['function']}".upper()
        message = f"{header}\n{message}"

    print(f"{message}\n\t\tFile \"{stack['file']}\", line {stack['line_num']}, in {stack['function']}\n")


class IkManager:

    def __init__(self):
        # Creates a dictionary of operation data that is checked for discrepancies then stored in
        # self.operation_data for use in the create_ik method.
        self.operation_data = None
        self.constrainer = Constrainer
        self.controller = ControlCreator
        self.grouper = GroupCreator
        self.__working_data = {}
        self.__current_data = {}
        self.__base_handler = {}
        self.__pv_handler = {}
        self.__tip_handler = {}

    def get_data(self):
        return self.operation_data if self.operation_data else IkDataFactory().create_operation_data()

    def constrain(self, item, leader, follower, constraint_type):
        pass

    def create_ik_handle(self, name, base_joint, tip_joint, ik_type):
        pass

    def create_ik(self, ik_type=None):
        print(f"Operation Data: {self.operation_data}")  # DEBUGGER
        self.operation_data = self.get_data()
        if not self.operation_data or not isinstance(self.operation_data, dict) or self.operation_data == {}:
            raise Exception("No operation data found.")
        for key, value in self.operation_data.items():
            self.__working_data = value
            self.__base_handler = self.__working_data.get('Base', None)
            self.__pv_handler = self.__working_data.get('PV', None)
            self.__tip_handler = self.__working_data.get('Tip', None)
            # print(f"Working Data: {self.__working_data}")
            print(f"Base Handler: {self.__base_handler}")
            print(f"PV Handler: {self.__pv_handler}")
            print(f"Tip Handler: {self.__tip_handler}")
            if self.__base_handler and self.__pv_handler and self.__tip_handler:
                self.__create_ik_chain()
            else:
                raise Exception("Missing data to create IK chain.")


class IkDataFactory:
    def __init__(self):
        self.namer = lambda x: NameParser(x).prefix  # Gets class instance and returns the prefix of x item
        self.selected_joints = SelectionOperator().get("joint")  # Gets selected joints from scene
        self.hierarchy = HierarchySorter(self.selected_joints).get()  # Sorts joints by hierarchy
        # Creates a RelationshipManager instance that checks joint hierarchy
        self.relation_manager = RelationshipManager()

    def create_operation_data(self):
        joint_data = {}

        if not self.selected_joints:
            raise Exception("No joints selected. Please select at least 1 joints.")
        print(f"Selected joints print order 1: {self.selected_joints}")  # DEBUGGER
        self.selected_joints = self.relation_manager.check_ik_hierarchy(*self.hierarchy)
        print(f"Selected joints print order 2: {self.selected_joints}")  # DEBUGGER

        def set_joint_tuples():
            if self.selected_joints:
                count = 0
                joint_tuples = []
                _joint_tuple = []
                for joint in self.selected_joints:
                    if count != 3:
                        _joint_tuple.append(joint)
                        count += 1

                    # When _joint_tuple has 3 items
                    if len(_joint_tuple) == 3:
                        _joint_tuple = tuple(_joint_tuple)
                        joint_tuples.append(_joint_tuple)
                        count = 0
                        _joint_tuple = []
                return joint_tuples

        for joint_tuple in set_joint_tuples():
            prefix = self.namer(str(joint_tuple[0]))
            joint_data[prefix] = {
                "Base": ["_Ctrl_Grp", "_Ctrl", "_01_IK_Jnt", joint_tuple[0]],
                "PV": ["_Ctrl_Grp", "_Ctrl", "_Offset", "_02_IK_Jnt", joint_tuple[1]],
                "Tip": ["_Ctrl_Grp", "_Ctrl", "_IK_Handle", "_03_IK_Jnt", joint_tuple[2]]
            }
        # print(f"create_operation_data: {joint_data}")  # DEBUGGER
        return self.parse_operation_data(joint_data)

    @staticmethod
    def parse_operation_data(broken_data):
        op_data = {}
        interior_data = {}
        for key, value in broken_data.items():
            prefix = key + "_IK"
            for k, v in value.items():
                # print(f"K: {k}, V: {v}")  # DEBUGGER
                center = f"_{k}"
                group = prefix + center + v[0]
                control = prefix + center + v[1]
                new_joint = key + v[-2]
                joint = v[-1]
                interior_data[k] = dict(group=group, control=control, new_joint=new_joint, old_joint=joint)
                if "_Offset" in v:
                    offset_group = prefix + center + v[2]
                    interior_data[k].update(dict(offset=offset_group))
                if "_IK_Handle" in v:
                    ik_handle = key + v[2]
                    interior_data[k].update(dict(ik_handle=ik_handle))
            main_group = key + "_IK_Ctrl_Grp"
            op_data[main_group] = dict(**interior_data)
        print_data = '\n'.join([f'{outer_key}, {inner_key}, {inner_value}' for outer_key, inner_dict in
                                op_data.items() for inner_key, inner_value in inner_dict.items()])
        # print(f"parse_operation_data:\n{print_data}")  # DEBUGGER
        return op_data


class SelectionOperator:
    # A mapping between the _type and the argument passed to __get_selection.
    type_to_arg = {
        "joint": "joint",
        "control": "transform",
        "mesh": "mesh",
        "curve": "nurbsCurve",
        "transform": "transform",
        "all": None,
        "long": {"long": True},
    }

    @staticmethod
    def __get_selection(_type=None, long=False):
        return cmds.ls(sl=True, long=long) if _type is None else cmds.ls(sl=True, type=_type, long=long)

    def get(self, _type: object):
        return self.__get_selected_type(_type)

    @staticmethod
    def select(item: str, clear=True, add=False, hierarchy=False, only=False, replace=False):
        if clear:
            cmds.select(cl=True)
        else:
            cmds.select(item, add=add, hi=hierarchy, noExpand=only, r=replace)

    def count(self, _type: object):
        return self.get_selected_type_count(_type)

    def __get_selected_type(self, _type):
        arg = self.type_to_arg.get(_type, None)
        if arg is None:
            return None
        elif isinstance(arg, dict):
            return self.__get_selection(**arg)
        else:
            return self.__get_selection(arg)

    def get_selected_type_count(self, _type):
        arg = self.__get_selected_type(_type)
        if arg is None:
            return None
        else:
            return len(arg) if isinstance(arg, list) else 1


class ControlCreator:
    pass

    # def control_creation(self):
    #     # joints_to_process = selected_joints if len(selected_joints) > 1 else cmds.ls(sl=True)[0:1]

    #             control_lyst = []
    #             for joint in joints_to_process:
    #                 joint_position = cmds.xform(joint, q=True, ws=True, t=True)
    #                 joint_rotation = cmds.xform(joint, q=True, ws=True, ro=True)
    #                 circle = cmds.circle(normal=[1, 0, 0], radius=radius)[0]

    #                 circle_rename = joint.replace("Jnt", "Ctrl")
    #                 circle = cmds.rename(circle, circle_rename)

    #                 control_lyst.append(circle)

    #                 null_group = cmds.group(empty=True)
    #                 null_group_rename = joint.replace("Jnt", "Ctrl_Grp")
    #                 null_group = cmds.rename(null_group, null_group_rename)

    #                 cmds.parent(circle, null_group)

    #                 cmds.xform(null_group, ws=True, t=joint_position)
    #                 cmds.xform(null_group, ws=True, ro=joint_rotation)

    #             return control_lyst


class MayaObject:

    def __init__(self, name: str, _type: str = None, parent: str = None):
        if isinstance(name, list):
            name = name[0]
        self._name = self.create(_type, name) if not cmds.objExists(name) else name
        self._type = self.type if _type is None else _type
        self._world_position = None
        self._rotation = None
        self._scale = None
        self._parent = None if parent is None else self.parent(parent)

    def __repr__(self):
        return (f'{self._type}: "{self.name}" \nWorld Position: {self.world_position}'
                f'\nRotaion: {self.rotation}\nScale: {self.scale}\nParent: {self.parent}\n')

    def __str__(self):
        return self.name

    def __name__(self):
        return self.name

    def create(self, _type, name=None):
        if name is None:
            name = self.name
        return cmds.createNode(_type, name=name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        cmds.rename(self._name, value)
        self._name = value

    @property
    def world_position(self):
        if self._world_position is None:
            self._world_position = cmds.xform(self.name, q=True, ws=True, t=True)
        return self._world_position

    @world_position.setter
    def world_position(self, position: tuple[3]):
        self._world_position = cmds.xform(self.name, ws=True, t=position)

    @property
    def rotation(self):
        if self._rotation is None:
            self._rotation = cmds.xform(self.name, q=True, ws=True, ro=True)
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: tuple[3]):
        self._rotation = cmds.xform(self.name, ws=True, ro=rotation)

    @property
    def scale(self):
        if self._scale is None:
            self._scale = cmds.xform(self.name, q=True, ws=True, scale=True)
        return self._scale

    @scale.setter
    def scale(self, scale: tuple[3]):
        self._scale = cmds.xform(self.name, ws=True, scale=scale)

    @property
    def parent(self, expected_parent=None):
        print(f"GETTING PARENT: {self._parent}")  # DEBUGGER
        if self._parent is None:
            if expected_parent:
                if expected_parent != 'world':
                    if (cmds.objExists(expected_parent) and
                            expected_parent == cmds.listRelatives(self.name, parent=True)):
                        self._parent = cmds.listRelatives(self.name, parent=True)
                    elif cmds.objExists(expected_parent):
                        self._parent = cmds.parent(self.name, expected_parent)
                    else:
                        print(f"Parent does not exist: {expected_parent}")
                        self._parent = cmds.listRelatives(self.name, parent=True)
                else:
                    self._parent = cmds.parent(self.name, world=True)
            elif cmds.listRelatives(self.name, parent=True) is None:
                return "'WORLD', which is considered None"
            else:
                self._parent = cmds.listRelatives(self.name, parent=True)
        return self._parent

    @parent.setter
    def parent(self, parent):
        print(f"GETTING PARENT: {self._parent}")  # DEBUGGER
        print(f"GETTING PASSED PARENT: {parent}")  # DEBUGGER
        if parent == 'world':
            if cmds.listRelatives(self.name, parent=True) is not None:
                self._parent = cmds.parent(self.name, world=True)
        else:
            self._parent = cmds.parent(self.name, parent)

    @property
    def children(self):
        return cmds.listRelatives(self.name, children=True)

    @property
    def descendants(self):
        return cmds.listRelatives(self.name, allDescendents=True)

    @property
    def ancestors(self):
        return cmds.listRelatives(self.name, allParents=True)

    @property
    def type(self):
        return cmds.objectType(self.name)

    @property
    def shape(self):
        return cmds.listRelatives(self.name, shapes=True)

    @property
    def shape_type(self):
        return cmds.objectType(self.shape)

    @property
    def bounding_box(self):
        return cmds.exactWorldBoundingBox(self.name)

    @property
    def center(self):
        bbox = self.bounding_box
        return (
            (bbox[0] + bbox[3]) / 2,
            (bbox[1] + bbox[4]) / 2,
            (bbox[2] + bbox[5]) / 2
        )

    def select(self, add=False, hierarchy=False, only=False, replace=False):
        cmds.select(self.name, add=add, hi=hierarchy, noExpand=only, r=replace)
        return cmds.ls(sl=True)

    def distance_between(self, other):
        return cmds.distanceDimension(sp=self.center, ep=other.get_center())

    def duplicate(self, name: str):
        new_object = MayaObject(name, self._type)
        new_object.world_position = self.world_position
        new_object.rotation = self.rotation
        new_object.scale = self.scale
        return new_object.name


class GroupCreator:
    pass


class RelationshipManager:
    @staticmethod
    def check_ik_hierarchy(*args):
        debug_print(f"CHECKING IK HIERARCHY: {args}")  # DEBUGGER

        def _get_relation(_object, relation_type, count_function, flag):
            debug_print(f"GETTING RELATION: {_object}, {relation_type}, {count_function}, {flag}")  # DEBUGGER
            count = count_function(_object, "joint")
            if count == 0 or not count:
                return None
            else:
                retrieved_relations = RelationshipManager.get_relations(_object, "joint", **{flag: True},
                                                                        count=2)
                debug_print(f"RETRIEVED RELATIONS: {retrieved_relations}\nfrom {_object}\nwith flag: {flag}\n and "
                      f"func: {count_function}")  # DEBUGGER
                return retrieved_relations[0] if flag == '_parent' else retrieved_relations[1]

        def get_parent_count_func(_object, type):
            return RelationshipManager().get_parent_count(_object, type)

        def get_child_count_func(_object, type):
            return RelationshipManager().get_child_count(_object, type)

        def _parse_args(_args):
            final_processed_args = []

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

            def _get_parent(obj):
                return _get_relation(obj, "parent", get_parent_count_func, '_parent')

            def _get_child(obj):
                return _get_relation(obj, "child", get_child_count_func, '_children')

            def _construct_relation_dict(_base, _pv, _tip):
                debug_print(f"CONSTRUCTING RELATION DICT WITH BASE JOINT: {_base}, PV JOINT: {_pv}, TIP JOINT: {_tip}")
                return {  # DEBUGGER
                    _base: dict(parent=_get_parent(_base), child=_get_child(_base)),
                    _pv: dict(parent=_get_parent(_pv), child=_get_child(_pv)),
                    _tip: dict(parent=_get_parent(_tip), child=_get_child(_tip))
                }

            def __check_hierarchy(base_jnt: str, pv_jnt: str, tip_jnt: str):
                check_dict = _construct_relation_dict(base_jnt, pv_jnt, tip_jnt)
                debug_print(f"CHECK DICT: {check_dict}\n-----------\n----------\n")  # DEBUGGER
                _base_jnt = base_jnt
                _pv_jnt = pv_jnt
                _tip_jnt = tip_jnt

                def _format_values(obj, relation_type):
                    _result = check_dict[obj][relation_type]
                    # debug_print(f"FORMATTING VALUES: {obj}, {relation_type}, {_result}, {type(_result)}") # DEBUGGER
                    if isinstance(_result, list):
                        # debug_print(f"RETURNING: {_result[0]}") # DEBUGGER
                        return _result[0]
                    else:
                        # debug_print(f"RETURNING: {_result}") # DEBUGGER
                        return _result

                def __relation_dict_check(_base_jnt, _pv_jnt, _tip_jnt) -> dict:
                    results = {}
                    # schema: {base_jnt_passed: [bool, [parent, child]],
                    # pv_jnt_passed: [bool, [parent, child]],
                    # tip_jnt_passed: [bool, [parent, child]]}
                    try:
                        # Check if Base is a parent of PV and if it has parents they are not _pv_jnt or _tip_jnt
                        _base_jnt_parent = _format_values(_base_jnt, 'parent')
                        _base_jnt_child = _format_values(_base_jnt, 'child')
                        # DEBUGGER
                        # debug_print(f"\n{_base_jnt}\n---------\n--------\nPARENT'S TYPE{type(_base_jnt_parent)}"
                        #       f"\nCHILD'S TYPE{type(_base_jnt_child)}\n---------\n--------\n")

                        results['base_jnt_passed'] = [_base_jnt_child == _pv_jnt and
                                                      (_base_jnt_parent is None or
                                                       (_base_jnt_parent != _pv_jnt and _base_jnt_parent != tip_jnt)
                                                       ), [_base_jnt_parent, _base_jnt_child]]
                        if not results['base_jnt_passed'][0]:
                            raise Exception(f"Child of _base_jnt --> {_base_jnt} is not PV --> {_pv_jnt}")

                        # Check if _pv_jnt is a child of _base_jnt and a parent of _tip_jnt
                        _pv_jnt_parent = _format_values(_pv_jnt, 'parent')
                        _pv_jnt_child = _format_values(_pv_jnt, 'child')
                        # DEBUGGER
                        # debug_print(f"\n\n-_pv_jnt_parent == _base_jnt and _pv_jnt_child == tip_jnt")
                        # debug_print(f"|-->{_pv_jnt_parent} == {_base_jnt} and {_pv_jnt_child} == {tip_jnt}")
                        # debug_print(f"|---->{_pv_jnt_parent == _base_jnt} and {_pv_jnt_child == tip_jnt}")
                        # debug_print(f"|------>{_pv_jnt_parent == _base_jnt and _pv_jnt_child == tip_jnt}\n\n")
                        # debug_print(f"{_pv_jnt}\n---------\n--------\nPARENT'S TYPE{type(_pv_jnt_parent)}"
                        #       f"\nCHILD'S TYPE{type(_pv_jnt_child)}\n---------\n--------\n")

                        results['pv_jnt_passed'] = [_pv_jnt_parent == _base_jnt and _pv_jnt_child == tip_jnt,
                                                    [_pv_jnt_parent, _pv_jnt_child]]
                        if not results['pv_jnt_passed'][0]:
                            raise Exception(f"PV jnt --> {_pv_jnt} does not have the correct parent-child"
                                            f" relationship.")

                        # Check if _tip_jnt is a child of _pv_jnt and if it has children they are not _pv_jnt or
                        _tip_jnt_parent = _format_values(_tip_jnt, 'parent')
                        _tip_jnt_child = _format_values(_tip_jnt, 'child')
                        # DEBUGGER
                        # debug_print(f"\n{_tip_jnt}\n---------\n--------\nPARENT'S TYPE{type(_tip_jnt_parent)}"
                        #       f"\nCHILD'S TYPE{type(_tip_jnt_child)}\n---------\n--------\n")

                        results['tip_jnt_passed'] = [_tip_jnt_parent == _pv_jnt and
                                                     (_tip_jnt_child is None or
                                                      (_tip_jnt_child != _pv_jnt and _tip_jnt_child != _base_jnt)),
                                                     [_tip_jnt_parent, _tip_jnt_child]]
                        if not results['tip_jnt_passed'][0]:
                            raise Exception(f"Tip jnt --> {_tip_jnt} does not have the"
                                            f" correct parent-child relationship.")
                    except Exception as err:
                        results['error'] = str(err)
                        raise err
                    return results

                if __relation_dict_check(_base_jnt, _pv_jnt, _tip_jnt).get('error', None):
                    return False
                debug_print(f"All checks passed for Base: {_base_jnt}, PV: {_pv_jnt}, Tip: {_tip_jnt}")  # DEBUGGER
                return True

            debug_print(f"\nSTART OF CHECK_IK_HIERARCHY._PARSE_ARGS: PARSING{_args}", add_div=True)  # DEBUGGER
            for _group in _split_args(_args):
                if len(_group) == 3:
                    debug_print(f"GROUP CONSIDERED TO BE A LENGTH OF 3: {_group}")
                    _base, _pv, _tip = _group  # Unpack the group into variables
                    # DEBUGGER
                    debug_print(f"Checking Hierarchy with BASE JOINT: {_base}, PV JOINT: {_pv}, TIP JOINT: {_tip}")
                    if __check_hierarchy(_base, _pv, _tip):
                        _de_tuple(_group, final_processed_args)
                    else:
                        raise Exception(f"Something went wrong during Checking Hierarchy with"
                                        f" BASE JOINT: {_base}, PV JOINT: {_pv}, TIP JOINT: {_tip}")

                elif len(_group) < 3:
                    if len(_group) == 2:
                        pass
                    if len(_group) == 1:
                        pass
                    else:
                        raise Exception("This Exception should never be raised."
                                        " _RelationshipManager__check_hierarchy is broken.")
                else:
                    raise Exception(f"This Exception should never be raised. for some reason the group has more"
                                    f" than 3 items. {_group}, {len(_group)}")

            debug_print(f"FINAL PROCESSED ARGS: {final_processed_args}")  # DEBUGGER
            return final_processed_args

        arg_set = _parse_args(args)
        debug_print(f"PASSING ARGS TO PARSE ARGS : {args}\nRETURNING ARGS FROM PARSE ARGS : {arg_set}")  # DEBUGGER
        return arg_set

    @staticmethod
    def get_relations(_object, type=None, _parent=False, _children=False, count: int = 0, **kwargs):
        get_all = kwargs.get('all', False)
        debug_print(f"GETTING RELATIONS: {_object}, {type}, {_parent}, {_children}, {count}, {kwargs}")  # DEBUGGER

        def list_relatives_helper(action_type, _type, _count):
            if get_all:
                return cmds.listRelatives(_object, **{action_type: True, 'type': _type})

            relatives_list = cmds.listRelatives(_object, **{action_type: True, 'type': _type})
            if _count > 0:
                return relatives_list[0:_count] if relatives_list else None
            return relatives_list

        parent = None
        children = None

        if _parent:
            if count > 0:
                parent = list_relatives_helper('allParents', type, count)
            else:
                parent = list_relatives_helper('parent', type, count)

        if _children:
            children = list_relatives_helper('children', type, count)

        return parent, children

    def get_child_count(self, _object: object, _type: str) -> int:
        return len(self.get_relations(_object, type=_type, _children=True, all=True))

    def get_parent_count(self, _object: object, _type: str) -> int:
        return len(self.get_relations(_object, type=_type, _parent=True, all=True))


class NameParser:
    def __init__(self, item: str, splitter: str = "_"):
        self.item = item
        self.split_symbol = splitter
        self.prefix = self.__parse_string()

    def __parse_string(self):
        parts = self.item.split(self.split_symbol)
        prefix = f"{parts[0]}_{parts[1]}"
        return prefix


class Constrainer:
    def __init__(self, name: str, leader: object, follower: object, constraint_type: str):
        self.name = name
        self.leader = leader
        self.follower = follower
        self.constraint_type = constraint_type

    def create_constraint(self):
        match self.constraint_type:
            case "point":
                self.create_point_constraint()
            case "orient":
                self.create_orient_constraint()
            case "parent":
                self.create_parent_constraint()
            case "aim":
                self.create_aim_constraint()
            case _:
                pass

    def create_point_constraint(self):
        cmds.pointConstraint(self.leader, self.follower, name=self.name)

    def create_orient_constraint(self):
        cmds.orientConstraint(self.leader, self.follower, name=self.name)

    def create_parent_constraint(self):
        cmds.parentConstraint(self.leader, self.follower, name=self.name)

    def create_aim_constraint(self):
        cmds.aimConstraint(self.leader, self.follower, name=self.name)


class IkCreator:
    def __init__(self, name: str, base_joint: object, tip_joint: object, ik_type: str):
        self.name = name
        self.base = base_joint
        self.tip = tip_joint
        self.ik_type = ik_type

    def create_ik(self):
        match self.ik_type:
            case "ik":
                self.create_ik_handle()
            case "pole":
                self.create_pole_vector()
            case "spring":
                self.create_spring_ik()
            case "stretchy":
                self.create_stretchy_ik()
            case "stretchy_spline":
                self.create_stretchy_spline_ik()
            case _:
                pass

    def create_ik_handle(self):
        cmds.ikHandle(startJoint=self.base, endEffector=self.tip)

    def create_pole_vector(self):
        pass

    def create_spring_ik(self):
        pass

    def create_stretchy_ik(self):
        pass

    def create_stretchy_spline_ik(self):
        pass


class GenericTree:
    def __init__(self):
        self.tree = defaultdict(list)
        debug_print(f"INITIALIZED TREE: {self.tree}")  # DEBUGGER
        self.sorted_nodes = []

    def build_tree(self, node_list, get_parent_callback=None):
        debug_print(f"BUILDING TREE WITH NODE LIST: {node_list}")  # DEBUGGER
        for node in node_list:
            parent = get_parent_callback(node) if get_parent_callback else None
            debug_print(f"WORKING ON NODE: {node}\tNODE'S PARENT SET TO: {parent}")  # DEBUGGER
            self.tree[parent].append(node)
        debug_print("UPDATED TREE: defaultdict(list)\n{}", style='CONTAINER',
                    to_format=self.tree, header="GenericTree")  # DEBUGGER

    def traverse_tree(self, node):
        debug_print(f"TRAVERSE TREE PASSED NODE: {node}")  # DEBUGGER
        if node is None:
            debug_print(f"PASSED NODE({node}) IS NONE, RETURNING", color='red')  # DEBUGGER
            return
        self.sorted_nodes.append(node)
        debug_print(f"APPENDING NODE TO SORTED NODES: {node}")  # DEBUGGER
        for child in sorted(self.tree[node]):
            debug_print(f"SENDING CHILD: {child}")  # DEBUGGER
            self.traverse_tree(child)
        # node_debug_output = "\n".join([item for item in self.sorted_nodes])
        node_debug_output = sorted(self.tree[node])
        debug_print(f"END OF TRAVERSE TREE, RETURNING SORTED NODES: "
                    f"{node_debug_output}, {self.sorted_nodes}")  # DEBUGGER


class HierarchySorter(GenericTree):
    def __init__(self, object_list: list):
        debug_print(f"START OF SORTING BY HIERARCHY, PASSED-OBJECT LIST: {object_list}", style='SECTION',
                    header=__class__.__name__)  # DEBUGGER
        super().__init__()
        self.object_list = object_list
        self.__create_tree()

    @staticmethod
    def __strip_path(joint_name):
        debug_print(f"STRIPPING FROM NAME IF NEEDED: {joint_name}\nRETURNING:"
                    f" {joint_name.split('|')[-1] if '|' in joint_name else joint_name}")  # DEBUGGER
        return joint_name.split("|")[-1] if '|' in joint_name else joint_name

    def get(self):
        root_joints = []
        if None in self.tree:
            debug_print(f"NONE IN TREE ROOT JOINTS SETTING ROOTS TO: {self.tree[None]}")  # DEBUGGER
            root_joints = self.tree[None]

        for root in root_joints:
            debug_print(f"ROOT: {root}")  # DEBUGGER
            self.traverse_tree(root)
        debug_print(f"END OF HIERARCHY SORTING, RETURNING SORTED NODES: {self.sorted_nodes}")  # DEBUGGER
        return self.sorted_nodes

    def __create_tree(self):
        debug_print(f"TREE CREATION STARTED, HIERARCHYSORTER PASSING OBJECT LIST TO BASE CLASS "
                    f"GENERICTREE TO BUILD AND SORT THE TREE\n{self.object_list}")  # DEBUGGER
        super().build_tree(self.object_list, self.__get_parent)

    def __get_parent(self, joint):
        try:
            parent = cmds.listRelatives(joint, parent=True, fullPath=True)
        except ValueError:
            parent = None
        debug_print(f"GETTING PARENT OF: {joint}\nPARENT'S FULL PATH: {parent}\nRETURNING:"
                    f" {self.__strip_path(parent[0]) if parent else None}")  # DEBUGGER
        return self.__strip_path(parent[0]) if parent else None


if __name__ == "__main__":
    ik = IkManager()
    ik.create_ik()
