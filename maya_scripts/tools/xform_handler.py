import math
import maya.cmds as cmds
from typing import Union

class XformHandler:
    def __init__(self, obj, threshold=1e-5):
        self.obj = obj
        self.threshold = threshold
        self.valid_attributes = self.get_all_transform_attributes()

    def __repr__(self):
        return self.get_world_space_position()

    def __str__(self):
        return (f"<XformHandler for {self.obj}>"
                f"\nPosition: {self.get_world_space_position()}")


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

    def _apply_threshold(self, value):
        return value if abs(value) > self.threshold else 0

    def get_all_transform_attributes(self):
        transform_attrs = ['translate', 'rotate', 'scale', 'jointOrient']
        return [attr for attr in cmds.listAttr(self.obj) if any(t_attr in attr for t_attr in transform_attrs)]

    def set_attribute_x(self, attribute, value):
        self.confirm_attribute_flag(attribute)
        cmds.setAttr(f"{self.obj}.{attribute}X", value)

    def set_attribute_y(self, attribute, value):
        self.confirm_attribute_flag(attribute)
        cmds.setAttr(f"{self.obj}.{attribute}Y", value)

    def set_attribute_z(self, attribute, value):
        self.confirm_attribute_flag(attribute)
        cmds.setAttr(f"{self.obj}.{attribute}Z", value)

    def set_attribute_xyz(self, attribute, value):
        self.confirm_attribute_flag(attribute)
        for i, axis in enumerate("XYZ"):
            if isinstance(value, (int, float)):
                cmds.setAttr(f"{self.obj}.{attribute}{axis}", value)
            elif isinstance(value, (tuple, list, set)) and len(value) == 1:
                cmds.setAttr(f"{self.obj}.{attribute}{axis}", value[0])
            else:
                cmds.setAttr(f"{self.obj}.{attribute}{axis}", value[i])

    def get_attribute(self, attribute):
        if attribute.endswith(("X", "Y", "Z")):
            self.confirm_attribute_flag(attribute[:-1])
        else:
            self.confirm_attribute_flag(attribute)
        return cmds.getAttr(f"{self.obj}.{attribute}")

    def set_local_space_position(self, position):
        cmds.xform(self.obj, translation=position)

    def get_local_space_position(self):
        return cmds.xform(self.obj, query=True, translation=True)

    def get_world_space_position(self):
        return cmds.xform(self.obj, query=True, worldSpace=True, translation=True)

    def set_world_space_position(self, position):
        cmds.xform(self.obj, worldSpace=True, translation=position)

    def get_world_space_rotation(self):
        return cmds.xform(self.obj, query=True, worldSpace=True, rotation=True)

    def set_world_space_rotation(self, rotation):
        cmds.xform(self.obj, worldSpace=True, rotation=rotation)

    def add(self, attribute, x:float = 0, y:float = 0, z:float = 0):
        """
        Adds the specified values to the x, y, and z components of the given attribute.

        :param attribute: The attribute to modify (e.g., 'translate', 'rotate').
        :param x: The amount to add to the x component.
        :param y: The amount to add to the y component.
        :param z: The amount to add to the z component.
        """
        attribute = self.confirm_attribute_flag(attribute)

        current_values = [self.get_attribute(f"{attribute}{axis}") for axis in "XYZ"]
        new_values = [current + delta for current, delta in zip(current_values, [x, y, z])]
        attribute = self.confirm_xform_flag(attribute)
        cmds.xform(self.obj, **{attribute: new_values})

    def calculate_vector(self, other_xform: Union['XformHandler', str]):
        pos1 = self.get_world_space_position()
        if isinstance(other_xform, XformHandler):
            pos2 = other_xform.get_world_space_position()
        else:
            pos2 = cmds.xform(other_xform, query=True, worldSpace=True, translation=True)
        return [pos2[i] - pos1[i] for i in range(3)]

    def calculate_distance(self, other_xform: Union['XformHandler', str]):
        vector = self.calculate_vector(other_xform)
        return math.sqrt(sum([v**2 for v in vector]))

    @staticmethod
    def normalize_vector(vector):
        magnitude = math.sqrt(sum([v**2 for v in vector]))
        if magnitude == 0:
            raise ValueError("Cannot normalize a vector with magnitude 0.")
        return [v / magnitude for v in vector]

    def move_relative_to_obj(self, other_xform: Union['XformHandler', str], distance):
        direction = self.calculate_vector(other_xform)
        unit_vector = self.normalize_vector(direction)
        new_pos = [self.get_world_space_position()[i] + distance * unit_vector[i] for i in range(3)]
        self.set_world_space_position(new_pos)

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
                cmds.xform(self.obj, ws=True, **{attrs: [self._apply_threshold(v) for v in final_values]})
            elif attrs == 'rotation':
                cmds.xform(self.obj, ws=True, **{attrs: [self._apply_threshold(v) for v in final_values]})
            elif attrs == 'jointOrient':
                self.set_attribute_xyz(attrs, [self._apply_threshold(v) for v in final_values])
            else:
                cmds.xform(self.obj, **{attrs: [self._apply_threshold(v) for v in final_values]})
        elif isinstance(attrs, dict):
            # Multiple attributes case
            for attr, val in attrs.items():
                attr = self.confirm_xform_flag(attr)
                if not (isinstance(val, (tuple, list, set)) and len(val) == 3):
                    raise ValueError(f"values for '{attr}' must be a tuple of three floats.")
                if attrs == 'translation':
                    cmds.xform(self.obj, ws=True, **{attr: [self._apply_threshold(v) for v in val]})
                elif attrs == 'rotation':
                    cmds.xform(self.obj, ws=True, **{attr: [self._apply_threshold(v) for v in val]})
                elif attrs == 'jointOrient':
                    self.set_attribute_xyz(attr, [self._apply_threshold(v) for v in val])
                else:
                    cmds.xform(self.obj, **{attr: [self._apply_threshold(v) for v in val]})
        else:
            raise ValueError("attrs must be a string or a dictionary.")

    def match_xform(self, src_xform: Union['XformHandler', str], attrs:list[str] | str):
        if isinstance(attrs, str):
            attrs = [attrs]

        values_to_match = {}
        if isinstance(src_xform, XformHandler):
            for attr in attrs:
                attr = self.confirm_attribute_flag(attr)
                if attr == 'translate':
                    values_to_match.update({self.confirm_xform_flag(attr): src_xform.get_world_space_position()})
                elif attr == 'rotate':
                    values_to_match.update({self.confirm_xform_flag(attr): src_xform.get_world_space_rotation()})
                elif attr == 'jointOrient':
                    src_xform.set_attribute_xyz(attr, self.get_attribute(self.confirm_attribute_flag(attr)))
                else:
                    values_to_match.update({self.confirm_xform_flag(attr): (src_xform.get_attribute(f"{self.confirm_attribute_flag(attr)}X"),
                                                   src_xform.get_attribute(f"{self.confirm_attribute_flag(attr)}Y"),
                                                   src_xform.get_attribute(f"{self.confirm_attribute_flag(attr)}Z")) for attr in attrs})
        else:
            for attr in attrs:
                if attr == 'translate':
                    values_to_match.update({attr: cmds.xform(src_xform, query=True, worldSpace=True,
                                                             translation=True)})
                if attr == 'translate':
                    values_to_match.update({attr: cmds.xform(src_xform, query=True, worldSpace=True,
                                                             rotation=True)})
                elif attr == 'jointOrient':
                    self.set_attribute_xyz(attr, (cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}X"),
                                                        cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}Y"),
                                                        cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}Z")))
                else:
                    values_to_match.update({self.confirm_xform_flag(attr):
                                                (cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}X"),
                                                 cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}Y"),
                                                 cmds.getAttr(f"{src_xform}.{self.confirm_attribute_flag(attr)}Z")) for attr in attrs})
        self.set_xform(values_to_match)

if __name__ == "__main__":
    source_xform = XformHandler("pCube1")
    target_xform = XformHandler("pCube2")
    target_xform.match_xform(source_xform, ['rotation', 'translation'])
    target_xform.match_xform(source_xform, 'scale')
    source_xform.add('rotate', x=45.0, y=30.0, z=45.0)
    source_xform.add('translate', x=0.1, y=0.1, z=0.1)
    source_xform.move_relative_to_obj(target_xform, 5.0)
    source_xform.set_xform({'translate': (0, 0, 0), 'rotate': (55, 55, 55)})
