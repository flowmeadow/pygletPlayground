#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Converts each file in the given directory to an IBA file
@File      : update_textures.py
@Project   : pygletPlayground
@Time      : 08.12.22 22:26
@Author    : flowmeadow
"""
import os
from glpg.texturing.methods import img_file_to_byte_array


def update_textures(base_path: str):
    path_list = [os.path.join(dir_path, f) for dir_path, _, file_names in os.walk(base_path) for f in file_names]
    for path in path_list:
        directory, base = os.path.split(path)
        file_name, extension = os.path.splitext(base)
        if extension in [".jpeg", ".jpg"] and f"{file_name}.iba" not in os.listdir(directory):
            print(f"Loading, converting and saving image {path} ...")
            img_file_to_byte_array(path, save=True)


if __name__ == "__main__":
    base_path = "demo_textures/"
    update_textures(base_path)
