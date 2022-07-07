#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce :
@File      : lights.py
@Time      : 15.09.21 16:47
@Author    : flowmeadow
"""

from rendering.lighting.light import Light
from pyglet.gl import *


class Lights:
    light_ids = {
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
        self.num_lights = 0
        self.lights = []

    def add(self, **kwargs):
        light_id = self.light_ids[self.num_lights]
        self.num_lights += 1
        self.lights.append(Light(light_id, **kwargs))

    def update(self, *args, **kwargs):
        for light in self.lights:
            light.update(*args, **kwargs)

    def draw(self):
        for light in self.lights:
            light.draw()

    def __getitem__(self, key):
        return self.lights[key]



