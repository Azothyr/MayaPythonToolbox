import sys

if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' in sys.path:
    sys.path.remove('C:/GitRepos/MayaPythonToolbox/maya_scripts')
if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' not in sys.path:
    sys.path.append('C:/GitRepos/MayaPythonToolbox/maya_scripts')
import maya.cmds as cmds
from pprint import pprint

# import re

debug_bool = False


def debug(text: str, _debug: bool = False, pretty: bool = False):
    if debug_bool or _debug:
        if pretty:
            pprint(f"{text}")
        else:
            print(f"{text}")


def duplicate_geo(obj: str, new_name: str = None, prefix: str = "", suffix: str = ""):
    if not cmds.objExists(obj):
        print(f"Object {obj} does not exist")
        return None
    if new_name is not None and cmds.objExists(new_name):
        return new_name

    new_obj_name = f"{prefix}{obj}{suffix}" if new_name is None else f"{prefix}{new_name}{suffix}"
    new_obj = cmds.duplicate(obj, name=new_obj_name)[0]

    default_layer = "Blend_Shape_Layer"
    if not cmds.objExists(default_layer):
        default_layer = cmds.createDisplayLayer(name=default_layer, empty=True)

    cmds.editDisplayLayerMembers(default_layer, new_obj)

    return new_obj


def set_driven_key(bs_mesh: str, driver: str, driver_value: float, fit01_value: float, in_tan: str = "spline",
                   out_tan: str = "spline"):
    cmds.setDrivenKeyframe(bs_mesh, currentDriver=driver, driverValue=driver_value, value=fit01_value,
                           inTangentType=in_tan, outTangentType=out_tan)


def setup_corrective_meshes(meshes: list, mesh_count: int = 0):
    for mesh in meshes:
        for attr in ["translate", "rotate", "scale"]:
            for axis in "XYZ":
                cmds.setAttr(f"{mesh}.{attr}{axis}", lock=False)
        if "wrap" in mesh.lower():
            mesh_count -= 1
        cmds.xform(mesh, translation=(0, 0, -200 - (100 * mesh_count)))
        mesh_count += 1


def create_attr(node, attr_name, attr_type: str = None, min_val: int = None, max_val: int = None,
                default_val: int = None):
    debug(f"Creating attribute {attr_name} on {node}")
    attr_type = attr_type if attr_type else "float"
    unchanging_kwargs = {"longName": attr_name, "attributeType": attr_type,
                         "keyable": True, "readable": True, "writable": True}

    if not cmds.attributeQuery(attr_name, node=node, exists=True):
        default_val = default_val if default_val else 0
        unchanging_kwargs["defaultValue"] = default_val
        if min_val is not None:
            unchanging_kwargs["minValue"] = min_val
        if max_val is not None:
            unchanging_kwargs["maxValue"] = max_val

        debug(f"Creating attribute {attr_name} on {node} with type {attr_type}, min, max, default: "
              f"{min_val}, {max_val}, {default_val}")
        cmds.addAttr(node, **unchanging_kwargs)
    else:
        debug(f"Attribute {attr_name} already exists on {node}")


