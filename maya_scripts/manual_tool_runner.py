import maya.cmds as cmds
import traceback
from typing import Type

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
                result = "[\n\t\t" + '\n\t\t'.join([f"X: {item[0]}, Y: {item[1]}, Z: {item[2]}" for item in data]) + "\n\t\t]"
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
        self.selection = SelectionOperator()
        self.joint_list = self.selection.get(_type="joint", _all=True)
        debug_print("IK MANAGER GETTING ALL JOINT'S IN MAYA SCENE", to_format=self.joint_list,
                    style="CONTAINER", header="IkManager", level=4)  # DEBUGGER
        self.tree = MayaObjectTree(self.joint_list, MayaObject, _type="joint")


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
    def __init__(self, external_id, _type=None):
        debug_print("INITIALIZING TREE NODE", style="SECTION", header="tree node", level=2)  # DEBUGGER
        debug_print(f"PASSED TO TREE NODE, NAME: {external_id}, TYPE: {_type}", level=3)  # DEBUGGER
        self.__dict__.update({
            'data': {},
        })
        self.data['name'] = external_id
        self.data['type'] = _type
        self.data['children']: list[TreeNode] = []
        self.data['parent'] = None
        debug_print(f"SELF.__DICT__:", to_format=self.__dict__, style="CONTAINER", header="tree node",
                    level=4)  # DEBUGGER

    def __repr__(self):
        debug_print(f"GETTING REPRESENTATION OF: {self}", level=1)  # DEBUGGER
        return self

    def __str__(self):
        debug_print(f"GETTING STRING REPRESENTATION OF: {self}", level=1)  # DEBUGGER
        return f"{self.type}: {self.name}"

    def __getattr__(self, attr_name):
        # Remove leading underscore if exists
        cleaned_name = attr_name.lstrip("_")

        # Search in 'data' dict
        if cleaned_name in self.__dict__.get("data", {}):
            return self.__dict__["data"][cleaned_name]

        # Search in other known attributes
        known_attrs = ['data', 'children', 'parent', 'type', 'name']
        for known_attr in known_attrs:
            if cleaned_name == known_attr:
                return self.__dict__[known_attr]

        # If we reach here, the attribute wasn't found
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr_name}'")

    def __setattr__(self, _key, value):
        debug_print(f"SETTING ATTRIBUTE {_key} TO {value}", header="tree node", level=2)  # DEBUGGER
        if 'data' in self.__dict__:
            containers = ['data', '_children', '_parent', '_type', '_name']
            if _key in containers:  # Add other base attributes as needed
                debug_print(f"SETTING ATTRIBUTE IN {containers}, KEY: {_key} TO: {value}", level=3)  # DEBUGGER
                self.__dict__[_key] = value  # Directly set the attribute in the instance dictionary
            else:
                debug_print(f"SETTING ATTRIBUTE, KEY: {_key} TO: {value}", level=3)  # DEBUGGER
                self.__dict__['data'][_key] = value  # Otherwise, add it to the 'data' dictionary

    def add_child(self, child_node: 'TreeNode'):
        debug_print(f"ADDING CHILD: {child_node} TO: {self}", level=3)  # DEBUGGER
        self._children.append(child_node)
        child_node.parent = self
        debug_print(f"CHILDREN OF {self}:\n",
                    to_format=self.children, style="CONTAINER", header="TreeNode", level=4)  # DEBUGGER

    def remove_child(self, child_node: 'TreeNode'):
        debug_print(f"REMOVING CHILD: {child_node} FROM: {self}", level=3)  # DEBUGGER
        self._children.remove(child_node)
        child_node.parent = None
        debug_print(f"CHILDREN OF {self}:\n",
                    to_format=self.children, style="CONTAINER", header="TreeNode", level=4)  # DEBUGGER


