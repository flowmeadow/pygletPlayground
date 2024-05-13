#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : PySide6 widget class to embedd a GLPG application
@File      : gl_widget.py
@Project   : pygletPlayground
@Time      : 13.04.24 10:15
@Author    : flowmeadow
"""
from abc import abstractmethod
from typing import Tuple

import pyglet
from PySide6 import QtCore
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from pyglet.gl import *

from glpg.camera.camera import Camera
from pyglet.window import key
from glpg.display.gl_screen import GLScreen


class GLWidget(QOpenGLWidget):
    """
    PySide6 widget class to embedd a GLPG application
    """
    def __init__(self, parent=None):
        """
        :param parent: [OPTIONAL] parent widget
        """
        super().__init__(parent=parent)

        # set attributes
        self.current_fps = 0.0
        self.display_center = (self.width // 2, self.height // 2)

        # initialize inputs
        self.keys = set()

        # set interval for drawing function
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.my_draw)
        self.timer.setInterval(0)
        self.timer.start()

        # initialize camera
        self.cam = Camera()

    def my_draw(self):
        """
        Update FPS, clear screen and draw next frame
        """
        self.current_fps = pyglet.clock.get_fps()
        pyglet.clock.tick()

        # Force widget to update, otherwise paintGL will not be called.
        self.update()

    def initializeGL(self):
        """
        Initialize OpenGL settings
        """
        GLScreen.init_gl(self)

        # run custom initialisation
        self.init_gl()

    def paintGL(self):
        """Pyglet equivalent of on_draw event for window"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        GLScreen.draw_frame(self)

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Update pressed keyboard inputs. By default, 'R', 'Q' and 'ESCAPE' close the window. 'R' also sets the
        restart request flag. If those keys should be used differently, this method has to be overwritten by child.
        :param symbol: keyboard symbol (e.g. a, b, c, 1, 2, 3, ...)
        :param modifiers: keyboard modifiers (e.g. ALT, SHIFT, CTRL, ...)
        """
        if symbol in [key.Q, key.ESCAPE]:
            self.close()
        self.keys.add(symbol)

    def on_key_release(self, symbol: int, modifiers: int):
        """
        Update released keyboard inputs
        :param symbol: keyboard symbol (e.g. a, b, c, 1, 2, 3, ...)
        :param modifiers: keyboard modifiers (e.g. ALT, SHIFT, CTRL, ...)
        """
        self.keys.discard(symbol)

    @property
    def size(self) -> Tuple[int, int]:
        """
        :return: window size (width, height)
        """
        return self.width, self.height

    @property
    def width(self) -> int:
        """
        :return: window size (width, height)
        """
        return QOpenGLWidget.width(self)

    @property
    def height(self) -> int:
        """
        :return: window size (width, height)
        """
        return QOpenGLWidget.height(self)

    def close(self):
        """
        Stop clock and close window
        """
        pyglet.clock.unschedule(self.my_draw)
        super().close()

    @abstractmethod
    def init_gl(self) -> None:
        """
        To be overwritten in child class. Initialize lights, models and other GL related stuff here.
        :return: None
        """

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
