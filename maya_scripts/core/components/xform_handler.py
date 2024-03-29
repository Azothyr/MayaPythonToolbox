import math
import maya.cmds as cmds
from typing import Union


class Calculator3dSpace:
    def __init__(self, source=None, target=None):
        # Check if the source is a valid object or XformHandler instance and assign accordingly
        if isinstance(source, XformHandler):
            self.source = source
        elif source and cmds.objExists(source):
            self.source = XformHandler(source)
        else:
            self.source = None

        # Check if the target is a valid object or XformHandler instance and assign accordingly
        if isinstance(target, XformHandler):
            self.target = target
        elif target and cmds.objExists(target):
            self.target = XformHandler(target)
        else:
            self.target = None

    @staticmethod
    def get_axis_from_vector(vector):
        match vector:
            case (1.0, 0.0, 0.0):
                return "x"
            case (-1.0, 0.0, 0.0):
                return "-x"
            case (0.0, 1.0, 0.0):
                return "y"
            case (0.0, -1.0, 0.0):
                return "-y"
            case (0.0, 0.0, 1.0):
                return "z"
            case (0.0, 0.0, -1.0):
                return "-z"
            case _:
                raise ValueError(f"Cannot determine axis from vector: {vector}")

    @staticmethod
    def get_vector_from_axis(axis):
        match axis:
            case "x":
                return 1.0, 0.0, 0.0
            case "-x":
                return -1.0, 0.0, 0.0
            case "y":
                return 0.0, 1.0, 0.0
            case "-y":
                return 0.0, -1.0, 0.0
            case "z":
                return 0.0, 0.0, 1.0
            case "-z":
                return 0.0, 0.0, -1.0
            case _:
                raise ValueError(f"Cannot determine vector from axis: {axis}")

    def calculate_comparison_vector(self, src_xform: Union['XformHandler', str] = None,
                                    other_xform: Union['XformHandler', str] = None):
        if src_xform is None:
            src_xform = self.source
        if not src_xform:
            raise ValueError("Source xform is not defined.")
        if other_xform is None:
            other_xform = self.target
        if not other_xform:
            raise ValueError("Target xform is not defined.")
        pos1 = self.source.get_world_space_position()
        if isinstance(other_xform, XformHandler):
            pos2 = other_xform.get_world_space_position()
        else:
            pos2 = cmds.xform(other_xform, query=True, worldSpace=True, translation=True)
        return [self.source.apply_threshold(pos2[i] - pos1[i]) for i in range(3)]

    def calculate_aim_axis_vector(self, src_xform: Union['XformHandler', str] = None,
                                  other_xform: Union['XformHandler', str] = None,
                                  relative_to_src: bool = False):
        if src_xform is None:
            src_xform = self.source
        if not src_xform:
            raise ValueError("Source xform is not defined.")
        if other_xform is None:
            other_xform = self.target
        # Calculate the world space direction vector of the source position to the target position
        vector = self.normalize_vector(self.calculate_comparison_vector(src_xform=src_xform, other_xform=other_xform),
                                       self.source, other_xform)
        if relative_to_src:
            # rotation_matrix = 3x3 matrix of [translation_vector, rotation_vector, scale_vector]
            rotation_matrix = self.source.get_world_space_rotation_matrix()
            # Multiply vector by rotation matrix (j=x|y|z, i=matrix row [0]->translationXYZ,
            # [1]->rotationXYZ,[2]->scaleXYZ)
            rotated_vector = [
                sum(vector[j] * round(rotation_matrix[i][j]) for j in range(3)) for i in range(3)
            ]
            # Calculation of the world space direction vector with the source's rotation accounted for
            vector = rotated_vector

        # Determine the dominant axis and its direction
        match ([abs(axis) for axis in vector].index(max([abs(axis) for axis in vector]))):
            case 0:
                x, y, z = -1.0 if vector[0] < 0.0 else 1.0, 0.0, 0.0
            case 1:
                x, y, z = 0.0, -1.0 if vector[1] < 0.0 else 1.0, 0.0
            case 2:
                x, y, z = 0.0, 0.0, -1.0 if vector[2] < 0.0 else 1.0
            case _:
                raise ValueError("Cannot determine dominant axis of aim vector.")

        return x, y, z

    def calculate_distance(self, src_xform: Union['XformHandler', str] = None,
                           other_xform: Union['XformHandler', str] = None):
        if src_xform is None:
            src_xform = self.source
        if not src_xform:
            raise ValueError("Source xform is not defined.")
        if other_xform is None:
            other_xform = self.target
        vector = self.calculate_comparison_vector(src_xform=src_xform, other_xform=other_xform)
        return math.sqrt(sum([v ** 2 for v in vector]))

    def normalize_vector(self, vector=None, src="", trgt=""):
        if vector is None:
            vector = self.calculate_comparison_vector()
        if vector[0] == vector[1] == vector[2] == 0:
            src = f":\n {src}\n" if src else ""
            trgt = f":\n {trgt}\n" if trgt else ""
            raise ValueError(
                f"Cannot calculate aim axis vector when source{src} and target{trgt} positions are the same.")
        magnitude = math.sqrt(sum([axis ** 2 for axis in vector]))
        if magnitude == 0:
            raise ValueError("Cannot normalize a vector with magnitude 0.")
        return [self.source.apply_threshold(axis / magnitude) for axis in vector]

    def calculate_local_axes_relativity_to_world(self, obj_handler=None):
        """
        Return: Dictionary of local axes and their closest world axes.
        format: {'local_axis': 'world_axis'}
        Example: {'x': 'x', '-x': '-x', 'y': 'y', '-y': '-y', 'z': 'z', '-z': '-z'}
        """
        if obj_handler is None:
            obj_handler = self.source
        rotation_matrix = obj_handler.get_world_space_rotation_matrix()
        world_axes_vectors = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        world_axes = ['x', 'y', 'z']
        result = {}

        for i, world_axis in enumerate(world_axes):
            transformed_axis = [sum(rotation_matrix[j][i] * axis[j] for j in range(3)) for axis in world_axes_vectors]
            dot_products = [sum(transformed_axis[k] * world_axes_vectors[k][i] for k in range(3)) for i in range(3)]

            objs_closest_world_axis_index = dot_products.index(max(dot_products, key=abs))
            sign = "-" if dot_products[objs_closest_world_axis_index] < 0 else ""
            rev_sign = "-" if sign == "" else ""
            # print(f"Local {world_axis}-axis is closest to World "
            #       f"{sign}{world_axes[objs_closest_world_axis_index]}-axis")
            # print(f"Local -{world_axis}-axis is closest to World "
            #       f"{rev_sign}{world_axes[objs_closest_world_axis_index]}-axis")

            result[f"{world_axis}"] = f"{sign}{world_axes[objs_closest_world_axis_index]}"
            result[f"-{world_axis}"] = f"{rev_sign}{world_axes[objs_closest_world_axis_index]}"

        return result

    def is_collinear(self, world_space_positions: list[list[float]], precision: float = 1e-5):
        """
        Check if the given world space positions are collinear.
        :param world_space_positions: List of world space positions
        :param precision: Precision of the calculation
        """
        # Get world space positions
        # Calculate vectors
        # vector1 = [pos2[i] - pos1[i] for i in range(3)]
        # vector2 = [pos3[i] - pos1[i] for i in range(3)]

        # Calculate cross product
        # cross_product = [
        #     vector1[1] * vector2[2] - vector1[2] * vector2[1],
        #     vector1[2] * vector2[0] - vector1[0] * vector2[2],
        #     vector1[0] * vector2[1] - vector1[1] * vector2[0]
        # ]

        # Calculate magnitude of the cross product
        # magnitude = math.sqrt(sum([axis ** 2 for axis in cross_product]))

        # If the magnitude is close to 0, the joints are collinear
        # return magnitude < precision
        pass


