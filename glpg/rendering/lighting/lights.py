#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Manages several OpenGL light sources
@File      : lights.py
@Time      : 15.09.21 16:47
@Author    : flowmeadow
"""
from typing import Optional, Tuple

from glpg.rendering.lighting.light import Light
from pyglet.gl import *


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
        """Initialize"""
        self.num_lights = 0
        self.lights = []

    def add(
        self,
        position: Optional[Tuple[float, float, float]] = None,
        color: Optional[Tuple[float, float, float]] = None,
        ambient: Optional[Tuple[float, float, float]] = None,
        diffuse: Optional[Tuple[float, float, float]] = None,
        specular: Optional[Tuple[float, float, float]] = None,
        spot_direction: Optional[Tuple[float, float, float]] = None,
        a_const: Optional[float] = None,
        a_lin: Optional[float] = None,
        a_quad: Optional[float] = None,
        spot_cutoff: Optional[float] = None,
    ):
        """
        Adds a new light source, Allowed keyword arguments
        :param position: light position [3,]
        :param color: light color [3,]
        :param ambient: ambient color [3,]
        :param diffuse: diffuse color [3,]
        :param specular: specular color [3,]
        :param spot_direction: spotlight direction vector [3,]
        :param a_const: constant attenuation
        :param a_lin: linear attenuation
        :param a_quad: quadratic attenuation
        :param spot_cutoff: spotlight cutoff angle
        """
        kwargs = dict(
            position=position,
            color=color,
            ambient=ambient,
            diffuse=diffuse,
            specular=specular,
            spot_direction=spot_direction,
            a_const=a_const,
            a_lin=a_lin,
            a_quad=a_quad,
            spot_cutoff=spot_cutoff,
        )
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
