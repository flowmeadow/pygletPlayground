#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : TODO
@File      : methods.py
@Project   : pygletPlayground
@Time      : 29.03.23 22:14
@Author    : flowmeadow
"""
import ctypes
import ctypes as ct
import os
import warnings
from dataclasses import dataclass
from typing import Tuple, Optional, Union, List

import numpy as np
import PIL.Image
from pyglet.gl import *
from sys import platform

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
    img_data = np.array(list(img.getdata()), np.uint8)

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


def load_image_byte_array(texture: Union[np.ndarray, str]) -> ImageData:
    """
    Given a file path, image data is loaded and returned as an ImageData object
    :param texture: Numpy array or file path to the image object
    :return: ImageData object
    """
    if isinstance(texture, np.ndarray):
        # transform array and get data length
        arr = np.uint8(texture * 255)
        img_size = arr.shape[:2]
        if len(arr.shape) == 2:
            img_mode = "L"
        elif len(arr.shape) == 3:
            img_mode = "RGB"
        else:
            raise NotImplementedError()

        # convert to ctypes array
        arr = arr.flatten()
        data_count = arr.shape[0]
        c_data = (ct.c_ubyte * data_count)()
        c_data[:] = arr

        img_data = ImageData(c_data, img_size, img_mode)

    elif isinstance(texture, str):
        _, extension = os.path.splitext(texture)
        # load from image file
        if extension in [".jpg", ".jpeg", ".png", ".bmp"]:
            img_data = img_file_to_byte_array(texture)
        # load from image byte array file (custom)
        elif extension in [".iba"]:
            with open(texture, "rb") as f:
                c_data = f.read()
            w = os.getxattr(texture, "user.img_width")
            h = os.getxattr(texture, "user.img_height")
            img_mode = os.getxattr(texture, "user.img_mode").decode("utf-8")
            img_size = (int(w), int(h))
            img_data = ImageData(c_data, img_size, img_mode)
        else:
            raise NotImplementedError()
    else:
        raise NotImplementedError()
    return img_data


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
    elif method == "xy-projection":
        tex_coords = (vertices[:, :2] - min_vec[:2]) / (max_vec[:2] - min_vec[:2])
        return tex_coords
    else:
        raise NotImplementedError()
