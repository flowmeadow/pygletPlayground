#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce :
@File      : light.py
@Time      : 10.09.21 12:52
@Author    : flowmeadow
"""
from pyglet.gl import *
import ctypes
import numpy as np
from rendering.methods import draw_light

update_dict = {
    "position": {
        "function": glLightfv,
        "argument": GL_POSITION,
    },
    "ambient": {
        "function": glLightfv,
        "argument": GL_AMBIENT,
    },
    "diffuse": {
        "function": glLightfv,
        "argument": GL_DIFFUSE,
    },
    "specular": {
        "function": glLightfv,
        "argument": GL_SPECULAR,
    },
    "spot_direction": {
        "function": glLightfv,
        "argument": GL_SPOT_DIRECTION,
    },
    "a_const": {
        "function": glLightf,
        "argument": GL_CONSTANT_ATTENUATION,
    },
    "a_lin": {
        "function": glLightf,
        "argument": GL_LINEAR_ATTENUATION,
    },
    "a_quad": {
        "function": glLightf,
        "argument": GL_QUADRATIC_ATTENUATION,
    },
    "spot_cutoff": {
        "function": glLightf,
        "argument": GL_SPOT_CUTOFF,
    },
}

"""
GL_SPOT_CUTOFF, GL_SPOT_DIRECTION, GL_SPOT_EXPONENT, 
"""


class Light:
    defaults = dict(
        position=(0.0, 0.0, 0.0),
        ambient=(1.0, 1.0, 1.0, 1.0),
        diffuse=(1.0, 1.0, 1.0, 0.0),
        specular=(1.0, 1.0, 1.0, 0.0),
        spot_direction=(-1.0, 0.0, 0.0),
        a_const=1.0,
        a_lin=0.0,
        a_quad=0.0,
        spot_cutoff=180.,
    )

    def __init__(self, id: int, **kwargs):
        self.id = id
        attributes = self.defaults.copy()
        attributes.update(kwargs)

        self.position = kwargs['position']

        for attr, val in attributes.items():
            self.update(attr, val)

    def update(self, key: str, data):
        fun = update_dict[key]["function"]
        arg = update_dict[key]["argument"]

        # convert to ctypes
        if isinstance(data, (list, tuple, np.ndarray)):
            data = (ctypes.c_float * len(data))(*data)

        glPushMatrix()
        glLoadIdentity()
        fun(self.id, arg, data)
        self.__setattr__(key, data)
        glPopMatrix()

    def draw(self):
        draw_light(self.position)