class UtilityNode:
    def __init__(self, node_name: str, type: str, operation: int = 0):
        self.debug = True
        debug(f"Creating node {node_name}", self.debug)
        self.node_name = node_name

        if not cmds.objExists(node_name):
            self.node_type = self.__set_type(type)
            self.operation = self.__set_operation(operation)
            self.node = self._create_node(self.node_type, self.node_name)
        else:
            self.node = node_name
            self.node_type = cmds.nodeType(self.node)
            self.operation = cmds.getAttr(f"{self.node}.operation")

    def __repr__(self):
        return self.node_name

    @staticmethod
    def __set_type(type=None):
        if type is None:
            raise ValueError("Node type cannot be None")

        lower_type = type.lower()
        match lower_type:
            case "multiplydivide": return "multiplyDivide"
            case "md": return "multiplyDivide"
            case "plusminusaverage": return "plusMinusAverage"
            case "pma": return "plusMinusAverage"
            case "condition": return "condition"
            case "cond": return "condition"
            case "distancebetween": return "distanceBetween"
            case "db": return "distanceBetween"
            case "dist": return "distanceBetween"
            case "reverse": return "reverse"
            case "rev": return "reverse"
            case "clamp": return "clamp"
            case "cl": return "clamp"

    def __set_operation(self, operation: int | str):
        md = [None, "multiply", "divide", "power"]
        pma = [None, "sum", "subtract", "average"]

        try:
            match self.node_type:
                case "multiplyDivide": return md.index(operation) if isinstance(operation, str) else md[operation]
                case "plusMinusAverage": return pma.index(operation) if isinstance(operation, str) else pma[operation]
                case "distanceBetween": return None
                case "reverse": return None
                case "clamp": return None
        except IndexError:
            return None

    @staticmethod
    def _create_node(node_type, node_name):
        if cmds.objExists(node_name):
            node = node_name
        else:
            node = cmds.shadingNode(node_type, name=node_name, asUtility=True)
        return node


class NodeManager(UtilityNode):
    def __init__(self, node_name: str, type: str, operation: int = 0):
        self.debug = True
        super().__init__(node_name, type, operation)

    def attr_exists(self, attr_name: str, node=None):
        node = self.node if node is None else node
        if "[" in attr_name:
            return cmds.attributeQuery(attr_name.split("[")[0], node=node, exists=True)
        return cmds.attributeQuery(attr_name, node=node, exists=True)

    def set_attr(self, attr_name: str, attr_value: float):
        if self.attr_exists(attr_name):
            cmds.setAttr(f"{self.node}.{attr_name}", attr_value)

    def get_attr(self, attr_name: str):
        return cmds.getAttr(f"{self.node}.{attr_name}")

    def connect_attr(self, attr_name: str, other_node: 'str | NodeManager', other_attr: str, direction: str = "out"):
        if isinstance(other_node, NodeManager):
            other_node = other_node.node_name
        try:
            if self.attr_exists(attr_name):
                match direction.lower():
                    case "out":
                        if self.attr_exists(other_attr, other_node):
                            debug(f"ATTEMPT: {self.node}.{attr_name} to {other_node}.{other_attr}", self.debug)
                            cmds.connectAttr(f"{self.node}.{attr_name}", f"{other_node}.{other_attr}", force=True)
                        else:
                            debug(f"\t>>>FAILED: Attribute {other_attr} does not exist on {other_node}<<<\n", self.debug)
                            debug(f"OPTIONS: {cmds.listAttr(other_node)}\n", self.debug, pretty=True)
                    case "in":
                        if self.attr_exists(other_attr, other_node):
                            debug(f"ATTEMPT: {other_node}.{other_attr} to {self.node}.{attr_name}", self.debug)
                            cmds.connectAttr(f"{other_node}.{other_attr}", f"{self.node}.{attr_name}", force=True)
                        else:
                            debug(f"\t>>>FAILED: Attribute {other_attr} does not exist on {other_node}<<<\n", self.debug)
                            debug(f"options: {cmds.listAttr(other_node)}\n", self.debug, pretty=True)
                    case _:
                        debug(f"\tERROR: Direction {direction} not recognized\n", self.debug)
            else:
                debug(f"NODE ERROR: Attribute {attr_name} does not exist on {self.node}<<<\n", self.debug)
                return
            debug(f"\t>>>SUCCESS: Connected {self.node}.{attr_name} to {other_node}.{other_attr}<<<\n", self.debug)

        except RuntimeError as e:
            match direction.lower():
                case "out":
                    debug(f"~~~~~~~RUNTIME ERROR: {self.node}.{attr_name} to {other_node}.{other_attr}~~~~~~~\n\n"
                          f"-------FROM MAYA:\n{e}-------\n", self.debug)
                case "in":
                    debug(f"~~~~~~~RUNTIME ERROR: {other_node}.{other_attr} to {self.node}.{attr_name}~~~~~~~\n\n"
                          f"-------FROM MAYA:\n{e}-------\n", self.debug)
                case _:
                    debug(f"~~~~~~~RUNTIME ERROR: Direction {direction} not recognized~~~~~~~\n"
                          f"-------FROM MAYA:\n{e}-------\n", self.debug)

    def disconnect_attr(self, attr_name: str, other_node: str, other_attr: 'str | NodeManager'):
        if self.attr_exists(attr_name):
            if self.attr_exists(other_attr) and cmds.objExists(other_node):
                cmds.disconnectAttr(f"{self.node}.{attr_name}", f"{other_node}.{other_attr}")

    def delete_node(self):
        if cmds.objExists(self.node):
            cmds.delete(self.node)

    def list_connections(self, attr_name: str):
        return cmds.listConnections(f"{self.node}.{attr_name}", plugs=True)

    def list_attr(self):
        return cmds.listAttr(self.node)


