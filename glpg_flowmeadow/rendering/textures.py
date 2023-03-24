#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Standalone functions for texture image operations
@File      : textures.py
@Project   : pygletPlayground
@Time      : 07.12.22 19:08
@Author    : flowmeadow
"""
import ctypes
import ctypes as ct
import os
from dataclasses import dataclass
from typing import Tuple

import numpy as np
import PIL.Image
from pyglet.gl import *

TEXTURE_FORMATS = {"RGB": GL_RGB, "L": GL_DEPTH_COMPONENT}


@dataclass
class ImageData:
    """
    Dataclass for images that contains a ctypes byte array, the size of the image in pixels and the Pillow image format.
    """

    c_data: ctypes.Array
    img_size: Tuple[int, int]
    img_mode: str


def img_file_to_byte_array(path: str, save: bool = False) -> ImageData:
    """
    Converts an image file to a ctypes array and returns it as an ImageData object.
    :param path: path to the image file (supported file types: PNG, JPEG, PPM, GIF, TIFF, and BMP)
    :param save: If True, the ctypes array is saved in a custom format (IBA) in the same directory. This format can be
    loaded much faster which is useful for a high amount of textures or high resolution images. Be sure to have enough
    disk space, as those files can get quite big.
    :return: ImageData object
    """
    # open image and convert it to a numpy array
    img = PIL.Image.open(path)  # .jpg, .bmp, etc. also work
    img_data = np.array(list(img.getdata()), np.int8)

    img_size, img_mode = img.size, img.mode
    data_type = np.ubyte  # default

    # transform array and get data length
    data = np.array(img_data, dtype=data_type).flatten()
    data_count = data.shape[0]

    # convert to ctypes array
    c_data = (ct.c_ubyte * data_count)()
    c_data[:] = data

    if save:
        # save ctypes array as a binary file
        directory, base = os.path.split(path)
        file_name, _ = os.path.splitext(base)
        out_path = os.path.join(directory, f"{file_name}.iba")
        with open(out_path, "wb") as f:
            f.write(data)
        # save image size and mode as metadata
        os.setxattr(out_path, "user.img_width", bytearray(str(img_size[0]), "utf-8"))
        os.setxattr(out_path, "user.img_height", bytearray(str(img_size[1]), "utf-8"))
        os.setxattr(out_path, "user.img_mode", bytearray(str(img_mode), "utf-8"))

    return ImageData(c_data, img_size, img_mode)


def load_image_byte_array(path: str) -> ImageData:
    """
    Given a file path, image data is loaded and returned as an ImageData object
    :param path: file path to the image object
    :return: ImageData object
    """
    _, extension = os.path.splitext(path)

    # load from image file
    if extension in [".jpg", ".jpeg"]:
        img_data = img_file_to_byte_array(path)
    # load from image byte array file (custom)
    elif extension in [".iba"]:
        with open(path, "rb") as f:
            c_data = f.read()
        w = os.getxattr(path, "user.img_width")
        h = os.getxattr(path, "user.img_height")
        img_mode = os.getxattr(path, "user.img_mode").decode("utf-8")
        img_size = (int(w), int(h))
        img_data = ImageData(c_data, img_size, img_mode)
    else:
        raise NotImplementedError()
    return img_data


def load_texture(path: str):
    """
    Given a file path, image data loaded and stored as a texture on the GPU
    :param path: file path to the image object
    :return: OpenGL location of the texture
    """
    img_data = load_image_byte_array(path)
    c_data, img_size, img_mode = img_data.c_data, img_data.img_size, img_data.img_mode
    img_format = TEXTURE_FORMATS[img_mode]

    id = GLuint()
    glEnable(GL_TEXTURE_2D)

    glGenTextures(1, id)
    glBindTexture(GL_TEXTURE_2D, id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, img_format, img_size[0], img_size[1], 0, img_format, GL_UNSIGNED_BYTE, c_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    glDisable(GL_TEXTURE_2D)

    return id


def wrap_texture(vertices: np.ndarray, method: str = "cylinder") -> np.ndarray:
    """
    Computes texture coordinates for an array of vertices
    :param vertices: vertex array [n, 3]
    :param method: wrapping method
    :return: texture coordinate array [n, 2]
    """
    min_vec = np.min(vertices, axis=0)
    max_vec = np.max(vertices, axis=0)
    mid_vec = (max_vec + min_vec) / 2

    if method == "cylinder":
        # cylindrical wrapping method
        vertices_mid = vertices[:, :2] - mid_vec[:2]
        x, y = vertices_mid[:, 0], vertices_mid[:, 1]
        r = (1.0 + -np.arctan2(x, y) / np.pi) / 2

        z_min, z_max = min_vec[2], max_vec[2]
        z = 1.0 - (vertices[:, 2] - z_min) / (z_max - z_min)
        return np.array([r, z]).T
    else:
        raise NotImplementedError()
