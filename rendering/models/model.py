#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce :
@File      : model.py
@Time      : 31.08.21 19:12
@Author    : flowmeadow
"""

from typing import Union, List, Optional

import numpy as np
from pyglet.gl import *

from transformations.methods import compute_normals, flip_inside_out, rotate_vec
from rendering.gpu.shader import Shader

from rendering.gpu.vao import VAO


class Model:

    default_shader = "blinn_phong"
    default_color = (0.0, 0.0, 1.0)

    def __init__(
        self,
        vertices: np.array,
        indices: np.array,
        color: Optional[Union[np.array, List[float]]] = default_color,
        rotation=(1.0, 0.0, 0.0, 0.0),
        scale=(1.0, 1.0, 1.0),
        translation=(0.0, 0.0, 0.0),
        shader_name: Union[str, List[str]] = default_shader,
        inside_out=False,
        num_lights=1,
        **kwargs,
    ) -> None:
        """
        TODO: GL_QUADS not implemented
        :param vertices:
        :param indices:
        :param rotation:
        :param scale:
        :param translation:
        :param shader_name:
        :param flat_geometry:
        :param kwargs:
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

        self.vao = VAO(indices, object_id=GL_TRIANGLES)
        self.vao.set_vbo("position", vertices)
        self.vao.set_vbo("color", colors[:, :3])
        self.vao.set_vbo("normal", normals)

        self.model_matrix = np.identity(4, dtype=np.float32)
        self.operations = []

        self.shaders = dict()
        if isinstance(shader_name, str):
            shader_name = [shader_name]
        for s in shader_name:
            self.shaders[s] = Shader(s, num_lights=num_lights)
        self.first_shader = shader_name[0]

    def rotate(self, angle, x, y, z):
        rot_vec = [angle, x, y, z]
        axis = np.array([x, y, z])
        l, m, n = axis / np.linalg.norm(axis)

        angle = np.pi * angle / 180.0
        s, c = np.sin(angle), np.cos(angle)
        rot_transform = np.array(
            [
                [l * l * (1 - c) + c, m * l * (1 - c) - n * s, n * l * (1 - c) + m * s, 0.0],
                [l * m * (1 - c) + n * s, m * m * (1 - c) + c, n * m * (1 - c) - l * s, 0.0],
                [l * n * (1 - c) - m * s, m * n * (1 - c) + l * s, n * n * (1 - c) + c, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        self.model_matrix = self.model_matrix @ rot_transform

        self.operations.append([glRotatef, rot_vec])

    def scale(self, x, y, z):
        scale_vec = [x, y, z]
        scale_transform = np.identity(4, dtype=np.float)
        np.fill_diagonal(scale_transform[:3, :3], scale_vec)
        self.model_matrix = self.model_matrix @ scale_transform

        self.operations.append([glScalef, scale_vec])

    def translate(self, x, y, z):
        trans_vec = [x, y, z]
        trans_transform = np.identity(4, dtype=np.float)
        trans_transform[:-1, 3] = trans_vec
        self.model_matrix = self.model_matrix @ trans_transform
        self.operations.append([glTranslatef, trans_vec])

    def reset(self):
        self.model_matrix = np.identity(4, dtype=np.float32)
        self.operations = []

    def draw(self, shader_name=None, num_indices=None, offset=0) -> None:
        if shader_name is None:
            shader_name = self.first_shader

        self.update_shader(shader_name)
        self.shaders[shader_name].use()

        glPushMatrix()

        for operation, args in self.operations:
            operation(*args)
        self.vao.draw(num_indices, offset)
        glPopMatrix()
        glFlush()

        self.shaders[shader_name].un_use()

        self.reset()

    def update_shader(self, shader_name):
        self.shaders[shader_name].update_model_matrix(self.model_matrix)
        self.shaders[shader_name].update_time()

    @staticmethod
    def format_color_array(color, num_vertices):
        if isinstance(color, (list, tuple)):
            color = np.array(color)
        elif not isinstance(color, np.ndarray):
            raise ValueError("Color has to be a tuple, list or np.ndarray")

        if color.ndim == 1 and color.shape[0] == 3:
            color = np.full((num_vertices, 3), color)

        elif color.ndim == 2 and color.shape[1] == 3:
            pass

        else:
            raise ValueError("Color array has to be 1 or 2 dimensional with each color having 3 entries")

        return color

    def update_camera(self, *args, **kwargs):
        for key in self.shaders.keys():
            self.shaders[key].update_camera(*args, **kwargs)

    def update_object(self, vertices=None, colors=None):
        if vertices is not None:
            self._vertices = np.array(vertices, dtype=np.float32)
            self._normals = compute_normals(self._indices, self._vertices)
            self.vao.set_vbo("normal", self._normals)
            self.vao.set_vbo("position", self._vertices)

        if colors is not None:
            self._colors = self.format_color_array(colors, self._vertices.shape[0])
            self.vao.set_vbo("color", colors[:, :3])
