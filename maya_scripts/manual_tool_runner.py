from collections import deque
import traceback
from typing import Type
import inspect
from maya import cmds
import math
from PySide2.QtWidgets import QGridLayout
from PySide2.QtCore import QTimer
from PySide2 import QtWidgets, QtCore
import random

global wall_gen_ui

debug_level = 5  # 0 - 10
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
    footer = kwargs.get('footer', stack['function'])
    end_div = kwargs.get('end_div', div)

    if kwargs.get('to_format', None):
        data = kwargs.get('to_format')
        if isinstance(data, dict):
            result = "{\n" + '\n'.join([f"\t\t{k}, {v}" for k, v in data.items()]) + "\n\t\t}"
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
        self.selection = MayaSelectionOperator().selection
        self.mapped_selection = MayaSelectionOperator(excluded_types=excluded_types,
                                                      included_types=included_types,
                                                      root=root_name, ).map_hierarchy(self.selection)
        debug_print("IK MANAGER GETTING SELECTION IN MAYA SCENE", to_format=self.mapped_selection,
                    style="CONTAINER", header="IkManager", level=10)  # DEBUGGER
        self.tree = MayaObjectTree(self.mapped_selection, MayaObject)
        debug_print("IK MANAGER GETTING ALL SELECTED HIERARCHIES IN MAYA SCENE",
                    to_format=self.tree.nodes, style="CONTAINER", header="IkManager", level=10)  # DEBUGGER
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


class MayaSelectionOperator:
    selection = cmds.ls(sl=True)

    def __init__(self, excluded_types=None, included_types=None, _type=None, _all=False, **kwargs):
        debug_print("INITIALIZING SELECTION OPERATOR", style="SECTION", header="MayaSelectionOperator",
                    level=10)
        self.excluded_types = excluded_types
        self.include_types = included_types
        self.forced_root = kwargs.get("root", None)

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
        if _all and _type is not None:
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
            if (_node is None or not cmds.objExists(_node) or cmds.objectType(_node) in self.excluded_types or
                    self.forced_root and _node == self.forced_root):
                debug_print(f"RETURNING: {_node} AS ROOT", header="MayaSelectionOperator", level=5)
                return None
            parent = cmds.listRelatives(_node, parent=True)
            return _node if parent is None else find_top_parent(self.strip_path(parent[0]))

        def get_hierarchy(_root):
            debug_print(f"GETTING HIERARCHY OF: {_root}", style="CONTAINER", header="MayaSelectionOperator",
                        level=5)
            _hierarchy = {}
            queue = deque([(_root, _hierarchy)])
            while queue:
                current, parent_dict = queue.popleft()
                children = cmds.listRelatives(current, children=True) or []
                debug_print(f"CHILDREN OF: {current} ARE: {children}\n{current}'S PARENT IS",
                            style="CONTAINER", to_format=parent_dict, header="MayaSelectionOperator", level=5)
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

        return result


