#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce :
@File      : model.py
@Time      : 31.08.21 19:12
@Author    : flowmeadow
"""

from typing import List, Union

import numpy as np
from pyglet.gl import *
from glpg_flowmeadow.rendering.gpu.shader import Shader
from glpg_flowmeadow.rendering.gpu.vao import VAO
from glpg_flowmeadow.transformations.methods import compute_normals, flip_inside_out, rotate_vec


class Model:

    default_shader = "blinn_phong"
    default_color = (0.0, 0.0, 1.0)

    def __init__(
        self,
        vertices: np.ndarray,
        indices: np.ndarray,
        color: Union[np.ndarray, List[float]] = default_color,
        rotation=(1.0, 0.0, 0.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        translation=(0.0, 0.0, 0.0),
        shader_name: Union[str, List[str]] = default_shader,
        inside_out=False,
        num_lights=1,
    ) -> None:
        """
        :param vertices: object vertex coordinates (m, 3) [float]
        :param indices: object triangle vertex indices (n, 3) [int]
        :param color: color of the object (3,) or each individual vertex (n, 3)
        :param rotation: initial rotation parameter; rotation axis [0, 1, 2] and rotation angle [3] in degrees
        :param scale: initial scale parameter; one for each axis (x, y, z)
        :param translation: initial translation vector
        :param shader_name: name of the shader or list of shader names for change during runtime
        :param inside_out: if True, flip face normals
        :param num_lights: number of light sources in scene
        """

        # color
        colors = self.format_color_array(color, vertices.shape[0])
        if inside_out:
            indices = flip_inside_out(indices)

        # set initial vertex positions
        vertices = rotate_vec(vertices, rotation[:3], rotation[3])  # rotate
        vertices *= np.array(scale)  # scale
        vertices += np.array(translation)  # translate

        # compute normals from vertices
        normals = compute_normals(indices, vertices)
        indices, vertices = np.array(indices, dtype=np.uint32), np.array(vertices, dtype=np.float32)
        self._indices = indices
        self._vertices = vertices
        self._normals = normals
        self._colors = colors

        # define VAO
        self.vao = VAO(indices, object_id=GL_TRIANGLES)
        self.vao.set_vbo("position", vertices)
        self.vao.set_vbo("color", colors[:, :3])
        self.vao.set_vbo("normal", normals)

        # initialize model matrix and model operations list
        self.model_matrix = np.identity(4, dtype=np.float32)
        self.operations = []

        # initialize shader
        self.shaders = dict()
        if isinstance(shader_name, str):
            shader_name = [shader_name]
        for s in shader_name:
            self.shaders[s] = Shader(s, num_lights=num_lights)
        self.first_shader = shader_name[0]

    def rotate(self, angle: float, x: float, y: float, z: float):
        """
        rotate model around an axis defined by x, y and z.
        :param angle: rotation angle
        :param x: x-factor
        :param y: y-factor
        :param z: z-factor
        """

        rot_vec = [angle, x, y, z]

        # normalize axis
        axis = np.array([x, y, z])
        l, m, n = axis / np.linalg.norm(axis)

        # compute angle, sine and cosine values
        angle = np.pi * angle / 180.0
        s, c = np.sin(angle), np.cos(angle)

        # build transformation matrix (4, 4)
        rot_transform = np.array(
            [
                [l * l * (1 - c) + c, m * l * (1 - c) - n * s, n * l * (1 - c) + m * s, 0.0],
                [l * m * (1 - c) + n * s, m * m * (1 - c) + c, n * m * (1 - c) - l * s, 0.0],
                [l * n * (1 - c) - m * s, m * n * (1 - c) + l * s, n * n * (1 - c) + c, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        # update model matrix and operations list
        self.model_matrix = self.model_matrix @ rot_transform
        self.operations.append([glRotatef, rot_vec])

    def scale(self, x: float, y: float, z: float):
        """
        scale model in x, y and z direction
        :param x: x-factor
        :param y: y-factor
        :param z: z-factor
        """
        scale_vec = [x, y, z]

        # build transformation matrix (4, 4)
        scale_transform = np.identity(4, dtype=np.float)
        np.fill_diagonal(scale_transform[:3, :3], scale_vec)

        # update model matrix and operations list
        self.model_matrix = self.model_matrix @ scale_transform
        self.operations.append([glScalef, scale_vec])

    def translate(self, x: float, y: float, z: float):
        """
        translate model about vector (x, y, z)
        :param x: x-factor
        :param y: y-factor
        :param z: z-factor
        """
        trans_vec = [x, y, z]

        # build transformation matrix (4, 4)
        trans_transform = np.identity(4, dtype=np.float)
        trans_transform[:-1, 3] = trans_vec

        # update model matrix and operations list
        self.model_matrix = self.model_matrix @ trans_transform
        self.operations.append([glTranslatef, trans_vec])

    def reset(self):
        """
        Reset model
        """
        self.model_matrix = np.identity(4, dtype=np.float32)
        self.operations = []

    def draw(self, shader_name: str = None, num_indices: int = None, offset=0):
        """
        Update shader, perform all transformations and draw model
        :param shader_name: select a shader
        :param num_indices: number of indices to draw; by default all
        :param offset: start point of the indices to draw; by default first (0)
        """

        # update shader
        if shader_name is None:
            shader_name = self.first_shader
        self.update_shader(shader_name)
        self.shaders[shader_name].use()

        glPushMatrix()
        # perform transformations
        for operation, args in self.operations:
            operation(*args)
        # draw model
        self.vao.draw(num_indices, offset)
        glPopMatrix()
        glFlush()

        # reset
        self.shaders[shader_name].un_use()
        self.reset()

    def update_shader(self, shader_name: str):
        """
        Updates shader attributes
        :param shader_name: shader to update
        """
        self.shaders[shader_name].update_model_matrix(self.model_matrix)
        self.shaders[shader_name].update_time()

    @staticmethod
    def format_color_array(color: np.ndarray, num_vertices: int) -> np.ndarray:
        """
        preprocess a given color array and bring it to size (m, 3)
        :param color: the original color array
        :param num_vertices: number of vertices (m)
        :return: color array (m, 3)
        """
        # type checking
        if isinstance(color, (list, tuple)):
            color = np.array(color)
        elif not isinstance(color, np.ndarray):
            raise ValueError("Color has to be a tuple, list or np.ndarray")
        # dimension checking
        if color.ndim == 1 and color.shape[0] == 3:
            color = np.full((num_vertices, 3), color)  # bring array to size (m, 3)
        elif color.ndim == 2 and color.shape[1] == 3:
            pass
        else:
            raise ValueError("Color array has to be 1 or 2 dimensional with each color having 3 entries")
        return color

    def update_camera(self, *args, **kwargs):
        """
        update camera parameters for every shader
        :param args: forwarded arguments
        :param kwargs: forwarded keyword arguments
        """
        for key in self.shaders.keys():
            self.shaders[key].update_camera(*args, **kwargs)

    def update_object(self, vertices: np.ndarray = None, colors: np.ndarray = None):
        """
        Update vertices and/or colors of the model
        :param vertices: vertices array (m, 3)
        :param colors: color array (m, 3) pr (3,)
        """
        if vertices is not None:
            self._vertices = np.array(vertices, dtype=np.float32)
            self._normals = compute_normals(self._indices, self._vertices)
            self.vao.set_vbo("normal", self._normals)
            self.vao.set_vbo("position", self._vertices)

        if colors is not None:
            self._colors = self.format_color_array(colors, self._vertices.shape[0])
            self.vao.set_vbo("color", colors[:, :3])
