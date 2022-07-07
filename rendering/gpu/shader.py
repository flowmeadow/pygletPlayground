#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Handles loading, linking and use of GLSL shaders
@File      : shader.py
@Time      : 31.08.21 23:49
@Author    : flowmeadow
"""
import os

from pyglet.gl import *
# from OpenGL.GL import shaders
# from OpenGL.GLUT import *
import ctypes as ct
import numpy as np
import time

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class Shader:
    """
    Handles loading, linking and use of GLSL shaders
    """

    def __init__(self, shader_name: str, model_base="base", num_lights=1):
        """
        Create program and compile shader
        :param shader_name: file name of the shader without extension.
                A '*.vert' and '*.frag' file of the same name must be available.
        """
        self.start_time = time.time()

        self.model_base = model_base
        self.program = glCreateProgram()

        file_path = f"{CURRENT_PATH}/../../shader/{model_base}/{shader_name}/{shader_name}"
        # load shader file text
        with open(f"{file_path}.vert", "r") as f:
            vs_src = f.readlines()
        with open(f"{file_path}.frag", "r") as f:
            fs_src = f.readlines()

        # compile shader
        vs = self.load_shader(vs_src, GL_VERTEX_SHADER, file_path)
        if not vs:
            raise ValueError("Vertex shader could not be loaded")
        fs = self.load_shader(fs_src, GL_FRAGMENT_SHADER, file_path)
        if not fs:
            raise ValueError("Fragment shader could not be loaded")

        # compile program
        # self.program = shaders.compileProgram(vs, fs, **dict(validate=True))
        self.program = glCreateProgram()
        glAttachShader(self.program, vs)
        glAttachShader(self.program, fs)

        # link program
        glLinkProgram(self.program)

        # check link status
        status = ct.c_int(0)

        # TODO: Nothing works here
        # glGetShaderiv(self.program, GL_LINK_STATUS, ct.byref(status))
        # if not status:
        #     log = ct.create_string_buffer(status.value)
        #     # retrieve the log text
        #     glGetShaderInfoLog(self.program, status, None, log)  # TODO not working
        #     raise Exception(log)

        glDeleteShader(vs)
        glDeleteShader(fs)

        # set uniforms
        self.model_matrix_loc = glGetUniformLocation(self.program, "modelMatrix".encode('ascii'))
        self.camera_pos_loc = glGetUniformLocation(self.program, "cameraPos".encode('ascii'))
        self.camera_view_loc = glGetUniformLocation(self.program, "cameraView".encode('ascii'))

        self.time_loc = glGetUniformLocation(self.program, "iTime".encode('ascii'))

        num_lights_loc = glGetUniformLocation(self.program, "iLights".encode('ascii'))

        # start configuration
        self.use()
        glUniform1ui(num_lights_loc, ct.c_uint(num_lights))  # set number of light sources
        self.un_use()

    def __del__(self):
        """
        Delete program
        """
        # TODO: Not working
        # glDeleteProgram(self.program)

    def use(self) -> None:
        """
        Select the current program
        """
        glUseProgram(self.program)

    @staticmethod
    def un_use() -> None:
        """
        Unselect the current program
        """
        glUseProgram(0)

    @staticmethod
    def load_shader(src: str, shader_type: int, file_path: str) -> int:
        """
        Compile a shader
        :param src: text of the shader file
        :param shader_type: type of the shader (GL_VERTEX_SHADER or GL_FRAGMENT_SHADER)
        :return: shader id
        """
        extensions = {GL_FRAGMENT_SHADER: 'frag', GL_VERTEX_SHADER: 'vert'}

        # convert source text
        c_text = (ct.c_char_p * len(src))(*[line.encode('utf-8') for line in src])

        # create shader
        shader = glCreateShader(shader_type)
        glShaderSource(shader, len(src), ct.cast(ct.pointer(c_text), ct.POINTER(ct.POINTER(ct.c_char))), None)

        # compile shader
        glCompileShader(shader)

        # check shader status
        status = ct.c_int(0)
        glGetShaderiv(shader, GL_COMPILE_STATUS, ct.byref(status))
        if not status:
            log = ct.create_string_buffer(status.value)
            # retrieve the log text
            glGetShaderInfoLog(shader, status, None, log)  # TODO not working

            glDeleteShader(shader)
            raise ImportError(f"{file_path}.{extensions[shader_type]}:\n {log.value}")
        return shader

    def update_model_matrix(self, matrix: np.array) -> None:
        """
        Updates the uniform modelMatrix attribute
        :param matrix: transformation matrix [4, 4]
        """
        self.use()
        mat = matrix.flatten("F")
        glUniformMatrix4fv(self.model_matrix_loc, 1, False, (ct.c_float * 16)(*mat))
        self.un_use()

    def update_camera(self, camera_pos, camera_view):
        self.use()
        glUniform3f(self.camera_pos_loc, *np.array(camera_pos, dtype=np.float32).flatten("F"))
        glUniform3f(self.camera_view_loc, *np.array(camera_view, dtype=np.float32).flatten("F"))
        self.un_use()

    def update_time(self):
        self.use()
        t = int(1000 * (time.time() - self.start_time))
        glUniform1ui(self.time_loc, t)
        self.un_use()