class TreeNode:
    _instances = {}

    def __new__(cls, identity, *args, **kwargs):
        if identity in cls._instances:
            return cls._instances[identity]
        instance = super(TreeNode, cls).__new__(cls)
        cls._instances[identity] = instance
        return instance

    def __init__(self, identity, ):
        self.children = None
        self._identity = identity
        self._parent_node = None
        self._children_nodes = []

    def __repr__(self):
        return f"{self.__class__}({self._identity})"

    def __str__(self):
        return f"{self.__class__}({self._identity})"

    @property
    def parent_node(self):
        return self._parent_node

    @parent_node.setter
    def parent_node(self, parent_node):
        self.add_parent(parent_node)

    @property
    def children_nodes(self):
        return self._children_nodes

    @parent_node.setter
    def parent_node(self, child_node):
        self.add_child(child_node)

    def add_parent(self, parent_node: 'TreeNode'):
        debug_print(f"ADDING PARENT: {parent_node} TO: {self._identity}", level=3)
        self._parent_node = parent_node
        parent_node.add_child(self)
        debug_print(f"PARENT OF {self._identity} IS {self._parent_node._identity}:\n", header="TreeNode", level=4)

    def remove_parent(self, parent_node: 'TreeNode'):
        debug_print(f"REMOVING PARENT: {parent_node} FROM: {self._identity}", level=3)
        self._parent_node = None
        parent_node.remove_child(self)

    def add_child(self, child_node: 'TreeNode'):
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

    def get_parent(self, _object):
        debug_print(f"GETTING PARENT OF: {self.name}", header="MayaObjectTree", level=2)  # DEBUGGER
        parent = cmds.listRelatives(_object, parent=True)
        return self.strip_path(parent) if parent else None

    def get_children(self, _object):
        debug_print(f"GETTING CHILDREN OF: {self.name}", header="MayaObjectTree", level=2)  # DEBUGGER
        parent = cmds.listRelatives(_object, children=True)
        return self.strip_path(parent) if parent else None

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

    def __init__(self, name: str, ):
        if isinstance(name, list):
            name = self.strip_path(name)
        super().__init__(name)
        self.name = name
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
                f'\n{splitter}CHILDREN: {self.children}\n{splitter}CLASS ID: <MayaObject id={id(self)}>\n')

    def __str__(self):
        return self.name

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
        debug_print("INITIALIZING TREE", style="SECTION", header="base tree")
        self.roots = []
        self.leaves = []
        self.nodes = {}
        self.node_class = node_class if node_class else TreeNode
        self.nodes = self.initialize(item_list) if item_list else None

    def initialize(self, item_list):
        pass

    @staticmethod
    def remove_node(node):
        if node.parent is not None:
            node.parent.children.remove(node)


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
                for root, children in node_map["multiple_roots"].items():
                    debug_print(f"NODE: {node_name} HAS ROOT: {root}", header="MayaObjectTree",
                                level=3)  # DEBUGGER
                    self.__instance_nodes_dict(children, self.node_class(root), collector)
                    if self.node_class(root).get("object_exists"):
                        collector[root] = self.node_class(root)
            else:
                current_node = self.node_class(node_name)
                if parent_node and current_node.get("object_exists"):
                    debug_print(f"NODE: {node_name} HAS PARENT: {parent_node}", header="MayaObjectTree",
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
        if maya_object.children is None:
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
            if maya_object.parent is None:
                debug_print(f"NODE: {node} PARENT IS THE WORLD/NONE SETTING AS A ROOT",
                            header="MayaObjectTree", level=2)  # DEBUGGER
                self.roots.append(maya_object)
            elif maya_object.children is None:
                debug_print(f"NODE: {node} HAS NO CHILDREN SETTING AS A LEAF", header="MayaObjectTree",
                            level=2)  # DEBUGGER
                self.leaves.append(maya_object)
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
        result = {"NODES": {}, "ENDS": {"LEAVES": None, "ROOTS": None}}
        for key, value in return_dict.items():
            result["NODES"].update({key: self.node_class(key)})
        #     result["DATA"]{key: 'parent'} = self.node_class(value).parent_node.name if value.parent_node else None
        #     result["DATA"]{key: 'children'} = [child for child in self.node_class(key).children_nodes]
        #     result["DATA"]{key: 'type'} = value.type
        #     result["DATA"]{key: 'world_position'} = value.world_position
        #     result["DATA"]{key: 'rotation'} = value.rotation
        #     result["DATA"]{key: 'scale'} = value.scale
        result["ENDS"]["LEAVES"] = "".join([f"\n\t\t\tNAME: {leaf.name}" for leaf in self.leaves])  # noqa
        result["ENDS"]["ROOTS"] = "".join([f"\n\t\t\tNAME: {root.name}" for root in self.roots])  # noqa
        debug_print(f"CLEANED RETURN:", to_format=result, style="CONTAINER", header="MayaObjectTree",
                    level=10)
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

    def initialize(self, node_map: list | str | dict):
        debug_print(f"INITIALIZING TREE WITH: {node_map}", style="CONTAINER", header="MayaObjectTree",
                    level=2)
        if isinstance(node_map, dict):
            debug_print(f"INSTANCING NODES FROM DICT", debug_level=1)
            instances = self.__instance_nodes_dict(node_map, None)

        elif isinstance(node_map, list):
            debug_print(f"INSTANCING NODES FROM LIST", debug_level=1)
            instances = self.__instance_nodes_list(node_map)
        else:
            debug_print(f"INSTANCING NODES FROM STR", debug_level=1)
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


def create_wall(params):
    x = params['x']
    y = params['y']
    z = params['z']
    wall_width = params['wall_width']
    wall_height = params['wall_height']
    brick_width = params['brick_width']
    brick_height = params['brick_height']
    brick_depth = params['brick_depth']
    h_offset = params['h_offset']
    v_offset = params['v_offset']
    d_offset = params['d_offset']
    curve_intensity = params['curve_intensity']
    size_variation = params['size_variation']
    dynamic_fill = params['dynamic_fill']

    # Delete existing 'wall_group' if it exists
    if cmds.objExists("wall_group"):
        cmds.delete("wall_group")

    # Create a new empty transform group
    wall_group = cmds.group(em=True, name="wall_group")

    current_wall_width = 0
    current_wall_height = 0

    while current_wall_height < wall_height:
        first_brick_in_row = True  # Flag to check if it's the first brick in the row
        while current_wall_width < wall_width:
            # Apply size variation
            varied_width = brick_width + random.uniform(-size_variation, size_variation)
            varied_height = brick_height + random.uniform(-size_variation, size_variation)

            # Create brick
            brick = cmds.polyCube(w=varied_width, h=varied_height, d=brick_depth)[0]

            # Parent the brick to the wall_group
            cmds.parent(brick, wall_group)

            if first_brick_in_row:
                x[0] = -wall_width / 2
                first_brick_in_row = False

            # Calculate percentage of how far from the center of the wall this brick is
            pct_from_center = (x[0] + wall_width / 2) / (wall_width / 2)

            # Check before the sqrt calculation
            z_curve = math.sqrt(max(curve_intensity ** 2 - x[0] ** 2, 0))

            # Flip the rotation calculation logic, so edge bricks face the opposite end
            y_rotation = -math.degrees(math.atan2(z_curve, x[0])) if x[0] != 0 else 0  # Avoid division by zero

            cmds.setAttr(f"{brick}.translateX", x[0])
            cmds.setAttr(f"{brick}.translateY", y[0])
            cmds.setAttr(f"{brick}.translateZ", z[0] + z_curve)
            cmds.setAttr(f"{brick}.rotateY", y_rotation)

            x[0] += varied_width + h_offset
            current_wall_width += varied_width + h_offset

            # Dynamic fill
            if dynamic_fill and current_wall_width > wall_width:
                cmds.setAttr(brick + ".scaleX", wall_width - (current_wall_width - varied_width))

        x[0] = -wall_width / 2
        z[0] += d_offset
        current_wall_width = 0
        y[0] += varied_height + v_offset
        current_wall_height += varied_height + v_offset


class WallGeneratorUI(QtWidgets.QWidget):
    def __init__(self):
        super(WallGeneratorUI, self).__init__()
        self.dynamic_fill_checkbox = None
        self.auto_update_checkbox = None
        self.setWindowTitle("Brick Wall Generator")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.generate_wall)

        self.build_ui()

    def build_ui(self):
        layout = QGridLayout()

        self.add_coordinate_control("X:", 0, layout, 6, 2)
        self.add_coordinate_control("Y:", 0, layout, 6, 3)
        self.add_coordinate_control("Z:", 0, layout, 6, 4)
        self.add_feature_control("Brick Width:", 1, 100, 25, layout, 0, 0)
        self.add_feature_control("Brick Height:", 1, 100, 25, layout, 0, 1)
        self.add_feature_control("Brick Depth:", 1, 100, 15, layout, 2, 0)
        self.add_feature_control("Size Variation:", 0, 50, 0, layout, 2, 1)
        self.add_feature_control("Wall Width:", 1, 50, 20, layout, 3, 0)
        self.add_feature_control("Wall Height:", 1, 30, 7.5, layout, 3, 1)
        self.add_feature_control("Vertical Offset:", 0, 100, 1, layout, 4, 0)
        self.add_feature_control("Horizontal Offset:", 0, 100, 1, layout, 4, 1)
        self.add_feature_control("Depth Offset:", 0, 50, 1, layout, 5, 0)
        self.add_feature_control("Curve Intensity:", 0, 100, 0, layout, 5, 1)

        self.auto_update_checkbox = QtWidgets.QCheckBox("Enable Auto Update")
        layout.addWidget(self.auto_update_checkbox, 6, 0)

        self.dynamic_fill_checkbox = QtWidgets.QCheckBox("Enable Dynamic Fill")
        layout.addWidget(self.dynamic_fill_checkbox, 6, 1)

        generate_button = QtWidgets.QPushButton("Generate Wall")
        layout.addWidget(generate_button, 7, 0, 1, 7)
        generate_button.clicked.connect(self.generate_wall)

        self.setLayout(layout)

    def add_feature_control(self, label, min_val, max_val, default_val, layout, row, col, widget_type="slider"):
        if widget_type == "slider":
            # Create Label
            lbl = QtWidgets.QLabel(label)
            lbl.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Add size policy if needed

            # Create Slider
            slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(default_val)
            slider.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)  # Add size policy if needed

            # Create SpinBox
            spinbox = QtWidgets.QDoubleSpinBox()
            spinbox.setRange(min_val, max_val)
            spinbox.setValue(default_val)
            spinbox.setSingleStep(0.01)
            spinbox.setDecimals(2)
            spinbox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Add size policy if needed

            # Connect Slider and SpinBox
            slider.valueChanged.connect(spinbox.setValue)
            spinbox.valueChanged.connect(slider.setValue)

            # Connect to the generation function
            slider.valueChanged.connect(self.delayed_generate_wall)
            spinbox.valueChanged.connect(self.delayed_generate_wall)

            # Add widgets to layout
            layout.addWidget(lbl, row, col * 3)  # Labels take up one column
            layout.addWidget(slider, row, col * 3 + 1)  # Sliders take up one column
            layout.addWidget(spinbox, row, col * 3 + 2)  # Spinboxes take up one column

            # Store references to these widgets for later use
            attribute_name = label.replace(" ", "_").replace(":", "").lower()
            setattr(self, attribute_name + "_slider", slider)
            setattr(self, attribute_name + "_spinbox", spinbox)

    def add_coordinate_control(self, label, default_val, layout, row, col):
        line_edit = QtWidgets.QLineEdit()
        line_edit.setText(str(default_val))
        line_edit.setFixedWidth(40)
        line_edit.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)

        label_widget = QtWidgets.QLabel(label)
        label_widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        layout.addWidget(label_widget, row, col, alignment=QtCore.Qt.AlignRight)
        layout.addWidget(line_edit, row, col + 1, 1, 1, alignment=QtCore.Qt.AlignLeft)

        attribute_name = label.replace(" ", "_").replace(":", "").lower()
        setattr(self, attribute_name + "_line_edit", line_edit)

    def delayed_generate_wall(self):
        if self.auto_update_checkbox.isChecked():
            self.timer.stop()
            self.timer.start(2000)  # 2000 ms delay

    def generate_wall(self):
        x = [float(self.x_line_edit.text())]
        y = [float(self.y_line_edit.text())]
        z = [float(self.z_line_edit.text())]
        params = {
            "x": x,
            "y": y,
            "z": z,
            "brick_width": self.brick_width_slider.value() / 50,
            "brick_height": self.brick_height_slider.value() / 50,
            "brick_depth": self.brick_depth_slider.value() / 50,
            "wall_width": self.wall_width_slider.value(),
            "wall_height": self.wall_height_slider.value(),
            "h_offset": self.horizontal_offset_slider.value() / 50,
            "v_offset": self.vertical_offset_slider.value() / 50,
            "d_offset": self.depth_offset_spinbox.value() / 50,
            "curve_intensity": self.curve_intensity_slider.value(),
            "size_variation": self.size_variation_slider.value() / 50,
            "dynamic_fill": self.dynamic_fill_checkbox.isChecked(),
        }

        create_wall(params)


def start_wall_ui():
    global wall_gen_ui  # Declare as global so we can access and modify it

    # Check if QApplication instance exists
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    # Destroy the existing UI if it already exists
    try:
        wall_gen_ui.close()
    except:
        pass

    # Create and show a new UI instance
    wall_gen_ui = WallGeneratorUI()
    wall_gen_ui.show()


if __name__ == "__main__":
    # type_to_exclude = ["parentConstraint", "pointConstraint", "orientConstraint", "scaleConstraint", "aimConstraint",
    #                    "ikHandle", "ikEffector", "ikSolver", "ikRPsolver", "ikSCsolver", "ikSplineSolver",]
    # selection = MayaSelectionOperator().selection
    # ik = IkManager(selection, excluded_types=type_to_exclude)

    # joint_list = MayaSelectionOperator().get(_type="joint", _all=True)
    # ik = IkManager(joint_list)

    start_wall_ui()
