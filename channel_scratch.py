import math
from PySide2.QtWidgets import QGridLayout
from PySide2.QtCore import QTimer
from PySide2 import QtWidgets, QtCore
import random
import maya.cmds as cmds


class ChannelBox:
    def __init__(self):
        self.world_fields = []
        self.rotation_fields = []
        self.scale_fields = []

    # Get coordinates for the selected object
    @staticmethod
    def get_coordinates(object_name):
        if ".vtx[" in object_name:
            world_coords = cmds.pointPosition(object_name, w=True)
        else:
            world_coords = cmds.xform(object_name, query=True, worldSpace=True, translation=True)
        return world_coords

    # Set a single coordinate for the selected object
    @staticmethod
    def set_single_coordinate(object_name, index, value):
        if ".vtx[" in object_name:
            current_coords = cmds.pointPosition(object_name, w=True)
            current_coords[index] = value
            cmds.xform(object_name, ws=True, t=current_coords)
        else:
            current_coords = list(cmds.getAttr(f"{object_name}.translate")[0])
            current_coords[index] = value
            cmds.xform(object_name, ws=True, t=current_coords)

    @staticmethod
    def get_rotation(object_name):
        return cmds.xform(object_name, query=True, worldSpace=True, rotation=True)

    @staticmethod
    def set_single_rotation(object_name, index, value):
        current_rotation = list(cmds.getAttr(f"{object_name}.rotate")[0])
        current_rotation[index] = value
        cmds.xform(object_name, ws=True, ro=current_rotation)

    @staticmethod
    def get_scale(object_name):
        return cmds.xform(object_name, query=True, worldSpace=True, scale=True)

    @staticmethod
    def set_single_scale(object_name, index, value):
        current_scale = list(cmds.getAttr(f"{object_name}.scale")[0])
        current_scale[index] = value
        cmds.xform(object_name, ws=True, s=current_scale)

    # Update UI with coordinates of the selected object
    def update_ui(self, *args):
        selected_objects = cmds.ls(selection=True, long=True)
        if not selected_objects:
            return
        object_name = selected_objects[0]
        world_coords = self.get_coordinates(object_name)
        for i in range(3):
            cmds.floatField(self.world_fields[i], edit=True, value=world_coords[i])

        selected_objects = cmds.ls(selection=True, long=True)
        if not selected_objects:
            return
        object_name = selected_objects[0]
        rotation_coords = self.get_rotation(object_name)
        for i in range(3):
            cmds.floatField(self.rotation_fields[i], edit=True, value=rotation_coords[i])

        scale_coords = self.get_scale(object_name)
        for i in range(3):
            cmds.floatField(self.scale_fields[i], edit=True, value=scale_coords[i])

    # Apply changes to X, Y, and Z coordinates
    def apply_x_coordinate(self, *args):
        self.apply_single_coordinate(0)

    def apply_y_coordinate(self, *args):
        self.apply_single_coordinate(1)

    def apply_z_coordinate(self, *args):
        self.apply_single_coordinate(2)

    def apply_single_coordinate(self, index):
        selected_objects = cmds.ls(selection=True, long=True)
        if not selected_objects:
            return
        object_name = selected_objects[0]
        value = cmds.floatField(self.world_fields[index], query=True, value=True)
        self.set_single_coordinate(object_name, index, value)

        # Apply changes to X, Y, and Z for rotation
    def apply_rotation_x(self, *args):
        self.apply_single_rotation(0)

    def apply_rotation_y(self, *args):
        self.apply_single_rotation(1)

    def apply_rotation_z(self, *args):
        self.apply_single_rotation(2)

    def apply_single_rotation(self, index):
        selected_objects = cmds.ls(selection=True, long=True)
        if not selected_objects:
            return
        object_name = selected_objects[0]
        value = cmds.floatField(self.rotation_fields[index], query=True, value=True)
        self.set_single_rotation(object_name, index, value)

    # Apply changes to X, Y, and Z for scale
    def apply_scale_x(self, *args):
        self.apply_single_scale(0)

    def apply_scale_y(self, *args):
        self.apply_single_scale(1)

    def apply_scale_z(self, *args):
        self.apply_single_scale(2)

    def apply_single_scale(self, index):
        selected_objects = cmds.ls(selection=True, long=True)
        if not selected_objects:
            return
        object_name = selected_objects[0]
        value = cmds.floatField(self.scale_fields[index], query=True, value=True)
        self.set_single_scale(object_name, index, value)

    def create_coor_ui(self):
        # Create UI window
        if cmds.window("CoordinateWindow", exists=True):
            cmds.deleteUI("CoordinateWindow", window=True)

        coordinate_window = cmds.window("CoordinateWindow", title="Coordinate UI Tool", w=300, h=200)
        cmds.columnLayout(adjustableColumn=True)

        self.world_fields = []

        # Row layout for World Coordinates
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(label="World Coords")
        self.world_fields.append(cmds.floatField(width=75, showTrailingZeros=False,
                                                 changeCommand=self.apply_x_coordinate, precision=8))
        self.world_fields.append(cmds.floatField(width=75, showTrailingZeros=False,
                                                 changeCommand=self.apply_y_coordinate, precision=8))
        self.world_fields.append(cmds.floatField(width=75, showTrailingZeros=False,
                                                 changeCommand=self.apply_z_coordinate, precision=8))
        cmds.setParent("..")  # To break out of the rowLayout

        # Row layout for Rotation
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(label="Rotation Coords")
        self.rotation_fields.append(cmds.floatField(width=75, showTrailingZeros=False,
                                                    changeCommand=self.apply_rotation_x, precision=8))
        self.rotation_fields.append(cmds.floatField(width=75, showTrailingZeros=False,
                                                    changeCommand=self.apply_rotation_y, precision=8))
        self.rotation_fields.append(cmds.floatField(width=75, showTrailingZeros=False,
                                                    changeCommand=self.apply_rotation_z, precision=8))
        cmds.setParent("..")  # To break out of the rowLayout

        # Row layout for Scale
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(label="Scale Coords")
        self.scale_fields.append(cmds.floatField(width=75, showTrailingZeros=False,
                                                 changeCommand=self.apply_scale_x, precision=8))
        self.scale_fields.append(cmds.floatField(width=75, showTrailingZeros=False,
                                                 changeCommand=self.apply_scale_y, precision=8))
        self.scale_fields.append(cmds.floatField(width=75, showTrailingZeros=False,
                                                 changeCommand=self.apply_scale_z, precision=8))
        cmds.setParent("..")  # To break out of the rowLayout

        # Event to update UI whenever an object is selected
        cmds.scriptJob(event=["SelectionChanged", self.update_ui], protected=True)

        cmds.showWindow(coordinate_window)