#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Handles loading, linking and use of GLSL shaders
@File      : shader.py
@Time      : 31.08.21 23:49
@Author    : flowmeadow
"""
import ctypes as ct
import importlib
import os
import time
from typing import Union

import numpy as np
from pyglet.gl import *


class Shader:
    """
    Handles loading, linking and use of GLSL shaders
    """

    def __init__(self, shader: Union[int, str], model_base: str = "base", num_lights: int = 1, num_textures: int = 0):
        """
        Create program and compile shader
        :param shader: filename of the shader without extension. A '*.vert' and '*.frag' file must be available.
        :param model_base: parent directory of the shader. Other models might require different shaders (e.g. material)
        :param num_lights: number of light sources
        """
        self.start_time = time.time()  # define time constant

        self.model_base = model_base
        self.program = glCreateProgram()

        # load shader text
        if isinstance(shader, str):
            shader_path = shader
            vs_cnt, fs_cnt = 0, 0
            for file in os.listdir(shader_path):
                if file.endswith(".vert"):
                    with open(f"{shader_path}/{file}", "r") as f:
                        vs_src = ''.join(f.readlines())
                    vs_cnt += 1
                if file.endswith(".frag"):
                    with open(f"{shader_path}/{file}", "r") as f:
                        fs_src = ''.join(f.readlines())
                    fs_cnt += 1
            if vs_cnt != 1 or fs_cnt != 1:
                raise ImportError("Given directory must have exactly one vertex (.vert) and one fragment (.frag) file")
        elif isinstance(shader, int):
            name_list = ["flat", "gouraud", "blinn_phong", "toon"]
            shader_name = name_list[shader]
            shader_txt = importlib.import_module(f"glpg.shader.{model_base}.{shader_name}.{shader_name}")

            vs_src = shader_txt.vert_txt
            fs_src = shader_txt.frag_txt
        else:
            raise NotImplementedError()

        # compile shader
        vs = self.load_shader(vs_src, GL_VERTEX_SHADER, shader)
        if not vs:
            raise ValueError("Vertex shader could not be loaded")
        fs = self.load_shader(fs_src, GL_FRAGMENT_SHADER, shader)
        if not fs:
            raise ValueError("Fragment shader could not be loaded")

        # compile program
        self.program = glCreateProgram()
        glAttachShader(self.program, vs)
        glAttachShader(self.program, fs)

        # link program
        glLinkProgram(self.program)

        # not needed anymore
        glDeleteShader(vs)
        glDeleteShader(fs)

        # get locations and set uniforms
        self.use()
        self.model_matrix_loc = glGetUniformLocation(self.program, "modelMatrix".encode("ascii"))
        self.camera_pos_loc = glGetUniformLocation(self.program, "cameraPos".encode("ascii"))
        self.camera_view_loc = glGetUniformLocation(self.program, "cameraView".encode("ascii"))
        self.time_loc = glGetUniformLocation(self.program, "iTime".encode("ascii"))
        num_lights_loc = glGetUniformLocation(self.program, "iLights".encode("ascii"))
        num_textures_loc = glGetUniformLocation(self.program, "iTextures".encode("ascii"))
        glUniform1i(num_lights_loc, ct.c_int32(num_lights))  # set number of light sources
        glUniform1i(num_textures_loc, ct.c_int32(num_textures))  # set number of textures
        for t_idx in range(num_textures):
            tex_loc = glGetUniformLocation(self.program, f"objTexture{t_idx}".encode("ascii"))
            glUniform1i(tex_loc, t_idx)
        self.un_use()

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
    def load_shader(src: str, shader_type: int, file_name: str = None) -> int:
        """
        Compile a shader
        :param src: text of the shader file
        :param shader_type: type of the shader (GL_VERTEX_SHADER or GL_FRAGMENT_SHADER)
        :param file_name: file_name of the shader file. Used for debugging only
        :return: shader id
        """
        extensions = {GL_FRAGMENT_SHADER: "frag", GL_VERTEX_SHADER: "vert"}

        # convert source text
        c_text = (ct.c_char_p * len(src))(*[line.encode("utf-8") for line in src])

        # create shader
        shader = glCreateShader(shader_type)
        glShaderSource(shader, len(src), ct.cast(ct.pointer(c_text), ct.POINTER(ct.POINTER(ct.c_char))), None)

        # compile shader
        glCompileShader(shader)

        # check shader status
        status = ct.c_int(0)
        glGetShaderiv(shader, GL_COMPILE_STATUS, ct.byref(status))

        if not status:
            # retrieve the log text
            glGetShaderiv(shader, GL_INFO_LOG_LENGTH, ct.byref(status))
            log = ct.create_string_buffer(status.value)
            glGetShaderInfoLog(shader, status, None, log)
            log_text = log.value.decode("utf-8")

            glDeleteShader(shader)

            file_name = file_name if file_name else "unknown"
            raise ImportError(f"{file_name}.{extensions[shader_type]}:\n\n{log_text}")
        return shader

    def update_model_matrix(self, matrix: np.array):
        """
        Updates the uniform modelMatrix attribute
        :param matrix: transformation matrix [4, 4]
        """
        self.use()
        mat = matrix.flatten("F")
        glUniformMatrix4fv(self.model_matrix_loc, 1, False, (ct.c_float * 16)(*mat))
        self.un_use()

    def update_camera(self, camera_pos: np.ndarray, camera_view: np.ndarray):
        """
        update camera attributes
        :param camera_pos: camera position array (3,)
        :param camera_view: camera view direction array (3,)
        """
        self.use()
        glUniform3f(self.camera_pos_loc, *np.array(camera_pos, dtype=np.float32).flatten("F"))
        glUniform3f(self.camera_view_loc, *np.array(camera_view, dtype=np.float32).flatten("F"))
        self.un_use()

    def update_time(self):
        """
        update runtime in milliseconds
        """
        self.use()
        t = int(1000 * (time.time() - self.start_time))
        glUniform1i(self.time_loc, t)
        self.un_use()
