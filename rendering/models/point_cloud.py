#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Simple point cloud object
@File      : point_cloud.py
@Project   : pygletPlayground
@Time      : 30.03.22 23:12
@Author    : flowmeadow
"""
from typing import Optional

import numpy as np
from pyglet.gl import *


class PointCloud:
    """
    Simple point cloud object
    """

    def __init__(self, points: np.ndarray, colors: Optional[np.ndarray] = None, point_size: int = 10):
        """
        Object that draws several 3D points as dots into the scene
        :param points: point coordinates (m, 3)
        :param colors: point colors (m, 3)
        :param point_size: point size in pixels
        """
        # define vertices and colors
        self.points = points
        self.colors = np.full((1.0, 1.0, 1.0), self.points.shape[0]) if colors is None else colors
        self.point_size = point_size

    def draw(self):
        """
        draw the points into the scene
        :return:
        """
        glEnable(GL_POINT_SMOOTH)
        glPointSize(self.point_size)
        glBegin(GL_POINTS)
        for p, c in zip(self.points, self.colors):
            glColor3d(c[0], c[1], c[2])
            glVertex3d(p[0], p[1], p[2])
        glEnd()
