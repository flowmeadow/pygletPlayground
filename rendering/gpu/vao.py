#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Vertex array object that handles several buffer objects.
@File      : vao.py
@Time      : 31.08.21 23:50
@Author    : flowmeadow
"""

from typing import Optional

import numpy as np
from pyglet.gl import *
import ctypes as ct


class VAO:
    """
    Vertex array object that handles several buffer objects.
    """

    # TODO: not working with a combination of GL_QUADS and GL_TRIANGLES
    def __init__(self, indices: np.array, object_id: int = GL_TRIANGLES):
        """
        Initialize VAO
        (l=3: GL_TRIANGLES, l=4: GL_QUADS)
        :param object_id: can be GL_TRIANGLES or GL_QUADS
        :param indices: indices array of the model [m, l]
        """
        self.object_id = object_id  # GL_TRIANGLES or GL_QUADS
        self.vertices_per_face = indices.shape[1]

        data_type = np.uint32  # index data type
        self.index_size = data_type().itemsize  # bytes per index (default: 32 bit)

        # transform array and get data length
        indices = np.array(indices, dtype=data_type).flatten()  # flatten 2D array
        self.index_count = indices.shape[0]  # number of indices

        # generate VAO
        self.vao = GLuint()
        glGenVertexArrays(1, self.vao)
        glBindVertexArray(self.vao)

        # generate VBOs
        self.ibo = GLuint()
        self.vbo = GLuint()
        self.cbo = GLuint()
        self.nbo = GLuint()

        glGenBuffers(1, self.ibo)  # indices
        glGenBuffers(1, self.vbo)  # vertex
        glGenBuffers(1, self.cbo)  # color
        glGenBuffers(1, self.nbo)  # normals

        # bind index data
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        byte_length = self.index_count * self.index_size
        c_data = (ct.c_uint * self.index_count)(*indices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, byte_length, c_data, GL_STATIC_DRAW)
        glBindVertexArray(0)

    def __del__(self) -> None:
        """
        Delete VBOs and VAO
        """
        # TODO: Again... not working
        # glDeleteBuffers(1, self.ibo)
        # glDeleteBuffers(1, self.ibo)
        # glDeleteBuffers(1, ct.pointer(self.ibo))
        # glDeleteBuffers(1, self.vbo)
        # glDeleteBuffers(1, [self.cbo])
        # glDeleteBuffers(1, [self.nbo])
        # glDeleteVertexArrays(1, self.vao)

    def set_vbo(self, attr_name: str, data: np.array) -> None:
        """
        Assign vertex attributes to VAO
        (k=2: textures, k=3: vertices, k=4: colors)
        :param attr_name: name of the vertex attribute ('position', 'color', 'normal')
        :param data: array containing the vertex attribute data [n, k]
        """
        glBindVertexArray(self.vao)
        # assign per vertex position information
        if attr_name == "position":
            glEnableClientState(GL_VERTEX_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            self.assign_vbo_data(data)
            glVertexPointer(3, GL_FLOAT, 0, None)
        # assign per vertex color information
        elif attr_name == "color":
            glEnableClientState(GL_COLOR_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, self.cbo)
            self.assign_vbo_data(data)
            glColorPointer(3, GL_FLOAT, 0, None)
        # assign per vertex normal information
        elif attr_name == "normal":
            glEnableClientState(GL_NORMAL_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, self.nbo)
            self.assign_vbo_data(data)
            glNormalPointer(GL_FLOAT, 0, None)
        # TODO: Texture Coords are not defined yet. Do I miss something else?
        else:
            raise NotImplementedError("Unknown ID")
        glBindVertexArray(0)

    def draw(self, num_indices: Optional[int] = None, offset: int = 0) -> None:
        """
        Draw the VAO
        :param num_indices: number of indices that are drawn
        :param offset: defines the first index to draw
        """
        if num_indices is None:  # if nothing given, draw everything
            num_indices = self.index_count
        offset = int(offset * self.vertices_per_face)
        num_indices = int(num_indices * self.vertices_per_face)

        # bind VAO and draw elements
        glBindVertexArray(self.vao)
        glDrawElements(self.object_id, num_indices, GL_UNSIGNED_INT, ct.c_void_p(offset * self.index_size))
        glBindVertexArray(0)

    def draw_vertices(self, num_indices: Optional[int] = None, offset: int = 0):
        """

        :param num_indices:
        :param offset:
        :return:
        """



    @staticmethod
    def assign_vbo_data(data: np.array) -> None:
        """
        Assign vertex attributes to VAO
        (k=2: textures, k=3: vertices, k=4: colors)
        :param data: array containing the vertex attribute data [n, k]
        """
        data_type = np.float32  # default
        # transform array and get data length
        data = np.array(data, dtype=data_type).flatten()
        data_count = data.shape[0]
        # define number of bytes and transform data
        byte_length = data_count * data_type().itemsize
        c_data = (ct.c_float * data_count)(*data)
        # assign data
        glBufferData(GL_ARRAY_BUFFER, byte_length, c_data, GL_STATIC_DRAW)
