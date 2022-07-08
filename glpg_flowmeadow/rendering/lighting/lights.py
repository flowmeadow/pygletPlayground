#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Manages several OpenGL light sources
@File      : lights.py
@Time      : 15.09.21 16:47
@Author    : flowmeadow
"""

from pyglet.gl import *

from glpg_flowmeadow.rendering.lighting.light import Light


class Lights:
    """
    Manages several OpenGL light sources
    """
    _light_ids = {
        0: GL_LIGHT0,
        1: GL_LIGHT1,
        2: GL_LIGHT2,
        3: GL_LIGHT3,
        4: GL_LIGHT4,
        5: GL_LIGHT5,
        6: GL_LIGHT6,
        7: GL_LIGHT7,
    }

    def __init__(self):
        """ Initialize """
        self.num_lights = 0
        self.lights = []

    def add(self, **kwargs):
        """
        Adds a new light source
        :param kwargs: forwarded keyword arguments
        """
        # create a new light object
        light_id = self._light_ids[self.num_lights]
        self.num_lights += 1
        self.lights.append(Light(light_id, **kwargs))

    def draw(self):
        """
        Draws a representation of all light sources into the scene
        """
        for light in self.lights:
            light.draw()

    def __getitem__(self, idx: int) -> Light:
        """
        Returns a light object by its index
        :param idx: Index of the light source
        :return: light object
        """
        return self.lights[idx]



