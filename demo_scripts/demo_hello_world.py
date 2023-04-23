#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Demo script; textured model of the earth is lighted and shaded by the sun in space.
@File      : texture_demo.py
@Project   : pygletPlayground
@Time      : 06.12.22 18:27
@Author    : flowmeadow
"""
import os

import numpy as np
from pyglet.gl import *

from glpg.camera.fly_motion import FlyMotion
from glpg.display.gl_screen import GLScreen
from glpg.rendering.lighting.lights import Lights
from glpg.rendering.methods import draw_text_2D
from glpg.rendering.models.model import Model
from glpg.rendering.models.model_generation.geometry import icosphere


class HelloWorld(GLScreen):
    """
    Demo application class containing a movable camera, three light sources and a
    sphere model that is transformed and shaded dynamically
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.frame_count = 0

        # define camera
        self.cam = FlyMotion(self, camera_pos=(1.0, 1.0, 1.0), camera_view=(-1.0, -1.0, -1.0))

        # define light sources
        self.lights = Lights()
        self.lights.add(  # circling around
            position=(1.0, 1.0, 0.0),
            color=(1.0, 1.0, 0.95),
        )

        texture_paths = [
            "demo_textures/8081_earthmap4k.iba",
            "demo_textures/8081_earthspec4k.iba",
            "demo_textures/8081_earthbump4k.iba",
            "demo_textures/8081_earthlights4k.iba",
        ]

        # define sphere model
        radius = 0.1
        vertices, indices = icosphere(radius=radius, refinement_steps=5)

        # create earth sphere
        self.earth = Model(
            vertices,
            indices,
            textures=texture_paths,
            shader="demo_shaders/earth",
            num_lights=self.lights.num_lights,
            scale=5.0,
        )

        # create cloud sphere
        self.clouds = Model(
            vertices,
            indices,
            textures="demo_textures/8081_earthclouds4k.iba",
            shader="demo_shaders/clouds",
            num_lights=self.lights.num_lights,
            scale=5.2,
        )

        # create sun sphere
        self.sun = Model(
            vertices,
            indices,
            shader="demo_shaders/sun",
            num_lights=self.lights.num_lights,
            scale=10.0,
        )

        # create night sky sphere
        self.night_sky = Model(
            vertices,
            indices,
            textures="demo_textures/nightsky4k.iba",
            shader="demo_shaders/night_sky",
            num_lights=self.lights.num_lights,
            scale=2.0,
        )

    def handle_events(self) -> None:
        """
        handle pygame events and do other stuff before drawing
        :return: None
        """
        # update camera position for all objects that use it in their shader
        self.earth.update_camera(self.cam.camera_pos, self.cam.camera_view)
        self.clouds.update_camera(self.cam.camera_pos, self.cam.camera_view)
        self.sun.update_camera(self.cam.camera_pos, self.cam.camera_view)

    def draw_world(self) -> None:
        """
        draw objects in the world
        :return: None
        """

        # move sun
        light_speed = 0.002
        new_pos = 10.0 * np.array([np.sin(self.frame_count * light_speed), np.cos(self.frame_count * light_speed), 0.0])
        self.lights[0].update("position", new_pos)
        self.sun.translate(*new_pos)

        # transform earth, clouds and night sky

        angle = 0.01 * self.frame_count
        self.earth.rotate(angle, 0.0, 0.0, -1.0)
        self.clouds.rotate(angle, 0.0, 0.0, -1.0)

        sky_center = self.cam.camera_pos
        self.night_sky.translate(*sky_center)
        self.night_sky.rotate(angle, 0.0, 0.0, -1.0)

        # draw objects
        glDisable(GL_DEPTH_TEST)  # disable such that sky is always drawn in the background
        self.night_sky.draw()  # draw night sky sphere
        glEnable(GL_DEPTH_TEST)

        self.earth.draw()
        self.clouds.draw()
        self.sun.draw()

        # draw_coordinates()
        # self.lights.draw()

        # update frame counter
        self.frame_count += 1

    def draw_screen(self) -> None:
        """
        draw objects onto the screen
        :return: None
        """
        draw_text_2D(10, self.height - 10, f"FPS: {self.current_fps:.2f}")
        if self.frame_count < 250:
            text = "Use ASDF to move and MOUSE to look around"
            draw_text_2D(self.width / 2 - 200, self.height / 2, f"{text}")


if __name__ == "__main__":
    # os.system(f"python update_shader.py")

    demo = HelloWorld(fullscreen=True)
    demo.run()
