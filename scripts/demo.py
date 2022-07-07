#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : TODO
@File      : demo.py
@Project   : pygletPlayground
@Time      : 01.10.21 23:50
@Author    : flowmeadow
"""
# from display.window import Window
from abc import ABC
from abc import ABCMeta, abstractmethod
import numpy as np
from pyglet.gl import *
from display.gl_screen import GLScreen
from rendering.methods import draw_text_2D, draw_coordinates
from camera.fly_motion import FlyMotion
from rendering.lighting.lights import Lights
from rendering.models.model import Model
from rendering.models.model_generation.geometry import cube, sphere
from camera.camera import Camera
from scripts.model_from_obj import load_model

import ctypes

# class Demo(Window):
#     def __init__(self):
#         super().__init__()
#         glClearColor(0.0, 0.0, 0.0, 1.0)
#         gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
#
#     def draw_world(self) -> None:
#         glClear(GL_COLOR_BUFFER_BIT)
#         glLoadIdentity()
#         glBegin(GL_TRIANGLES)
#         glVertex2f(0, 0)
#         print(self.size)
#         glVertex2f(self.size[0], 0)
#         glVertex2f(self.size[0], self.size[1])
#         glEnd()


class MyScreen(GLScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cam = FlyMotion(self, camera_pos=(1.0, 1.0, 1.0), camera_view=(-1.0, -1.0, -1.0))
        # self.cam = Camera(camera_pos=(1., 1., 1.), camera_view=(-1., -1., -1.))

        self.lights = Lights()

        self.lights.add(
            position=(1., 1., 0.),
            ambient=(1.0, 1.0, 0.5),
            diffuse=(1.0, 1.0, 0.5),
            specular=(1.0, 1.0, 0.5),
        )

        vertices, indices = sphere(refinement_steps=3)
        self.obj = Model(
            vertices=vertices,
            indices=indices,
            shader_name='blinn_phong',
            color=(0.0, 0.4, 1.0),
            scale=1.,
            rotation=(1.0, 0.0, 0.0, 90.0),
            num_lights=self.lights.num_lights
        )

        self.frame_count = 0

    def handle_events(self) -> None:
        """
        handle pygame events and do other stuff before drawing
        :return: None
        """
        self.obj.update_camera(self.cam.camera_pos, self.cam.camera_view)
        pass

    def draw_world(self) -> None:

        """
        draw objects in the world
        :return: None
        """
        # glClear(GL_COLOR_BUFFER_BIT)
        # glLoadIdentity()
        # glBegin(GL_TRIANGLES)
        # glVertex2f(0, 0)
        # glVertex2f(self.width, 0)
        # glVertex2f(self.width, self.height)
        # glEnd()
        # glColor3f(1.0, 0.0, 0.0)
        # glBegin(GL_TRIANGLES)
        # glVertex3f(0.0, 0.0, -0.9)
        # glVertex3f(2.0, 0.0, 1.0)
        # glVertex3f(0.0, 1.0, 1.0)
        #
        # glEnd()
        # glFlush()
        draw_coordinates()
        new_pos = (np.sin(self.frame_count * 0.01), np.cos(self.frame_count * 0.01), 0.5)
        self.lights[0].update("position", new_pos)
        self.lights.draw()
        self.obj.draw()
        self.frame_count += 1

    def draw_screen(self) -> None:
        """
        draw objects onto the screen
        :return: None
        """
        draw_text_2D(10, self.height - 10, f"{self.current_fps:.2f}")


def main():
    demo = MyScreen(fullscreen=True)
    demo.run()


if __name__ == "__main__":
    main()