class MayaObject(TreeNode):
    def __init__(self, ext_id: str, _type: str = None, parent: str = None):
        debug_print("INITIALIZING MAYA OBJECT", style="SECTION", header="maya object", level=2)  # DEBUGGER
        debug_print(f"PASSED VALUES, NAME: {ext_id}, TYPE: {_type}", level=1)  # DEBUGGER
        if isinstance(ext_id, list):
            debug_print(f"EXT_ID IS A LIST, GETTING FIRST ITEM", level=1)  # DEBUGGER
            ext_id = ext_id[0]
        debug_print(f"INITIALIZING MAYA OBJECT WITH: {ext_id}, ", level=2)  # DEBUGGER
        self.data = self.__dict__
        super().__init__(ext_id, _type)
        debug_print(f"INITIALIZED MAYA OBJECT: {self} WITH DATA:", style="SECTION", header="maya object", level=1)
        self.data['name'] = self.strip_to_name(ext_id) if ext_id and self._exists(ext_id) else None
        debug_print(f"INITIALIZED MAYA OBJECT: "
                    f"{_type if _type and _type.lower() == cmds.objectType(ext_id) else cmds.objectType(ext_id)}"
                    f" WITH DATA:", style="SECTION", header="maya object",)
        self.data['type'] = _type if _type and _type.lower() == cmds.objectType(ext_id) else cmds.objectType(ext_id)
        self.data['world_position'] = self.data.get('world_position', parent)
        self.data['rotation'] = self.data.get('rotation', parent)
        self.data['scale'] = self.data.get('scale', parent)
        self.data['children'] = self.data.get('children', parent)
        self.data['parent'] = self.data.get('parent', parent)
        debug_print(f"INITIALIZED MAYA OBJECT: {self} WITH DATA:", style="SECTION", header="maya object",
                    to_format=self.data, level=4)  # DEBUGGER

    @staticmethod
    def strip_to_name(value: str):
        if '|' in value:
            return value.split('|')[-1]
        else:
            return value

    @staticmethod
    def _exists(name):
        return cmds.objExists(name)

    def create(self, _type, name=None):
        if name is None:
            name = self.data['name']
        cmds.createNode(_type, name=name)

    def un_parent(self): self.parent = 'world'

    def __repr__(self): return self

    def __str__(self): return (f'{self._type}: "{self.name}" \nWorld Position: {self.world_position}' 
                               f'\nRotaion: {self.rotation}\nScale: {self.scale}\nParent: {self.parent}\n')

    def __name__(self):
        return self.name

    def __class__(self):
        return type(self)

    @property
    def world_position(self):
        debug_print(f"GETTING WORLD POSITION OF: {self.name}", level=1)
        if self.data.get('world_position', None) is None:
            self.data['world_position'] = cmds.xform(self.name, q=True, ws=True, t=True)
        debug_info = [str(item) for item in self.data.get('world_position')]
        debug_print(f"WORLD POSITION OF {self.name}:", to_format=debug_info,
                    style="CONTAINER", header="MayaObject", level=2)  # DEBUGGER
        return self.data.get('world_position')

    @world_position.setter
    def world_position(self, position: tuple[3]):
        debug_info = [str(item) for item in position]
        debug_print(f"SETTING WORLD POSITION OF: {self.name} TO:",
                    to_format=debug_info, style="CONTAINER", header="MayaObject", level=2)  # DEBUGGER
        self.data['world_position'] = cmds.xform(self.name, ws=True, t=position)

    @property
    def rotation(self):
        debug_print(f"GETTING ROTATION OF: {self.name}", level=1)
        if self.data.get('rotation', None) is None:
            self.data['rotation'] = cmds.xform(self.name, q=True, ws=True, ro=True)
        debug_info = [str(item) for item in self.data.get('world_position')]
        debug_print(f"ROTATION OF {self.name}:",
                    to_format=debug_info, style="CONTAINER", header="MayaObject", level=2)  # DEBUGGER
        return self.data.get('rotation')

    @rotation.setter
    def rotation(self, rotation: tuple[3]):
        debug_info = [str(item) for item in rotation]
        debug_print(f"SETTING ROTATION OF: {self.name} TO:",
                    to_format=debug_info, style="CONTAINER", header="MayaObject", level=2)  # DEBUGGER
        self.data['rotation'] = cmds.xform(self.name, ws=True, ro=rotation)

    @property
    def scale(self):
        debug_print(f"GETTING SCALE OF: {self.name}", level=1)
        if self.data.get('scale', None) is None:
            self.data['scale'] = cmds.xform(self.name, q=True, ws=True, scale=True)
        debug_info = [str(item) for item in self.data.get('scale')]
        debug_print(f"SCALE OF {self.name}:",
                    to_format=debug_info, style="CONTAINER", header="MayaObject", level=2)  # DEBUGGER
        return self.data.get('scale')

    @scale.setter
    def scale(self, scale: tuple[3]):
        debug_print(f"SETTING SCALE OF: {self.name} TO: {scale}", level=1)
        self.data['scale'] = cmds.xform(self.name, ws=True, scale=scale)
        debug_info = [str(item) for item in scale]
        debug_print(f"SCALE OF {self.name}:",
                    to_format=debug_info, style="CONTAINER", header="MayaObject", level=2)  # DEBUGGER

    @property
    def parent(self):
        debug_print(f"GETTING PARENT: {self.data.get('parent', None)}", level=1)  # DEBUGGER
        if self.data.get('parent', None) is None:
            debug_print(f" PARENT IS {self.data['parent']}, CHECKING MAYA", level=2)  # DEBUGGER
            parent = cmds.listRelatives(self.name, parent=True)
            if isinstance(parent, list):
                if "|" in parent[0]:
                    parent = parent[0].split('|')[-1]
                parent = parent[0]
            self.data['parent'] = self.strip_to_name(parent) if parent else None
        debug_print(f"PARENT OF {self.name}: {self.data.get('parent', None)}", level=2)  # DEBUGGER
        return self.data.get('parent')

    @parent.setter
    def parent(self, parent):
        debug_print(f"SETTING PARENT: {parent}", level=1)  # DEBUGGER
        if isinstance(parent, list):
            if "|" in parent[0]:
                parent = parent[0].split('|')[-1]
            parent = parent[0]
        if parent == 'world':
            debug_print(f"UNPARENTING: {self.name} SET TO {'WORLD considered None'}", level=2)  # DEBUGGER
            self.data['parent'] = cmds.parent(self.name, world=True)
        else:
            self.data['parent'] = cmds.parent(self.name, parent) if cmds.objExists(
                parent) else cmds.parent(self.name, world=True)
            debug_print(f"PARENTING: {self.name} TO: {parent}", level=2)  # DEBUGGER

    @property
    def children(self):
        debug_print(f"GETTING CHILDREN OF: {self.name}", level=1)  # DEBUGGER
        children = '\n'.join([str(child) for child in self.children]) if self.data.get('children', None) else None
        debug_print(f"CHILDREN OF {self.name}:\n{children}", level=2)  # DEBUGGER
        return children

    @children.setter
    def children(self, node):
        debug_print(f"ADDING CHILD: {node} TO: {self.name}", level=1)  # DEBUGGER
        self.add_child(node)

    @property
    def ancestors(self):
        debug_print(f"GETTING ANCESTORS OF: {self.name}", level=1)  # DEBUGGER
        if not self.data.get('ancestors', None):
            ancestors = cmds.listRelatives(self.name, allParents=True)
            self.data['ancestors'] = ancestors
        else:
            ancestors = self.data.get('ancestors')
        ancestors = '\n'.join([self.strip_to_name(ancestor) for ancestor in ancestors])
        debug_print(f"ANCESTORS OF {self.name}:\n{ancestors}", level=2)  # DEBUGGER
        return ancestors

    @property
    def type(self):
        debug_print(f"GETTING TYPE OF: {self.name}", level=1)  # DEBUGGER
        self.data['type'] = self.data.get('type', cmds.objectType(self.name))
        debug_print(f"TYPE OF {self.name}: {self.data.get('type')}", level=2)  # DEBUGGER
        return self.data.get('type', cmds.objectType(self.name))

    @property
    def shape(self):
        debug_print(f"GETTING SHAPE OF: {self.name}", level=1)  # DEBUGGER
        self.data['shape'] = self.data.get('shape', cmds.listRelatives(self.name, shapes=True))
        debug_print(f"SHAPE OF {self.name}: {self.data.get('shape')}", level=2)  # DEBUGGER
        return self.data['shape']

    @property
    def shape_type(self):
        debug_print(f"GETTING SHAPE TYPE OF: {self.name}", level=1)  # DEBUGGER
        self.data['shape_type'] = self.data.get('shape_type', cmds.objectType(self.shape))
        debug_print(f"SHAPE TYPE OF {self.name}: {self.data.get('shape_type')}", level=2)  # DEBUGGER
        return self.data['shape_type']

    @property
    def bounding_box(self):
        debug_print(f"GETTING BOUNDING BOX OF: {self.name}", level=1)  # DEBUGGER
        debug_print(f"BOUNDING BOX OF {self.name}: {self.data.get('bounding_box', None)}", level=2)  # DEBUGGER
        return self.data.get('bounding_box', cmds.exactWorldBoundingBox(self.name))

    @property
    def center(self):
        debug_print(f"GETTING CENTER OF: {self.name}", level=1)  # DEBUGGER
        bbox = self.data.get('center', None) if self.data.get('center') else self.bounding_box
        debug_print(f"CENTER OF {self.name}: {bbox}", level=2)  # DEBUGGER
        return (
            (bbox[0] + bbox[3]) / 2,
            (bbox[1] + bbox[4]) / 2,
            (bbox[2] + bbox[5]) / 2
        )

    def select(self, add=False, hierarchy=False, only=False, replace=False):
        debug_print(f"SELECTING: {self.name}", level=1)  # DEBUGGER
        cmds.select(self.name, add=add, hi=hierarchy, noExpand=only, r=replace)
        debug_print(f"SELECTED: {cmds.ls(sl=True)}", level=2)  # DEBUGGER
        return cmds.ls(sl=True)

    def distance_between(self, other):
        debug_print(f"GETTING DISTANCE BETWEEN: {self.name} AND {other.name}", level=1)  # DEBUGGER
        debug_print(f"DISTANCE BETWEEN {self.name} AND {other.name}:"
                    f" {cmds.distanceDimension(sp=self.center, ep=other.get_center())}", level=2)  # DEBUGGER
        return cmds.distanceDimension(sp=self.center, ep=other.get_center())

    def duplicate(self, name: str):
        debug_print(f"DUPLICATING: {self.name} AS {name}", level=1)  # DEBUGGER
        new_object = MayaObject(name, self._type)
        new_object.un_parent()
        new_object.world_position = self.world_position
        new_object.rotation = self.rotation
        new_object.scale = self.scale
        debug_print(f"DUPLICATED: {new_object.name}\n WITH WORLD", level=2)  # DEBUGGER
        return new_object.name