class XformHandler:
    def __init__(self, obj, threshold=1e-5, precision=3, allow_loc=True):
        if not obj:
            raise ValueError("ERROR XFORMHANDLER: Object name must be provided.")
        if not cmds.objExists(obj) and not allow_loc:
            raise ValueError(f"ERROR XFORMHANDLER: Object '{obj}' does not exist.")
        if not cmds.objExists(obj):
            obj = cmds.spaceLocator(name=obj)[0] if allow_loc else None
        self.obj = obj
        if not self.obj:
            raise ValueError(f"ERROR XFORMHANDLER: Object '{obj}' does not exist.")
        self.threshold = threshold
        self.precision = precision
        self.calc = Calculator3dSpace(self)
        self.valid_attributes = self.get_all_transform_attributes()
        self.xform_attrs = [f"{self.obj}.{attr}{axis}" for attr in ['translate', 'rotate', 'scale'] for
                            axis in 'XYZ']
        if cmds.objectType(self.obj) == 'joint':
            for axis in 'XYZ':
                self.xform_attrs.append(f"{self.obj}.jointOrient{axis}")

    def __repr__(self):
        return self.get_world_space_position()

    def __str__(self):
        return (f"<XformHandler for {self.obj}>"
                f"\nPosition: {self.get_world_space_position()}"
                f"\nRotation: {self.get_world_space_rotation()}"
                f"\nScale: {self.get_attribute('scale')}")

    def apply_threshold(self, value, debug=False):
        if isinstance(value, (tuple, list, set)):
            return type(value)(self.apply_threshold(v) for v in value)
        else:
            if value == 0:
                debug = False
            if abs(value) < self.threshold:
                if debug:
                    print(f"\tValue {value} is below threshold {self.threshold}. Setting to 0.")
                return 0
            else:
                value = round(value, self.precision)
                if 0.99 < abs(value) - abs(round(value)) < 0.01:
                    if debug:
                        print(f"\tValue {value} is close to an integer. Rounding to nearest integer.")
                    return int(round(value))
                return value

    def fix_small_values(self, debug=False):
        for attr in self.xform_attrs:
            value = cmds.getAttr(attr)
            if isinstance(value, list) or isinstance(value, tuple):
                if debug:
                    print(f"Working on {attr},\n\toriginial value: {value}")
                fixed_value = [self.apply_threshold(v, debug=debug) for v in value]
                cmds.setAttr(f"{attr}", *fixed_value)
            else:
                if debug:
                    print(f"Working on {attr},\n\toriginial value: {value}")
                fixed_value = self.apply_threshold(value, debug=debug)
                cmds.setAttr(f"{attr}", fixed_value)

    @staticmethod
    def apply_threshold_decorator(method):
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            self.fix_small_values()
            return result

        return wrapper

    def _is_valid_attribute(self, attribute):
        if attribute == 'rotation':
            attribute = 'rotate'
        elif attribute == 'translation':
            attribute = 'translate'
        if attribute not in self.valid_attributes:
            raise ValueError(f"Attribute '{attribute}' is not a valid transformation attribute for '{self.obj}'.")
        return True

    def confirm_xform_flag(self, flag):
        if flag == 'rotate':
            flag = 'rotation'
        elif flag == 'translate':
            flag = 'translation'
        self._is_valid_attribute(flag)
        return flag

    def confirm_attribute_flag(self, flag):
        if flag == 'rotation':
            flag = 'rotate'
        elif flag == 'translation':
            flag = 'translate'
        self._is_valid_attribute(flag)
        return flag

    def get_all_transform_attributes(self):
        transform_attrs = ['translate', 'rotate', 'scale', 'jointOrient']
        return [attr for attr in cmds.listAttr(self.obj) if any(t_attr in attr for t_attr in transform_attrs)]

    def get_local_to_world_axis_mapping(self):
        return self.calc.calculate_local_axes_relativity_to_world()

    @apply_threshold_decorator
    def set_attribute_x(self, attribute, value):
        self.confirm_attribute_flag(attribute)
        cmds.setAttr(f"{self.obj}.{attribute}X", self.apply_threshold(value))

    @apply_threshold_decorator
    def set_attribute_y(self, attribute, value):
        self.confirm_attribute_flag(attribute)
        cmds.setAttr(f"{self.obj}.{attribute}Y", self.apply_threshold(value))

    @apply_threshold_decorator
    def set_attribute_z(self, attribute, value):
        self.confirm_attribute_flag(attribute)
        cmds.setAttr(f"{self.obj}.{attribute}Z", self.apply_threshold(value))

    @apply_threshold_decorator
    def set_attribute_xyz(self, attribute, value):
        self.confirm_attribute_flag(attribute)
        if isinstance(value, (int, float)):
            value = self.apply_threshold(value)
            for axis in "XYZ":
                cmds.setAttr(f"{self.obj}.{attribute}{axis}", value)
        elif isinstance(value, (tuple, list, set)) and len(value) == 1:
            single_value = self.apply_threshold(value[0])
            for axis in "XYZ":
                cmds.setAttr(f"{self.obj}.{attribute}{axis}", single_value)
        else:
            for i, axis in enumerate("XYZ"):
                cmds.setAttr(f"{self.obj}.{attribute}{axis}", self.apply_threshold(value[i]))

    def get_attribute(self, attribute):
        if attribute.endswith(("X", "Y", "Z")):
            self.confirm_attribute_flag(attribute[:-1])
        else:
            self.confirm_attribute_flag(attribute)
        return cmds.getAttr(f"{self.obj}.{attribute}")

    @apply_threshold_decorator
    def set_local_space_position(self, position):
        cmds.xform(self.obj, translation=[self.apply_threshold(v) for v in position])

    def get_local_space_position(self):
        return [self.apply_threshold(v) for v in cmds.xform(self.obj, query=True, translation=True)]

    def get_world_space_position(self):
        return [self.apply_threshold(v) for v in cmds.xform(self.obj, query=True, worldSpace=True,
                                                            translation=True)]

    @apply_threshold_decorator
    def set_world_space_position(self, position):
        position = [self.apply_threshold(coord) for coord in position]
        cmds.xform(self.obj, worldSpace=True, translation=position)

    def get_world_space_rotation(self):
        return [self.apply_threshold(v) for v in cmds.xform(self.obj, query=True, worldSpace=True,
                                                            rotation=True)]

    @apply_threshold_decorator
    def set_world_space_rotation(self, rotation):
        rotation = [self.apply_threshold(angle) for angle in rotation]
        cmds.xform(self.obj, worldSpace=True, rotation=rotation)

    def get_world_space_rotation_matrix(self):
        # Query the transformation matrix of the object in world space
        transform_matrix = cmds.xform(self.obj, query=True, worldSpace=True, matrix=True)

        # Extract the rotation matrix (upper 3x3 part of the 4x4 transformation matrix)
        rotation_matrix = [transform_matrix[i:i + 3] for i in range(0, 9, 4)]
        return rotation_matrix

    @apply_threshold_decorator
    def add_in_world(self, attribute, x: float = 0, y: float = 0, z: float = 0):
        attribute = self.confirm_attribute_flag(attribute)
        current_values = [self.get_attribute(f"{attribute}{axis}") for axis in "XYZ"]
        new_values = [self.apply_threshold(current + delta) for current, delta in zip(current_values, [x, y, z])]
        attribute = self.confirm_xform_flag(attribute)
        cmds.xform(self.obj, worldSpace=True, relative=True, **{attribute: new_values})

    @apply_threshold_decorator
    def add_in_local(self, attribute, x: float = 0, y: float = 0, z: float = 0):
        attribute = self.confirm_xform_flag(attribute)
        x, y, z = [self.apply_threshold(value) for value in [x, y, z]]

        if attribute in ['translate', 'translation']:
            cmds.move(x, y, z, self.obj, relative=True, worldSpaceDistance=True, objectSpace=True)
        elif attribute in ['rotate', 'rotation']:
            cmds.rotate(x, y, z, self.obj, relative=True, objectSpace=True)
        else:
            cmds.xform(self.obj, relative=True, **{attribute: [x, y, z]})

    @apply_threshold_decorator
    def move_relative_to_obj(self, other_xform: Union['XformHandler', str], distance):
        direction = self.calc.calculate_comparison_vector(other_xform=other_xform)
        unit_vector = self.calc.normalize_vector(vector=direction, src=self.obj, trgt=other_xform)
        new_pos = [self.apply_threshold(self.get_world_space_position()[i] + distance * unit_vector[i]
                                        ) for i in range(3)]
        self.set_world_space_position(new_pos)

    @apply_threshold_decorator
    def set_xform(self, attrs, values=None, zero_out=False):
        if isinstance(attrs, str):
            # Single attribute case
            if values:
                if not (isinstance(values, tuple) and len(values) == 3):
                    raise ValueError("values must be a tuple of three floats.")
                final_values = values
            elif zero_out:
                final_values = (0, 0, 0)
            else:
                final_values = (self.get_attribute(f"{self.confirm_attribute_flag(attrs)}{axis}") for axis in 'XYZ')

            attrs = self.confirm_xform_flag(attrs)
            if attrs == 'translation':
                cmds.xform(self.obj, ws=True, **{attrs: [self.apply_threshold(v) for v in final_values]})
            elif attrs == 'rotation':
                cmds.xform(self.obj, ws=True, **{attrs: [self.apply_threshold(v) for v in final_values]})
            elif attrs == 'jointOrient':
                self.set_attribute_xyz(attrs, [self.apply_threshold(v) for v in final_values])
            else:
                cmds.xform(self.obj, **{attrs: [self.apply_threshold(v) for v in final_values]})
        elif isinstance(attrs, dict):
            # Multiple attributes case
            for attr, val in attrs.items():
                attr = self.confirm_xform_flag(attr)
                if not (isinstance(val, (tuple, list, set)) and len(val) == 3):
                    raise ValueError(f"values for '{attr}' must be a tuple of three floats.")
                if attr == 'translation':
                    cmds.xform(self.obj, ws=True, **{attr: [self.apply_threshold(v) for v in val]})
                elif attr == 'rotation':
                    cmds.xform(self.obj, ws=True, **{attr: [self.apply_threshold(v) for v in val]})
                elif attr == 'jointOrient':
                    self.set_attribute_xyz(attr, [self.apply_threshold(v) for v in val])
                else:
                    cmds.xform(self.obj, **{attr: [self.apply_threshold(v) for v in val]})
        elif isinstance(attrs, list):
            for attr in attrs:
                if isinstance(attr, str):
                    if zero_out:
                        self.set_xform(attr, zero_out=True)
                    else:
                        self.set_xform(attr)
                else:
                    raise ValueError("attrs must be a string, list of strings or a dictionary.")
        else:
            raise ValueError("attrs must be a string, list of strings or a dictionary.")

    @apply_threshold_decorator
    def match_xform(self, src_xform: Union['XformHandler', str], attrs: list[str] | str):
        """
        Match the transformation of the source object to the target object.

        :param src_xform: Source object to match the transformation to.
        Accepts either a string maya object name or an XformHandler
        :param attrs: List of attributes to match.
        If a string is given, it will match a single attribute. Accepted values are:
        'translate', 'translation', 'rotate', 'rotation', 'scale', 'jointOrient'
        """
        if isinstance(attrs, str):
            attrs = [attrs]

        values_to_match = {}
        if isinstance(src_xform, XformHandler):
            for attr in attrs:
                attr = self.confirm_attribute_flag(attr)
                if attr in ['translate', 'translation']:
                    values_to_match.update({self.confirm_xform_flag(attr): [self.apply_threshold(v) for v in
                                                                            src_xform.get_world_space_position()]})
                elif attr in ['rotate', 'rotation']:
                    values_to_match.update({self.confirm_xform_flag(attr): [self.apply_threshold(v) for v in
                                                                            src_xform.get_world_space_rotation()]})
                elif attr == 'jointOrient':
                    src_xform.set_attribute_xyz(attr, self.get_attribute(self.confirm_attribute_flag(attr)))
                else:
                    values_to_match.update({self.confirm_xform_flag(attr): (
                        self.apply_threshold(src_xform.get_attribute(f"{self.confirm_attribute_flag(attr)}X")),
                        self.apply_threshold(src_xform.get_attribute(f"{self.confirm_attribute_flag(attr)}Y")),
                        self.apply_threshold(src_xform.get_attribute(f"{self.confirm_attribute_flag(attr)}Z"))
                    ) for attr in attrs})
        else:
            for attr in attrs:
                if attr in ['translate', 'translation']:
                    values_to_match.update({attr: [self.apply_threshold(v) for v in cmds.xform(
                        src_xform, query=True, worldSpace=True, translation=True)]})
                elif attr in ['rotate', 'rotation']:
                    values_to_match.update({attr: [self.apply_threshold(v) for v in cmds.xform(
                        src_xform, query=True, worldSpace=True, rotation=True)]})
                elif attr == 'jointOrient':
                    self.set_attribute_xyz(attr, (
                        self.apply_threshold(cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}X")),
                        self.apply_threshold(cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}Y")),
                        self.apply_threshold(cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}Z"))))
                else:
                    values_to_match.update({self.confirm_xform_flag(attr): (
                        self.apply_threshold(cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}X")),
                        self.apply_threshold(cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}Y")),
                        self.apply_threshold(cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}Z"))
                    ) for attr in attrs})
        self.set_xform(values_to_match)


if __name__ == "__main__":
    debug = False
    # # Example of usage moving a source object relative to a target object
    # source_xform = XformHandler("pCube1")
    # target_xform = XformHandler("pSphere1")
    # calculator = Calculator3dSpace(source_xform, target_xform)
    # print(calculator.calculate_aim_axis_vector(relative_to_src=True))
    # source_xform.add_in_local('rotate', x=45.0, y=180.0, z=45.0)
    # target_xform.match_xform(source_xform, ['rotation', 'translation'])
    # target_xform.match_xform(source_xform, 'scale')
    # source_xform.add_in_world('translate', x=0.1, y=0.1, z=0.1)
    # source_xform.move_relative_to_obj(target_xform, 5.0)
    # source_xform.set_xform({'translate': (0, 0, 0), 'rotate': (55, 55, 55)})

    # Example of usage fixing small values on joints
    # selection = cmds.ls(type="joint")
    #
    # for joint in selection:
    #     jnt = XformHandler(joint, precision=2)
    #     jnt.fix_small_values(debug=debug)

    if debug:
        print("COMPLETE")
