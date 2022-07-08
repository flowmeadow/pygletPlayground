#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : demo script
@File      : demo.py
@Project   : pygletPlayground
@Time      : 01.10.21 23:50
@Author    : flowmeadow
"""
import numpy as np

from glpg_flowmeadow.camera.fly_motion import FlyMotion
from glpg_flowmeadow.display.gl_screen import GLScreen
from glpg_flowmeadow.rendering.lighting.lights import Lights
from glpg_flowmeadow.rendering.methods import draw_coordinates, draw_text_2D
from glpg_flowmeadow.rendering.models.model import Model
from glpg_flowmeadow.rendering.models.model_generation.geometry import sphere, cube, cylinder


class MyScreen(GLScreen):
    """
    Demo application class containing a movable camera, three light sources and a
    sphere model that is transformed and shaded dynamically
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame_count = 0

        # define shader list to use
        self.shaders = ["flat", "gouraud", "blinn_phong", "toon"]
        self.current_shader = self.shaders[0]

        # define camera
        self.cam = FlyMotion(self, camera_pos=(1.0, 1.0, 1.0), camera_view=(-1.0, -1.0, -1.0))

        # define light sources
        self.lights = Lights()
        self.lights.add(  # circling around
            position=(1.0, 1.0, 0.0),
            ambient=(1.0, 1.0, 0.5),
            diffuse=(1.0, 1.0, 0.5),
            specular=(1.0, 1.0, 0.5),
        )
        self.lights.add(  # at camera position
            position=(0.0, 0.0, 1.0),
            ambient=(0.0, 0.5, 1.0),
            diffuse=(0.0, 0.5, 1.0),
            specular=(0.0, 0.5, 1.0),
        )
        self.lights.add(  # constant
            position=(0.0, 0.0, 1.0),
            ambient=(1.0, 0.0, 0.5),
            diffuse=(1.0, 0.0, 0.5),
            specular=(1.0, 0.0, 0.5),
        )

        # define sphere model
        vertices, indices = sphere(refinement_steps=4)
        self.sphere = Model(
            vertices=vertices,
            indices=indices,
            shader_name=self.shaders,
            color=(0.0, 0.4, 1.0),
            rotation=(1.0, 0.0, 0.0, 90.0),
            translation=(0.0, 0.0, 0.1),
            num_lights=self.lights.num_lights,
        )
        vertices, indices = cube(refinement_steps=3)
        self.cube = Model(
            vertices=vertices,
            indices=indices,
            shader_name=self.shaders,
            color=(0.6, 0.4, 0.1),
            scale=0.1,
            rotation=(0.0, 0.0, 1.0, 45.0),
            num_lights=self.lights.num_lights,
        )

        vertices, indices = cylinder()
        self.cylinder = Model(
            vertices=vertices,
            indices=indices,
            shader_name=self.shaders,
            color=(0.2, 0.8, 0.1),
            translation=(0.0, 0.5, 0.0),
            num_lights=self.lights.num_lights,
        )

    def handle_events(self) -> None:
        """
        handle pygame events and do other stuff before drawing
        :return: None
        """
        self.sphere.update_camera(self.cam.camera_pos, self.cam.camera_view)  # update camera based on user inputs
        pass

    def draw_world(self) -> None:
        """
        draw objects in the world
        :return: None
        """
        draw_coordinates()

        # update shader
        idx = (self.frame_count // 500) % len(self.shaders)
        self.current_shader = self.shaders[idx]

        # move light sources
        new_pos = (np.sin(self.frame_count * 0.01), np.cos(self.frame_count * 0.01), 0.5)
        self.lights[0].update("position", new_pos)
        self.lights[1].update("position", self.cam.camera_pos)

        self.lights.draw()

        # transform sphere
        z = np.abs(np.sin(self.frame_count * 0.01)) / 2
        self.sphere.translate(0.0, 0.0, z)
        self.sphere.draw(shader_name=self.current_shader)

        # transform cube
        self.cube.draw(shader_name=self.current_shader)
        self.cube.translate(0.5, 0.0, 0.1)
        self.cube.rotate(self.frame_count * 0.2, 0.0, 0.0, 1.0)

        self.cylinder.draw(shader_name=self.current_shader)
        self.cylinder.scale(1.0, 1.0, 1.0 - z)

        # update frame counter
        self.frame_count += 1

    def draw_screen(self) -> None:
        """
        draw objects onto the screen
        :return: None
        """
        draw_text_2D(10, self.height - 10, f"FPS: {self.current_fps:.2f}")
        draw_text_2D(self.width - 300, self.height - 10, f"Current Shader: {self.current_shader.upper()}")
        draw_text_2D(self.width - 300, self.height - 35, f"Next in {(500 - self.frame_count) % 500} frames")
        if self.frame_count < 250:
            text = "Use ASDF to move and MOUSE to look around"
            draw_text_2D(self.width / 2 - 200, self.height / 2, f"{text}")


if __name__ == "__main__":
    demo = MyScreen(fullscreen=True)
    demo.run()