class BaseTree:
    def __init__(self, item_list: any = None, node_class: Type[TreeNode] = None, _type: str = None):
        debug_print("INITIALIZING TREE", style="SECTION", header="base tree", level=10)  # DEBUGGER
        self.roots = None
        self.node_class = node_class if node_class else TreeNode
        if item_list:
            debug_print("ITEM LIST PROVIDED ON BASE TREE INIT, INITIALIZING WITH THE FOLLOWING",
                        style="CONTAINER", to_format=item_list, header="base tree", level=3)  # DEBUGGER
            self.initialize_from_list(item_list, _type=_type)
        debug_print()

    def __instance_nodes(self, item_list, _type=None):
        debug_print("INSTANCING NODES", style="SUBSECTION", header="base tree", level=7)
        nodes = {}
        for item in item_list:
            debug_print(f"CREATING NODE INSTANCE FOR: {item}", level=3)  # DEBUGGER
            node_instance = self.node_class(item, _type)
            debug_print(f"NODE INSTANCE CREATED: {node_instance}", level=3)  # DEBUGGER
            nodes[item] = node_instance
        debug_print("ALL NODES CREATED:", to_format=nodes, style="CONTAINER",
                    header="base tree", level=4)  # DEBUGGER
        return nodes

    def initialize_from_list(self, item_list, _type=None):
        debug_print("INITIALIZING FROM LIST", style="SUBSECTION", header="base tree", level=7)  # DEBUGGER
        debug_print("INITIALIZING FROM", style="CONTAINER", to_format=item_list, header="base tree",
                    level=4)  # DEBUGGER
        # Step 1: Create node instances and add them to a dictionary
        name_to_node = self.__instance_nodes(item_list, _type=_type)

        # Step 2: Set up parent-child relationships and heapify
        for item, node in name_to_node.items():
            debug_print(f"SETTING UP PARENT-CHILD RELATIONSHIP FOR: {item} OF {node}", level=3)  # DEBUGGER
            parent = node.parent('parent', None)  # Assumes all data objects have a parent attribute
            debug_print(f"PARENT OF {node}: {parent}", level=1)  # DEBUGGER
            if parent in name_to_node:
                debug_print(f"PARENT FOUND IN DICT", level=1)  # DEBUGGER
                parent_node = name_to_node[parent]
                debug_print(f"PARENT NODE: {parent_node}", level=1)  # DEBUGGER
                parent_node.add_child(node)
                debug_print(f"CREATED NODE AND ADDED {node} AS CHILD TO {parent}", level=3)  # DEBUGGER
        debug_print("ALL NODES ADDED TO PARENTS:", to_format=name_to_node, style="CONTAINER",
                    header="base tree", level=4)

        # Step 3: Identify the root (no parent) and set it
        for node in name_to_node.values():
            if node.parent is None:
                self.root = node
                break

    @staticmethod
    def remove_node(node):
        if node.parent is not None:
            node.parent.children.remove(node)


class MayaObjectTree(BaseTree):
    def __init__(self, item_list: any = None, node_class: Type[MayaObject] = None, _type: str = None):
        debug_print("INITIALIZING TREE", style="SECTION", header="MayaObjectTree", level=10)  # DEBUGGER
        debug_print(f"INITIALIZING TREE WITH THE FOLLOWING: CLASS: {node_class}, TYPE: {_type}, ITEMS:",
                    style="CONTAINER", to_format=item_list, header="MayaObjectTree", level=3)  # DEBUGGER
        super().__init__(item_list, node_class, _type)


if __name__ == "__main__":
    ik = IkManager()
    # ik.create_ik()