class BlendShapeManager:
    def __init__(self, name: str, source: str, targets: list):
        self.debug = True
        self.name = name
        self.source = source
        self.targets = self.find_blend_shape_targets()
        self.current_targets = targets
        self.skin_cluster = self.__get_skin_cluster()
        self.blend_shape = self.__create_blend_shape()

    def __repr__(self):
        return self.name

    def __get_skin_cluster(self):
        deformers = cmds.listHistory(self.source)
        if deformers:
            for obj in deformers:
                if cmds.nodeType(obj) == "skinCluster":
                    return obj
        return None

    def __create_blend_shape(self):
        if not cmds.objExists(self.name):
            debug(f"Creating blend shape {self.name} with targets: {self.current_targets}", self.debug)
            blend_shape = cmds.blendShape(*self.current_targets, self.source, name=self.name, topologyCheck=True)
            self.targets.extend(self.current_targets)
        else:
            debug(f"Blend shape {self.name} already exists", self.debug)
            blend_shape = [self.name]
        self.blend_shape = blend_shape
        self.__fix_deformer_order()
        return blend_shape

    def __fix_deformer_order(self):
        for target in self.targets:
            self.set_weight(target, 0)

        for target in self.current_targets:
            if target not in self.targets:
                cmds.blendShape(self.name, edit=True, target=(self.source, len(self.targets)+1, target, 1),
                                topologyCheck=True)
                self.targets.append(target)
        if not self.skin_cluster:
            return
        if cmds.findDeformers(self.source)[0] != self.skin_cluster and self.skin_cluster in cmds.findDeformers(
                self.source):
            deformers = cmds.findDeformers(self.source)
            deformers.pop(deformers.index(self.skin_cluster))
            deformers.insert(0, self.skin_cluster)
            for i in range(len(deformers) - 1):
                cmds.reorderDeformers(deformers[i], deformers[i + 1], self.source)

    @staticmethod
    def find_blend_shapes(geometry):
        """
        Find all blend shape nodes associated with a geometry.

        Args:
        - geometry (str): The name of the geometry.

        Returns:
        - list: A list of blend shape node names.
        """
        # Get the construction history of the geometry
        history = cmds.listHistory(geometry)

        # Filter out the blend shape nodes from the history
        blend_shapes = [node for node in history if cmds.nodeType(node) == "blendShape"]

        return blend_shapes

    def find_blend_shape_targets(self):
        """
        Find all blend shape target names (weights) for a given blend shape node.

        Args:
        - blend_shape_node (str): The name of the blend shape node.

        Returns:
        - list: A list of blend shape target names.
        """
        targets = []
        for node in self.find_blend_shapes(self.source):
            # Get the list of aliases for the blend shape node which includes the target names
            aliases = cmds.aliasAttr(node, query=True)

            # The aliases list is a flat list with the structure [alias, attribute, alias, attribute, ...]
            # The target names are every second element in the list, starting at index 0
            target_names = aliases[0::2]  # This slices the list to get every second element, starting from the first
            targets.extend(target_names)

        return targets

    def set_weight(self, target: int | str, weight: float):
        if isinstance(target, str):
            if target in self.targets:
                target = self.targets.index(target)
            else:
                raise RuntimeError(f"Target {target} not found in blend shape {self.blend_shape}")
        cmds.blendShape(self.blend_shape, edit=True, w=(target, weight), topologyCheck=True)

    def mirror(self, mesh: str, dest_mesh: str, axis: str = "X"):
        # Broken for now
        if mesh not in self.source:
            raise RuntimeError(f"Mesh {mesh} not found in blend shape {self.name}")
        for target in self.targets:
            self.set_weight(target, 0)
        cmds.setAttr(f"{mesh}.scale{axis.upper()}", -1)
        # Select the driven mesh first, then the driver mesh
        cmds.select(dest_mesh, mesh)

    def add_target(self, target: str):
        if target not in self.targets:
            self.targets.append(target)
            cmds.blendShape(self.name, edit=True, target=(self.source, len(self.targets), target, 1),
                            topologyCheck=True)
        else:
            debug(f"Target {target} already exists in blend shape {self.name}", self.debug)


