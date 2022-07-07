#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : several methods to handle specific OpenGL functions
@File      : rendering.py
@Time      : 09.09.21 00:23
@Author    : flowmeadow
"""
import numpy as np
from pyglet.gl import *
import pyglet

# def draw_text_3D(x_txt: int, y_txt: int, z_txt: int, text: str, color=(1.0, 1.0, 1.0)) -> None:
#     """
#     Draws a given string into the scene.
#     :param x_txt: x-position
#     :param y_txt: y_txt-position
#     :param z_txt: z_txt-position
#     :param text: test to draw
#     :param color: color of the text
#     :return: None
#     """
#     font = GLUT_BITMAP_8_BY_13
#     glColor3f(color[0], color[1], color[2])
#     glRasterPos3f(x_txt, y_txt, z_txt)
#     for ch in text:
#         glutBitmapCharacter(font, ord(ch))


def draw_text_2D(x_txt: int, y_txt: int, text: str) -> None:
    label = pyglet.text.Label(
        text, font_name="Consolas", font_size=12, x=x_txt, y=y_txt, anchor_x="left", anchor_y="top"
    )
    label.draw()


def draw_coordinates(R=np.eye(3), t=np.zeros(3), scale=1.) -> None:
    """
    Draws a reference coordinate system in the scene TODO
    :return: None
    """
    center = np.array([0.0, 0.0, 0.0]) + t
    vertices = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    colors = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    glBegin(GL_LINES)
    for v, c in zip(vertices, colors):
        v = (R @ v) * scale + t
        glColor3f(*c)
        glVertex3f(*center)
        glVertex3f(*v)
    glEnd()
    glFlush()


def draw_light(light_pos) -> None:
    """
    Draw a reference for a point light source
    :param light_pos: center of the light source
    :return: None
    """
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(light_pos[0] - 0.1, light_pos[1], light_pos[2])
    glVertex3f(light_pos[0] + 0.1, light_pos[1], light_pos[2])
    glVertex3f(light_pos[0], light_pos[1] - 0.1, light_pos[2])
    glVertex3f(light_pos[0], light_pos[1] + 0.1, light_pos[2])
    glVertex3f(light_pos[0], light_pos[1], light_pos[2] - 0.1)
    glVertex3f(light_pos[0], light_pos[1], light_pos[2] + 0.1)
    glVertex3f(0.0, 0.0, 1.0)
    glEnd()
    glFlush()


def draw_cam(pos, rot_mat, radius, side_num=20, edge_only=True, color=None):
    """
    TODO
    :param pos:
    :param rot_mat:
    :param radius:
    :param side_num:
    :param edge_only:
    :param color:
    :return:
    """
    color = (1.0, 1.0, 1.0) if color is None else color
    glColor3f(*color)
    if edge_only:
        glBegin(GL_LINE_LOOP)
    else:
        glBegin(GL_POLYGON)
    vertices = []

    T = np.eye(4)
    T[:3, :3] = rot_mat
    T[:3, -1] = pos

    for idx in range(0, side_num):
        angle = idx * 2.0 * np.pi / side_num
        vertex = np.array([np.cos(angle) * radius, np.sin(angle) * radius, 0.5])
        vertex = (T @ np.append(vertex, 1.))[:3]
        vertices.append(vertex)
        glVertex3f(*vertex)
    glEnd()

    glBegin(GL_LINES)
    for vertex in vertices:
        glVertex3f(*pos)
        glVertex3f(*vertex)
    glEnd()

    draw_coordinates(rot_mat, pos, scale=0.2)
    glFlush()
