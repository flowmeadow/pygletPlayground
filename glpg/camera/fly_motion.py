#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Camera class that allows flying freely through the scene
@File      : fly_motion.py
@Time      : 09.09.21 22:55
@Author    : flowmeadow
"""
import numpy as np
import pyglet.window
from pyglet.window import key as gl_key
from glpg.transformations.methods import rotate_vec

from glpg.camera.camera import Camera


class FlyMotion(Camera):
    """
    Camera class that allows flying freely through the scene. Camera can be
    controlled using the mouse and the 'WASD' keys.
    """

    def __init__(
        self,
        window,
        **kwargs,
    ):
        """
        :param display_center: the display center coordinate
        :param camera_pos: position of the camera in world coordinates [3,]
        :param camera_view: view direction of the camera in world coordinates [3,]
        :param camera_up: vector pointing up from the camera world coordinates [3,]
        """
        self._mouse = window.mouse
        self._keys = window.keys
        window.set_exclusive_mouse(True)
        super().__init__(**kwargs)

    def update(self, window: pyglet.window.Window):
        """
        Updates the camera attributes based on user inputs
        :param window: current window object
        :return:
        """
        self.update_mouse_movement()
        self.update_key_movement()

    def update_key_movement(self):
        """
        Updates camera position based on keyboard inputs
        """
        keys = self._keys
        for key in keys:
            if key in [gl_key.UP, gl_key.W]:
                self.camera_pos += 0.01 * self.camera_view  # go forward
            if key in [gl_key.DOWN, gl_key.S]:
                self.camera_pos -= 0.01 * self.camera_view  # go backward
            if key in [gl_key.RIGHT, gl_key.D]:
                side_vec = np.cross(self.camera_view, self.camera_up)
                side_vec /= np.linalg.norm(side_vec)
                self.camera_pos += 0.01 * side_vec  # go right
            if key in [gl_key.LEFT, gl_key.A]:
                side_vec = np.cross(self.camera_view, self.camera_up)
                side_vec /= np.linalg.norm(side_vec)
                self.camera_pos -= 0.01 * side_vec  # go left

    def update_mouse_movement(self):
        """
        update camera rotation based on mouse position
        """
        mouse = self._mouse

        # look up/down
        if mouse.dy != 0:
            left_vec = -np.cross(self.camera_view, self.camera_up)
            self.camera_view = rotate_vec(
                vec=self.camera_view,
                axis=left_vec,
                angle=-mouse.dy * 0.05,
            )
        # look left/right
        if mouse.dx != 0:
            self.camera_view = rotate_vec(
                vec=self.camera_view,
                axis=self.camera_up,
                angle=-mouse.dx * 0.05,
            )

        # reset mouse
        mouse.reset()
