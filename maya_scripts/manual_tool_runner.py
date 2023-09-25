import maya.cmds as cmds
import traceback
from typing import Type

debug_level = 5
style_presets = {
    "SECTION": {'div': ("|" + "~~" * 50 + "|\n"), 'add_div': True, 'header_function': True, 'section': True},
    "SECTION-END": {'div': ("\n|" + "/\\" * 50 + "|\n|" + "\\/" * 50 + "|"), 'add_end_div': True,
                    'footer_function': True, 'section_end': True},
    "SUBSECTION": {'div': ("|"+f"{' '*20}|" + "v" * 65 + "|\n"), 'add_div': True, 'header_function': True,
                   'subsection': True},
    "SUBSECTION-END": {'div': ("|"+f"{' '*20}|" + "^" * 65 + "|"), 'add_end_div': True, 'footer_function': True,
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
        elif isinstance(data, list):
            result = "[\n\t\t" + '\n\t\t'.join(data) + "\n\t\t]"
        elif isinstance(data, tuple):
            result = "{\n\t\t" + '\n\t\t'.join(data) + "\n\t\t}"
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
            header = f"{header}\n|{' '*41}END OF SECTION"
        if kwargs.get('subsection_end', False):
            header = f"{header}\n|{' '*41}END OF SUBSECTION"
        message = f"{message}\n|{footer}"

    if kwargs.get('header', False) or kwargs.get('header_function', False):
        if kwargs.get('header_function', False):
            header = f"|{' ' * (50 - (len(header)))}{header}.{stack['function']}".upper()
        if kwargs.get('section', False):
            header = f"{' '*41}START OF SECTION\n{header}"
        if kwargs.get('subsection', False):
            header = f"{' '*41}START OF SUBSECTION\n{header}"
        message = f"{header}\n{message}"

    if kwargs.get('add_function', False):
        message = f"\t{stack['function']}{message}"

    print(f"|{message}\n|--------File \"{stack['file']}\", line {stack['line_num']}, in {stack['function']}\n|")


class IkManager:
    def __init__(self):
        self.selection = SelectionOperator()
        self.joint_list = self.selection.get(_type="joint", _all=True)
        debug_print("IK MANAGER GETTING ALL JOINT'S IN MAYA SCENE", to_format=self.joint_list,
                    style="CONTAINER", level=4)  # DEBUGGER
        self.tree = BaseTree(self.joint_list, MayaObject)


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
    def __init__(self, external_id):
        debug_print("INITIALIZING TREE NODE", style="SECTION", header="tree node", level=10)  # DEBUGGER
        debug_print(f"NAME PASSED TO TREE NODE {external_id}", level=2)  # DEBUGGER
        self.external_id = external_id
        self.data = {}
        self._children: list[TreeNode] = []
        self._parent = None

    def __getattr__(self, name):
        debug_print(f"GETTING ATTRIBUTE {name}", header="tree node", level=2)  # DEBUGGER
        return getattr(self.data, name)

    def __setattr__(self, name, value):
        debug_print(f"SETTING ATTRIBUTE {name}", header="tree node", level=2)  # DEBUGGER
        return setattr(self.data, name, value)

    def add_child(self, child_node: Type[TreeNode]):
        self.children.append(child_node)
        child_node.parent = self

    def remove_child(self, child_node: Type[TreeNode]):
        self.children.remove(child_node)
        child_node.parent = None


class BaseTree:
    def __init__(self, item_list: any = None, node_class: Type[TreeNode] = None):
        debug_print("INITIALIZING TREE", style="SECTION", header="base tree", level=10)  # DEBUGGER
        self.root = None
        self.node_class = node_class if node_class else TreeNode
        if item_list:
            debug_print("ITEM LIST PROVIDED ON BASE TREE INIT, INITIALIZING WITH THE FOLLOWING",
                        style="CONTAINER", to_format=item_list, header="base tree", level=4)  # DEBUGGER
            self.initialize_from_list(item_list)

    def initialize_from_list(self, item_list):
        debug_print("INITIALIZING FROM LIST", style="SUBSECTION", header="base tree", level=7)  # DEBUGGER
        debug_print("INITIALIZING FROM", style="CONTAINER", to_format=item_list, header="base tree",
                    level=4)  # DEBUGGER
        debug_level = 0  # DEBUGGER
        name_to_node = {}

        # Step 1: Create node instances and add them to a dictionary
        for item in item_list:
            debug_print(f"CREATING NODE INSTANCE FOR: {item}", level=2)  # DEBUGGER
            node_instance = self.node_class(item)
            debug_print(f"NODE INSTANCE CREATED: {node_instance}", level=2)  # DEBUGGER
            name_to_node[item] = node_instance
        debug_print("ALL NODES CREATED:", to_format=name_to_node, style="CONTAINER",
                    header="base tree", level=4)  # DEBUGGER

        # Step 2: Set up parent-child relationships and heapify
        for item, node in name_to_node.items():
            parent = node.data.parent  # Assumes all data objects have a parent attribute
            if parent in name_to_node:
                parent_node = name_to_node[parent]
                parent_node.add_child(node)

        # Step 3: Identify the root (no parent) and set it
        for node in name_to_node.values():
            if node.parent is None:
                self.root = node
                break

    @staticmethod
    def remove_node(node):
        if node.parent is not None:
            node.parent.children.remove(node)


class MayaObject(TreeNode):
    def __init__(self, name: str, _type: str = None, parent: str = None):
        super().__init__(name)
        if isinstance(name, list):
            name = name[0]
        self._name = name
        self._type = self.type if _type is None else _type
        self._world_position = None
        self._rotation = None
        self._scale = None
        self._children = []
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
        debug_print(f"GETTING PARENT: {self._parent}", level=1)  # DEBUGGER
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
        debug_print(f"GETTING CURRENT PARENT: {self._parent}", level=1)  # DEBUGGER
        debug_print(f"GETTING PASSED PARENT: {parent}", level=1)  # DEBUGGER
        if parent == 'world':
            if cmds.listRelatives(self.name, parent=True) is not None:
                self._parent = cmds.parent(self.name, world=True)
        else:
            self._parent = cmds.parent(self.name, parent)

    @property
    def children(self):
        debug_print(f"GETTING CHILDREN OF: {self.name}", level=1)  # DEBUGGER
        return self._children

    @children.setter
    def children(self, node):
        self.add_child(node)

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


if __name__ == "__main__":
    ik = IkManager()
    # ik.create_ik()
