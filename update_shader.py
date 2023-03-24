#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Generates a python file for each shader, containing the raw GLSL code as string
@File      : update_shader.py
@Project   : pygletPlayground
@Time      : 08.07.22 16:41
@Author    : flowmeadow
"""
import os


def main():
    # iterate through shader directory
    print("UPDATE SHADER FILES:")
    for directory, sub_dirs, files in os.walk("glpg_flowmeadow/shader"):
        vert_txt, frag_txt = None, None
        # check fore each directory if there are a *.vert and *.frag file and read them
        if len(files) > 0:
            for file in files:
                if file.endswith(".vert"):
                    with open(f"{directory}/{file}", "r") as f:
                        vert_txt = f.read()

                if file.endswith(".frag"):
                    with open(f"{directory}/{file}", "r") as f:
                        frag_txt = f.read()

            # write the text in a python file
            if vert_txt is not None and frag_txt is not None:
                file_name = os.path.basename(directory)
                with open(f"{directory}/{file_name}.py", "w") as f:
                    txt = f'vert_txt = """\n{vert_txt}\n"""\n\nfrag_txt = """\n{frag_txt}\n"""'
                    f.write(txt)
                print(f"  -- Updated shader '{file_name}'")


if __name__ == "__main__":
    main()
