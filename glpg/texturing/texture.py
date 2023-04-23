#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Texture object class for texture upload and manipulation
@File      : texture.py
@Project   : pygletPlayground
@Time      : 28.03.23 22:15
@Author    : flowmeadow
"""
from glpg.texturing.methods import *


class Texture:
    """
    Texture object class for texture upload and manipulation
    """

    # transition dictionary from Pillow to OpenGL notation
    texture_formats = {"RGB": GL_RGB, "L": GL_DEPTH_COMPONENT}

    # default texture parameters
    _defaults = {
        GL_TEXTURE_WRAP_S: GL_REPEAT,
        GL_TEXTURE_WRAP_T: GL_REPEAT,
        GL_TEXTURE_MIN_FILTER: GL_LINEAR_MIPMAP_LINEAR,
        GL_TEXTURE_MAG_FILTER: GL_LINEAR,
    }

    def __init__(self, texture: Union[np.ndarray, str], texture_params: dict = None):
        """
        :param texture: file path to an image or numpy array holding the image information
        :param texture_params: dictionary of texture parameters
        """
        # get the image data
        self.img_data = load_image_byte_array(texture)

        # define locations for texture and sampler
        self.location = GLuint()
        self.sampler_id = GLuint()
        glEnable(GL_TEXTURE_2D)
        glGenTextures(1, self.location)
        glGenSamplers(1, self.sampler_id)
        glDisable(GL_TEXTURE_2D)

        # load texture to GPU
        self.load()

        # update sampler parameter
        tex_params = self._defaults.copy()
        if isinstance(texture_params, dict):
            for key, val in texture_params.items():
                tex_params[key] = val
        for key, val in tex_params.items():
            self.update_param(key, val)

    def load(self, texture: Optional[Union[np.ndarray, str]] = None):
        """
        Upload or update texture data
        :param texture: file path to an image or numpy array holding the image information
        """
        if texture is not None:
            self.img_data = load_image_byte_array(texture)

        c_data, img_size, img_mode = self.img_data.c_data, self.img_data.img_size, self.img_data.img_mode
        img_format = self.texture_formats[img_mode]

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.location)
        glTexImage2D(GL_TEXTURE_2D, 0, img_format, img_size[0], img_size[1], 0, img_format, GL_UNSIGNED_BYTE, c_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindSampler(0, 0)
        glDisable(GL_TEXTURE_2D)

        return self

    def update_param(self, param_type: int, param_value: int):
        """
        Updates sampler parameter
        :param param_type: Defines which parameter to change (e.g., GL_TEXTURE_MAG_FILTER)
        :param param_value: Value that is set (e.g., GL_LINEAR)
        """
        glSamplerParameteri(self.sampler_id, param_type, param_value)
