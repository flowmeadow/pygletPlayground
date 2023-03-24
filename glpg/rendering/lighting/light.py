#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Light source class that manages an OpenGL light source
@File      : light.py
@Time      : 10.09.21 12:52
@Author    : flowmeadow
"""
import ctypes
from typing import Optional, Tuple, Union

import numpy as np
from glpg.rendering.methods import draw_light
from pyglet.gl import *

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

    def __init__(
        self,
        id: int,
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
        Create an OpenGL light object
        :param id: OpenGL light ID (0 - 7)
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
        self._id = id

        if color is not None:
            ambient = diffuse = specular = color

        # default values
        kwargs = dict(
            position=(0.0, 0.0, 0.0) if not position else position,
            ambient=(1.0, 1.0, 1.0) if not ambient else ambient,
            diffuse=(1.0, 1.0, 1.0) if not diffuse else diffuse,
            specular=(1.0, 1.0, 1.0) if not specular else specular,
            spot_direction=(0.0, 0.0, 0.0) if not spot_direction else spot_direction,
            a_const=0.5 if not a_const else a_const,
            a_lin=0.0 if not a_lin else a_lin,
            a_quad=0.0 if not a_quad else a_quad,
            spot_cutoff=180.0 if not spot_cutoff else spot_cutoff,
        )
        self.position = kwargs["position"]

        # if 'color' is given, update 'ambient', 'diffuse' and 'specular'

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
        elif isinstance(data, (int, float)):
            data = ctypes.c_float(data)
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