def bicep_version():
    def run_tool(obj, attr, mode="", *args, **kwargs):
        _debug = True if internal_debug else False
        match mode:
            case "create_attr":
                if attr is None:
                    debug(f"attribute not specified to create on {obj}")
                    return
                debug(f"mode: {mode}", _debug)
                create_attr(obj, attr, *args, **kwargs)
            case "create_node":
                debug(f"mode: {mode}", _debug)
                node = NodeManager(obj, type=attr, *args, **kwargs)
                debug(f"node: {node}", _debug)
                return node
            case _:
                debug(f"Incorrect mode: {mode}", _debug)
                pass

    obj = "COG_FK_Ctrl"
    part1 = "Arm"
    part2 = "Shirt"
    side = "L"
    rev_side = "R"
    transfer_dir = "LtoR"
    purpose = "Bicep_Flex"

    blend_shape1 = f"{part1}_BS"
    blend_shape2 = f"{part2}_BS"

    initial_mesh1 = "Body_Geo"
    initial_mesh2 = "Shirt_Geo"

    joint1 = f"{side}_{part1}_02_RK_Jnt"
    joint2 = f"{rev_side}_{part1}_02_RK_Jnt"
    ctrl1 = f"{side}_{part1}_02_FK_Ctrl"
    ctrl2 = f"{rev_side}_{part1}_02_FK_Ctrl"

    blend_shape_weight01 = f"{side}_{part1}_{purpose}"
    blend_shape_weight02 = f"{rev_side}_{part1}_{purpose}"
    blend_shape_weight11 = f"{side}_{part2}_{purpose}"
    blend_shape_weight12 = f"{rev_side}_{part2}_{purpose}"
    blend_shape_node01 = f"{blend_shape1}_{blend_shape_weight01}"  # L part 1
    blend_shape_node02 = f"{blend_shape1}_{blend_shape_weight02}"  # R part 1
    blend_shape_node11 = f"{blend_shape2}_{blend_shape_weight11}"  # L part 2
    blend_shape_node12 = f"{blend_shape2}_{blend_shape_weight12}"  # R part 2

    init_driver_val = 35
    term_driver_val = 85
    # Left Side
    # set_driven_key(f"{blend_shape1}.{blend_shape_weight01}", f"{joint1}.rotateZ",
    #                init_driver_val, 0)
    # set_driven_key(f"{blend_shape2}.{blend_shape_weight11}", f"{joint1}.rotateZ",
    #                init_driver_val, 0)
    # set_driven_key(f"{blend_shape1}.{blend_shape_weight01}", f"{joint1}.rotateZ",
    #                term_driver_val, 1)
    # set_driven_key(f"{blend_shape2}.{blend_shape_weight11}", f"{joint1}.rotateZ",
    #                term_driver_val, 1)
    # cmds.setAttr(f"{ctrl1}.rotateZ", term_driver_val)
    # exit("COMPLETED SECTION")

    # # Run this only if you need to create the blend shape
    # cmds.select(corrective_mesh)
    # cmds.selectMode(component=True)
    # cmds.selectType(vertex=True)

    # secondary_blend_shape.mirror(wrap_mesh, rev_corrective_mesh)
    # primary_blend_shape.add_target(rev_corrective_mesh)

    # Right Side
    # set_driven_key(f"{blend_shape1}.{blend_shape_weight02}", f"{joint2}.rotateZ",
    #                init_driver_val, 0)
    # set_driven_key(f"{blend_shape2}.{blend_shape_weight12}", f"{joint2}.rotateZ",
    #                init_driver_val, 0)
    # set_driven_key(f"{blend_shape1}.{blend_shape_weight02}", f"{joint2}.rotateZ",
    #                term_driver_val, 1)
    # set_driven_key(f"{blend_shape2}.{blend_shape_weight12}", f"{joint2}.rotateZ",
    #                term_driver_val, 1)
    # cmds.setAttr(f"{ctrl2}.rotateZ", term_driver_val)
    # exit("COMPLETED SECTION")
    # cmds.setAttr(f"{ctrl1}.rotateZ", 0)
    # cmds.setAttr(f"{ctrl2}.rotateZ", 0)
    # exit("COMPLETED SECTION")

    # corrective_mesh1 = duplicate_geo(initial_mesh1, blend_shape_weight01)
    # rev_corrective_mesh1 = duplicate_geo(initial_mesh1, blend_shape_weight02)
    # wrap_mesh1 = duplicate_geo(initial_mesh1, f"{part1}_Wrap")
    #
    # corrective_mesh2 = duplicate_geo(initial_mesh2, blend_shape_weight11)
    # rev_corrective_mesh2 = duplicate_geo(initial_mesh2, blend_shape_weight12)
    # wrap_mesh2 = duplicate_geo(initial_mesh2, f"{part2}_Wrap")
    #
    # setup_corrective_meshes([corrective_mesh1, rev_corrective_mesh1, wrap_mesh1], mesh_count=5)
    #
    # setup_corrective_meshes([corrective_mesh2, rev_corrective_mesh2, wrap_mesh2], mesh_count=5)

    # primary_blend_shape1 = BlendShapeManager(blend_shape1, initial_mesh1, [corrective_mesh1])
    # primary_blend_shape2 = BlendShapeManager(blend_shape2, initial_mesh2, [corrective_mesh2])
    # secondary_blend_shape1 = BlendShapeManager(f"{transfer_dir}_{wrap_mesh1}", wrap_mesh1, [corrective_mesh1])
    # secondary_blend_shape2 = BlendShapeManager(f"{transfer_dir}_{wrap_mesh2}", wrap_mesh2, [corrective_mesh2])
    # exit("COMPLETED SECTION")

    attr1 = "FlexSwitch"
    attr2 = "ManualFlex"

    channel_attr1 = f"{part1}_{attr1}"
    channel_attr2 = f"{side}_{part1}_{attr2}"
    channel_attr3 = f"{rev_side}_{part1}_{attr2}"
    # run_tool(obj, channel_attr1, "create_attr", min_val=0, max_val=1)
    # run_tool(obj, channel_attr2, "create_attr")
    # run_tool(obj, channel_attr3, "create_attr")
    # exit("COMPLETED SECTION")

    node1 = run_tool(f"{channel_attr1}_MD", "md", operation=1, mode="create_node")
    node2 = run_tool(f"{channel_attr2}_PMA", "pma", operation=1, mode="create_node")
    node3 = run_tool(f"{channel_attr3}_PMA", "pma", operation=1, mode="create_node")

    # Left Side
    node1.connect_attr("input1X", blend_shape_node01, "output", direction="in")
    node1.connect_attr("input2X", obj, channel_attr1, direction="in")
    node2.connect_attr("input2D[0].input2Dx", obj, channel_attr2, direction="in")
    node1.connect_attr("outputX", node3, "input2D[1].input2Dx")
    node2.connect_attr("output2Dx", blend_shape1, blend_shape_weight01)  # L Arm
    node2.connect_attr("output2Dx", blend_shape2, blend_shape_weight02)  # R Arm

    # Right Side
    node1.connect_attr("input1Y", blend_shape_node11, "output", direction="in")
    node1.connect_attr("input2Y", obj, channel_attr1, direction="in")
    node3.connect_attr("input2D[0].input2Dy", obj, channel_attr2, direction="in")
    node1.connect_attr("outputY", node3, "input2D[1].input2Dy")
    node3.connect_attr("output2Dy", blend_shape1, blend_shape_weight11)
    node3.connect_attr("output2Dy", blend_shape2, blend_shape_weight12)
    exit("COMPLETED SECTION")


