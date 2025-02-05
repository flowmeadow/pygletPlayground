#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Demo script for mesh manipulation and coloring based on generated textures
@File      : dynamic_height_map.py
@Project   : pygletPlayground
@Time      : 24.03.23 19:43
@Author    : flowmeadow
"""
import warnings

import numpy as np
from glpg.camera.fly_motion import FlyMotion
from glpg.display.gl_screen import GLScreen
from glpg.input.menu import Menu
from glpg.rendering.lighting.lights import Lights
from glpg.rendering.methods import draw_coordinates, draw_text_2D, draw_texture
from glpg.rendering.models.model import Model
from glpg.rendering.models.model_generation.geometry import bars, grid
from glpg.texturing.methods import wrap_texture
from glpg.texturing.texture import Texture
from pyglet.gl import *


def generate_height_map(
    grid_size=(100, 100),
    seed=0,
    num_iter=100,
    counter=0,
    smoothness=0.5,
    experimental_mode=False,
):
    max_size = 100
    max_iter = 100

    if max(grid_size) > max_size and not experimental_mode:
        grid_size = [min(g, max_size) for g in grid_size]
        warnings.warn(
            f"\nGrid size of more than {max_size} is not recommended as the computation increases exponentially."
            f"\nIf you want to compute with higher grid sizes, set the 'experimental_mode' flag. "
        )
    if num_iter > max_iter and not experimental_mode:
        num_iter = max_iter
        warnings.warn(
            f"\nMore than {max_iter} iterations is not recommended as the computation increases exponentially."
            f"\nIf you want to compute with more iterations, set the 'experimental_mode' flag. "
        )
    np.random.seed(seed)

    x_arr, y_arr = (
        np.arange(grid_size[0]) / grid_size[0],
        np.arange(grid_size[1]) / grid_size[1],
    )
    grid_pts = np.array(np.meshgrid(y_arr, x_arr)).T.reshape(-1, 2)
    height_map = np.zeros(grid_size)
    rand_pts = np.random.random((num_iter, 4))

    rand_pts[:, 0] += 0.01 * np.sin(counter)
    rand_pts[:, 1] += 0.01 * np.cos(counter)

    p_1_arr, p_2_arr = rand_pts[:, :2], rand_pts[:, 2:]
    for p_1, p_2 in zip(p_1_arr, p_2_arr):
        heights = np.cross(p_2 - p_1, grid_pts - p_1) / np.linalg.norm(p_2 - p_1)
        heights = np.tanh(heights * 2 ** (smoothness * 8))
        height_map += heights.reshape(grid_size)
    height_map = (height_map - np.min(height_map)) / (
        np.max(height_map) - np.min(height_map)
    )
    return height_map

class ColorMap:
    def __init__(self):
        self.key_points = []
        self.r_arr = []
        self.g_arr = []
        self.b_arr = []
        self.cmap_arr = None

    def add(self, value, color):
        self.key_points.append(value)
        self.r_arr.append(color[0])
        self.g_arr.append(color[1])
        self.b_arr.append(color[2])

        self.cmap_arr = np.concatenate([[self.key_points], [self.r_arr], [self.g_arr], [self.b_arr]], axis=0).T

    def arr2img(self, arr):
        img_arr = np.zeros((*arr.shape, 3))
        img_arr[:, :, 0] = np.interp(arr, self.cmap_arr[:, 0], self.cmap_arr[:, 1])
        img_arr[:, :, 1] = np.interp(arr, self.cmap_arr[:, 0], self.cmap_arr[:, 2])
        img_arr[:, :, 2] = np.interp(arr, self.cmap_arr[:, 0], self.cmap_arr[:, 3])
        img_arr[:, :, 2] = np.interp(arr, self.cmap_arr[:, 0], self.cmap_arr[:, 3])

        return img_arr


class ClassicColorMap(ColorMap):
    def __init__(self):
        super().__init__()
        super().add(0.00, [0.0, 0.0, 1.0])
        super().add(0.25, [0.0, 1.0, 1.0])
        super().add(0.50, [0.0, 1.0, 0.0])
        super().add(0.75, [1.0, 1.0, 0.0])
        super().add(1.00, [1.0, 0.0, 0.0])

    def add(self, *args):
        warnings.warn("Default colormaps don't have an add function")
        pass


class DemoApp(GLScreen):
    """
    Demo application class containing a movable camera, three light sources and a
    sphere model that is transformed and shaded dynamically
    """

    def __init__(self, grid_size, **kwargs):
        super().__init__(max_fps=60, **kwargs)
        self.frame_count = 0
        self.animation_speed = 0
        self.param_pointer = 0
        self.panel_width = 500
        self.grid_size = grid_size
        self.grid_options = list(2 ** np.arange(5)) + list(range(32, 97, 16))

        # define camera
        self.cam = FlyMotion(
            self, camera_pos=(1.0, 1.0, 1.0), camera_view=(-1.0, -1.0, -1.0)
        )

        # define light sources
        self.lights = Lights().add(position=(0.5, 0.5, 1.0))

        # generate classic colormap object (interpolates blue -> turquoise -> green -> yellow -> red)
        self.cmap = ClassicColorMap()

        # generate and initialize heightmap texture (grayscale) based on grid size
        self.height_tex = Texture(np.zeros(grid_size))
        self.height_tex.update_param(GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
        self.height_tex.update_param(GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)

        # generate and initialize color texture (RGB) based on grid size
        rgb_texture = self.cmap.arr2img(np.zeros(grid_size))
        self.color_tex = Texture(rgb_texture)
        self.color_tex.update_param(GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
        self.color_tex.update_param(GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)

        # define grid model
        vertices, indices = grid(width=self.grid_size[0], length=self.grid_size[1])
        self.grid = Model(
            vertices=vertices,
            indices=indices,
            texture_coords=wrap_texture(vertices, method="xy-projection"),
            textures=[self.height_tex, self.color_tex],
            shader="demo_shaders/height_map",
            num_lights=self.lights.num_lights,
        )

        # define pillars (bars) model
        vertices, indices = bars(width=self.grid_size[0], length=self.grid_size[1])
        self.bars = Model(
            vertices=vertices,
            indices=indices,
            texture_coords=wrap_texture(vertices, method="xy-projection"),
            textures=[self.height_tex, self.color_tex],
            shader="demo_shaders/height_map",
            num_lights=self.lights.num_lights,
        )

        # create menu object
        self.menu = self.init_menu()

    def handle_events(self) -> None:
        """
        handle pygame events and do other stuff before drawing
        :return: None
        """
        self.grid.update_camera(
            self.cam.camera_pos, self.cam.camera_view
        )  # update camera based on user inputs

        # generate new heightmap
        height_array = generate_height_map(
            grid_size=self.grid_size,
            counter=self.animation_speed,
            smoothness=self.menu.get_option("smoothness"),
            seed=self.menu.get_option("height_seed"),
            experimental_mode=True,
        )

        # generate new color texture
        color_array = self.cmap.arr2img(height_array)

        # update arrays based on menu settings
        if not self.menu.get_option("height_tex_enabled"):
            height_array = np.full(height_array.shape, 0.5)
        if not self.menu.get_option("color_tex_enabled"):
            color_array = np.full(color_array.shape, 0.5)

        # update textures and texture options
        self.height_tex.load(height_array)
        self.color_tex.load(color_array)
        self.height_tex.update_param(
            GL_TEXTURE_MAG_FILTER, self.menu.get_option("height_tex_filter")
        )
        self.color_tex.update_param(
            GL_TEXTURE_MAG_FILTER, self.menu.get_option("color_tex_filter")
        )

        # check menu for user input
        self.menu.update()

        # update frame counter
        self.frame_count += 1
        self.animation_speed += 0.1 * self.menu.get_option("speed")

    def draw_world(self) -> None:
        """
        draw objects in the world
        :return: None
        """
        # draw coordinate frame and light source
        draw_coordinates()
        self.lights.draw()

        # draw selected model (self.bar or self.grid)
        self.menu.get_option("model_type").draw()

    def draw_screen(self) -> None:
        """
        draw objects onto the screen
        :return: None
        """
        # draw the menu
        self.menu.draw()

        # draw the two textures
        max_edge_size = self.panel_width // 2  # maximum image edge size
        img_size = np.array(self.grid_size) * np.min(
            max_edge_size / np.array(self.grid_size)
        )
        draw_texture(
            self.width - 2 * img_size[0],
            self.height - img_size[1],
            *img_size,
            self.height_tex,
        )
        draw_texture(
            self.width - img_size[0],
            self.height - img_size[1],
            *img_size,
            self.color_tex,
        )

        # draw current FPS
        draw_text_2D(10, self.height - 10, f"FPS: {self.current_fps:.2f}")

    def init_menu(self):
        """
        Creates menu object and adds menu entries
        """
        menu = Menu(
            self,
            x=self.size[0] - self.panel_width,
            y=0,
            w=self.panel_width,
            h=self.size[1] - self.panel_width // 2,
        )

        menu.add_entry(
            "model_type",
            [self.grid, self.bars],
            "Model Type",
            ["Grid", "Bars"],
            info_txt="The object model to render. Can be a connected mesh (Grid) or separated pillars (Bars)",
            index=0,
        )
        menu.add_entry(
            "grid_width",
            self.grid_options,
            "Grid Width",
            info_txt="Number of cells in x-direction\n(REQUIRES RESTART)",
            index=self.grid_options.index(self.grid_size[0]),
        )
        menu.add_entry(
            "grid_height",
            self.grid_options,
            "Grid Height",
            info_txt="Number of cells in y-direction\n(REQUIRES RESTART)",
            index=self.grid_options.index(self.grid_size[1]),
        )
        menu.add_entry(
            "height_tex_enabled",
            [True, False],
            "Height Texture Enabled",
            info_txt="Enable or disable the grayscale heightmap texture",
            index=0,
        )
        menu.add_entry(
            "color_tex_enabled",
            [True, False],
            "Color Texture Enabled",
            info_txt="Enable or disable the RGB texture",
            index=0,
        )
        menu.add_entry(
            "height_tex_filter",
            [GL_LINEAR, GL_NEAREST],
            "Height Texture Filter",
            ["GL_LINEAR", "GL_NEAREST"],
            info_txt="Filter for the texture magnification function (GL_TEXTURE_MAG_FILTER) "
            "of the grayscale heightmap texture",
            index=0,
        )
        menu.add_entry(
            "color_tex_filter",
            [GL_LINEAR, GL_NEAREST],
            "Color Texture Filter",
            ["GL_LINEAR", "GL_NEAREST"],
            info_txt="Filter for the texture magnification function (GL_TEXTURE_MAG_FILTER) of the RGB texture",
            index=0,
        )
        menu.add_entry(
            "speed",
            np.round(np.arange(11) * 0.1, 1),
            "Height Map Animation Speed",
            info_txt="Defines the animation speed by adjusting the distance between two height maps",
            index=5,
        )
        menu.add_entry(
            "height_seed",
            range(256),
            "Height Map Seed",
            info_txt="Random seed for height map generation",
            index=20,
        )
        menu.add_entry(
            "smoothness",
            np.round(np.arange(11) * 0.1, 1),
            "Height Map Smoothness",
            info_txt="Specifies the smoothness of the generated height map",
            index=7,
        )
        menu.welcome_msg = [
            f"{__doc__}",
            "HINT: Close menu to increase frame rate\n",
            menu.build_title("KEYMAP"),
            *menu.welcome_msg,
            "Change camera's position:   A,S,D,F",
            "Change camera's rotation:   MOUSE",
            "Restart application:        R",
            "Close application:          Q\n",
        ]
        return menu


if __name__ == "__main__":
    grid_size = [48, 48]  # default grid_size
    keep_running = True
    while keep_running:
        demo = DemoApp(grid_size, fullscreen=True)  # create window object
        demo.run()  # run it
        grid_size = demo.menu.get_option("grid_width"), demo.menu.get_option(
            "grid_height"
        )  # get selected grid size
        keep_running = demo.restart_request  # set to True if app was restarted
        del demo  # delete old object
