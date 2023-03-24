#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : General OpenGL application class, that follows a certain drawing pipeline
@File      : gl_screen.py
@Project   : pygletPlayground
@Time      : 02.10.21 13:00
@Author    : flowmeadow
"""
from abc import ABCMeta, abstractmethod

from pyglet.gl import *

from glpg.camera.camera import Camera
from glpg.display.base import Base


class GLScreen(Base):
    """
    General OpenGL application class, that follows a certain drawing pipeline
    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        """
        :param kwargs: forwarded keyword arguments
        """
        # TODO: How to deal with debug mode
        #       do NOT allow fullscreen only in debug mode
        #       Enable mouse in debug mode (e.g. camera.fly_motion)
        # gettrace = getattr(sys, "gettrace", None)
        # if gettrace():
        #     kwargs["fullscreen"] = False

        super().__init__(**kwargs)

        # initialize camera
        self.cam = Camera()

    def init_gl(self):
        """
        Initialize OpenGL settings
        """
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_MULTISAMPLE)

    def draw_frame(self):
        """
        Run drawing pipeline
        """
        # initialize perspective
        glLoadIdentity()
        gluPerspective(45, (self.width / self.height), 0.1, 50.0)

        # configure OpenGL settings
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # prepare next frame
        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glClearColor(0.0, 0.0, 0.0, 0.0)
        # glClearDepth(1.0)
        # glLoadIdentity()

        # handle the gathered events if necessary (empty by default)
        self.cam.update(self)
        self.handle_events()
        glFlush()

        # initialize camera
        gluLookAt(
            *self.cam.camera_pos,
            *(self.cam.camera_pos + self.cam.camera_view),
            *self.cam.camera_up,
        )
        # draw world objects (empty by default)
        self.draw_world()
        glFlush()

        # draw on screen
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0.0, self.height, -1.0, 1.0)
        self.draw_screen()
        glEnable(GL_DEPTH_TEST)

        # # TODO: Check computational cost of this. It can be optional
        # glDisable(GL_DEPTH_TEST)
        # # compute inverse model view projection matrix
        # glLoadIdentity()
        #
        # glGetFloatv(GL_PROJECTION_MATRIX, self._projection_matrix)
        # glGetFloatv(GL_MODELVIEW_MATRIX, self._view_matrix)
        # self.inverse_matrix = np.linalg.inv(to_matrix(self._view_matrix) @ to_matrix(self._projection_matrix))
        #
        # # draw screen objects (empty by default)
        # glFlush()
        # glEnable(GL_DEPTH_TEST)

    @abstractmethod
    def handle_events(self) -> None:
        """
        handle pygame events and do other stuff before drawing
        :return: None
        """
        pass

    @abstractmethod
    def draw_world(self) -> None:
        """
        draw objects in the world
        :return: None
        """
        pass

    @abstractmethod
    def draw_screen(self) -> None:
        """
        draw objects onto the screen (e.g. GUI, text, images).
        :return: None
        """
        pass
