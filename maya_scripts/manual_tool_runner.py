import maya.cmds as cmds
import traceback
from typing import Type, Dict, Any
import inspect

debug_level = 8  # 0 - 10
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
    def __init__(self):
        debug_print("START OF IK MANAGER INITIALIZATION", style="SECTION", header="IkManager",
                    level=10)  # DEBUGGER
        self.selection = SelectionOperator()
        self.joint_list = self.selection.get(_type="joint", _all=True)
        debug_print("IK MANAGER GETTING ALL JOINT'S IN MAYA SCENE", to_format=self.joint_list,
                    style="CONTAINER", header="IkManager", level=4)  # DEBUGGER
        self.tree = MayaObjectTree(self.joint_list, MayaObject, _type="joint")
        debug_print("IK MANAGER GETTING ALL JOINT'S IN MAYA SCENE", to_format=self.tree.nodes["ENDS"],
                    style="CONTAINER", header="IkManager", level=8)  # DEBUGGER
        debug_print("END OF IK MANAGER INITIALIZATION", style="SECTION", header="IkManager",
                    level=10)  # DEBUGGER


class SelectionOperator:
    # A mapping between the _type and the argument passed to __get_selection.
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


class TreeNode:
    _instances = {}

    def __new__(cls, identity, *args, **kwargs):
        if identity in cls._instances:
            return cls._instances[identity]
        instance = super(TreeNode, cls).__new__(cls)
        cls._instances[identity] = instance
        return instance

    def __init__(self, identity, ):
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


class MayaObject(TreeNode):

    @staticmethod
    def generic_getter(func):
        def wrapper(self, _object, *args, **kwargs):
            expected_args = len(inspect.signature(func).parameters)
            debug_print(f"GETTING: {func} FROM: MayaObject ExPECTS {expected_args} ARGS", level=1)

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
        new_object = MayaObject(name, self._type)
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
        self.nodes = self.initialize_from_list(item_list) if item_list else None

    def initialize_from_list(self, item_list):
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

    def __instance_nodes(self, name_list):
        debug_print(f"INSTANCING NODES FROM: {name_list}", style="CONTAINER", header="MayaObjectTree",
                    level=2)  # DEBUGGER
        return dict((name, self.node_class(name)) for name in name_list if self.node_class(name).get("object_exists"))

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

    def __find_roots_and_leaf_nodes(self, node_list: str):
        debug_print(f"FINDING ROOTS AND LEAVES FROM: {node_list}", style="CONTAINER",
                    header="MayaObjectTree", level=1)  # DEBUGGER
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
        debug_print(f"CLEANING RETURN: {return_dict}", style="CONTAINER", header="MayaObjectTree",
                    level=2)  # DEBUGGER
        result = {"NODES": {}, "ENDS": {"LEAVES": None, "ROOTS": None}}
        for key, value in return_dict.items():
            result["NODES"] = {key: self.node_class(key)}
        #     result["DATA"]{key: 'parent'} = self.node_class(value).parent_node.name if value.parent_node else None
        #     result["DATA"]{key: 'children'} = [child for child in self.node_class(key).children_nodes]
        #     result["DATA"]{key: 'type'} = value.type
        #     result["DATA"]{key: 'world_position'} = value.world_position
        #     result["DATA"]{key: 'rotation'} = value.rotation
        #     result["DATA"]{key: 'scale'} = value.scale
        result["ENDS"]["LEAVES"] = "".join([f"\n\t\t\tNAME: {leaf.name}" for leaf in self.leaves])  # noqa
        result["ENDS"]["ROOTS"] = "".join([f"\n\t\t\tNAME: {root.name}" for root in self.roots])  # noqa
        debug_print(f"CLEANED RETURN: {result}", style="CONTAINER", header="MayaObjectTree",
                    level=2)
        return result

    def initialize_from_list(self, item_list):
        instances = self.__instance_nodes(item_list)
        debug_print(f"INSTANCES: {instances}", style="CONTAINER", header="MayaObjectTree", level=2)  # DEBUGGER

        for item_name, node in instances.items():
            try:
                debug_print(f"WORKING ON ITEM: {item_name} AND NODE: {node}", style="CONTAINER",
                            header="MayaObjectTree", level=4)  # DEBUGGER
                self.__set_parent_node(item_name)
                self.__set_children_nodes(item_name)
            except Exception as e:
                debug_print(f"Error while processing item: {item_name}. Error: {str(e)}", header="MayaObjectTree",
                            level=8)  # DEBUGGER

        self.__find_roots_and_leaf_nodes(item_list)
        instances = self.__clean_final_return(instances)
        if self.nodes is None:
            debug_print(f"SETTING TREE TO: {instances}", style="CONTAINER", header="MayaObjectTree",
                        level=2)  # DEBUGGER
            debug_print("END OF INITIALIZING TREE", style="END-SECTION", header="MayaObjectTree",
                        level=10)  # DEBUGGER
            self.nodes = instances
        else:
            debug_print(f"ADDING TO TREE: {instances}", style="CONTAINER", header="MayaObjectTree",
                        level=2)  # DEBUGGER

            debug_print("END OF INITIALIZING TREE", style="END-SECTION", header="MayaObjectTree",
                        level=10)  # DEBUGGER
            return instances


if __name__ == "__main__":
    ik = IkManager()
    # ik.create_ik()
