#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : base camera class
@File      : camera.py
@Time      : 09.09.21 22:55
@Author    : flowmeadow
"""
from abc import ABCMeta, abstractmethod
from typing import Tuple, Union

import numpy as np
import pyglet.window

from glpg.rendering.methods import draw_cam
from glpg.transformations.methods import construct_T


class Camera:
    """
    base camera class containing the cameras pose information.
    'move' method has to be defined in the child classes
    """

    __metaclass__ = ABCMeta

    def __init__(
        self,
        camera_pos=(0.0, 0.0, 0.0),
        camera_view=(1.0, 0.0, 0.0),
        camera_up=(0.0, 0.0, 1.0),
        name="Camera",
    ):
        """
        :param camera_pos: position of the camera in world coordinates [3,]
        :param camera_view: view direction of the camera in world coordinates [3,]
        :param camera_up: vector pointing up from the camera world coordinates [3,]
        """
        self.name = name
        camera_view, camera_up = np.array(camera_view), np.array(camera_up)
        self._camera_pos = np.array(camera_pos)
        self._camera_view = camera_view / np.linalg.norm(camera_view)
        self._camera_up = camera_up / np.linalg.norm(camera_up)

    def copy_from(self, cam: object):  # TODO: how to reference base class object from child for type hints
        """
        Copy the pose from another Camera object and
        :param cam: Camera object
        """
        self.camera_pos = cam.camera_pos
        self.camera_view = cam.camera_view
        self.camera_up = cam.camera_up

    def draw(self):
        """
        Draw camera to scene
        """
        draw_cam(self.camera_pos, self.rot_mat(), radius=0.2)

    @abstractmethod
    def update(self, window: pyglet.window.Window) -> None:
        """
        Overwrite in child to change cam during run time
        :param window: current window object
        """

    @property
    def camera_pos(self) -> np.array:
        """
        :return: camera position
        """
        return self._camera_pos.copy()

    @camera_pos.setter
    def camera_pos(self, value: Union[np.array, Tuple[float, float, float]]):
        """
        :param value: numpy array or 3 entry large tuple/list
        """
        self._camera_pos = np.array(value)

    @property
    def camera_view(self) -> np.array:
        """
        :return: camera view direction (normalized)
        """
        return self._camera_view.copy()

    @camera_view.setter
    def camera_view(self, value: Union[np.array, Tuple[float, float, float]]):
        """
        :param value: numpy array or 3 entry large tuple/list
        """
        arr = np.array(value)
        self._camera_view = arr / np.linalg.norm(arr)  # normalize vector

    @property
    def camera_up(self) -> np.array:
        """
        :return: camera up vector (normalized)
        """
        return self._camera_up.copy()

    @camera_up.setter
    def camera_up(self, value: Union[np.array, Tuple[float, float, float]]):
        """
        :param value: numpy array or 3 entry large tuple/list
        """
        arr = np.array(value)
        self._camera_up = arr / np.linalg.norm(arr)  # normalize vector
        self._camera_up = arr

    def rot_mat(self) -> np.ndarray:
        """
        return the rotation matrix from world to camera coordinates
        :return: rotation matrix as numpy array (3, 3)
        """
        x_c = np.cross(self.camera_view, self.camera_up)
        y_c = self.camera_up
        z_c = self.camera_view
        R = np.concatenate((x_c, y_c, z_c)).reshape(3, 3).T
        return R

    def transf(self):
        """
        Compute and return the transformation matrix from world to camera coordinates
        :return:
        """
        return construct_T(self.rot_mat(), self.camera_pos)
