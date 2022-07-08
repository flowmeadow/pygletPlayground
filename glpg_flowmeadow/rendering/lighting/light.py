#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Light source class that manages an OpenGL light source
@File      : light.py
@Time      : 10.09.21 12:52
@Author    : flowmeadow
"""
import ctypes
from typing import Union

import numpy as np
from pyglet.gl import *
from glpg_flowmeadow.rendering.methods import draw_light

# define OpenGl update function and argument for each light parameter
# TODO: add GL_SPOT_EXPONENT
update_dict = dict(
    position={"function": glLightfv, "argument": GL_POSITION},
    ambient={"function": glLightfv, "argument": GL_AMBIENT},
    diffuse={"function": glLightfv, "argument": GL_DIFFUSE},
    specular={"function": glLightfv, "argument": GL_SPECULAR},
    spot_direction={"function": glLightfv, "argument": GL_SPOT_DIRECTION},
    a_const={"function": glLightf, "argument": GL_CONSTANT_ATTENUATION},
    a_lin={"function": glLightf, "argument": GL_LINEAR_ATTENUATION},
    a_quad={"function": glLightf, "argument": GL_QUADRATIC_ATTENUATION},
    spot_cutoff={"function": glLightf, "argument": GL_SPOT_CUTOFF},
)


class Light:
    """
    Light source class that manages an OpenGL light source
    """

    # default parameter
    position = (0.0, 0.0, 0.0)
    ambient = (1.0, 1.0, 1.0, 1.0)
    diffuse = (1.0, 1.0, 1.0, 0.0)
    specular = (1.0, 1.0, 1.0, 0.0)
    spot_direction = (-1.0, 0.0, 0.0)
    a_const = 1.0
    a_lin = 0.0
    a_quad = 0.0
    spot_cutoff = 180.0

    def __init__(self, id: int, **kwargs):
        """
        :param id: OpenGL light ID (0 - 7)
        :param kwargs: parameters to update
        """
        self._id = id
        for attr, val in kwargs.items():
            self.update(attr, val)

    def update(self, key: str, data: Union[list, tuple, np.ndarray]):
        """
        Updates OpenGL light source parameter
        :param key: parameter to change
        :param data: value
        """
        fun = update_dict[key]["function"]
        arg = update_dict[key]["argument"]

        # convert to ctypes
        if isinstance(data, (list, tuple, np.ndarray)):
            data = (ctypes.c_float * len(data))(*data)
        else:
            raise ValueError(f"Value {data} for parameter {key} of light source {self._id} has wrong type")

        # update parameter
        glPushMatrix()
        glLoadIdentity()
        fun(self._id, arg, data)
        self.__setattr__(key, data)
        glPopMatrix()

    def draw(self):
        """
        Draws a representation of the light source into the scene
        """
        draw_light(self.position)