def elbow_version():
    # print(cmds.blendShape("Elbow_BS", q=True, target=True))
    initial_mesh = "Body_Geo"

    side = "L"
    rev_side = "R"
    transfer_dir = "LtoR"
    part = "Arm"
    joint1 = f"{side}_{part}_02_RK_Jnt"
    joint2 = f"{rev_side}_{part}_02_RK_Jnt"

    corrective_mesh = duplicate_geo(initial_mesh, f"{side}_{part}_Corrective")
    rev_corrective_mesh = duplicate_geo(initial_mesh, f"{rev_side}_{part}_Corrective")
    wrap_mesh = duplicate_geo(initial_mesh, f"{part}_Wrap")

    meshes = [corrective_mesh, rev_corrective_mesh, wrap_mesh]
    setup_corrective_meshes([rev_corrective_mesh, wrap_mesh])
    primary_blend_shape = BlendShapeManager(
        f"{part}_BS", initial_mesh, [corrective_mesh])

    init_driver_val = 35
    term_driver_val = 85

    set_driven_key(f"{primary_blend_shape}.{corrective_mesh}", f"{joint1}.rotateZ",
                   init_driver_val, 0)
    set_driven_key(f"{primary_blend_shape}.{corrective_mesh}", f"{joint1}.rotateZ",
                   term_driver_val, 1)
    cmds.setAttr(f"{joint1}.rotateZ", term_driver_val)

    # # Run this only if you need to create the blend shape
    # cmds.select(corrective_mesh)
    # cmds.selectMode(component=True)
    # cmds.selectType(vertex=True)

    # secondary_blend_shape.mirror(wrap_mesh, rev_corrective_mesh)
    # primary_blend_shape.add_target(rev_corrective_mesh)

    set_driven_key(f"{primary_blend_shape}.{rev_corrective_mesh}", f"{joint2}.rotateZ",
                   init_driver_val, 0)
    set_driven_key(f"{primary_blend_shape}.{rev_corrective_mesh}", f"{joint2}.rotateZ",
                   term_driver_val, 1)
    cmds.setAttr(f"{joint2}.rotateZ", term_driver_val)


if __name__ == "__main__":
    internal_debug = True

    def module_name():
        import inspect
        import os
        # Get the current frame and find the file name of the script
        frame = inspect.currentframe()
        filename = inspect.getfile(frame)
        return os.path.basename(filename).split('.')[0]


    l_spacer = "-" * 25 + "|" + " " * 4
    r_spacer = " " * 4 + "|" + "-" * 25
    debug(f"\n{l_spacer} RUNNING {module_name()} DUNDER MAIN {r_spacer}", internal_debug)

    bicep_version()
    # elbow_version()

    debug(f"\n{l_spacer} COMPLETED {module_name()} DUNDER MAIN {r_spacer}", internal_debug)
