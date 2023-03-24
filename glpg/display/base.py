#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Base window class that handles setup, catches frame rates and user inputs
@File      : base.py
@Project   : pygletPlayground
@Time      : 02.10.21 12:26
@Author    : flowmeadow
"""
from abc import abstractmethod
from typing import Tuple

import pyglet
from glpg.input.mouse import Mouse
from pyglet.window import key


class Base(pyglet.window.Window):
    """
    Base window class that handles setup, catches frame rates and user inputs
    """

    # default settings for pyglet.window.Window
    _parent_kwargs = dict(
        width=None,
        height=None,
        caption=None,
        resizable=False,
        style=None,
        fullscreen=False,
        visible=True,
        vsync=True,
        file_drops=False,
        display=None,
        screen=None,
        config=None,
        context=None,
        mode=None,
    )

    # default settings for custom window
    _child_kwargs = dict(
        max_fps=120,
    )

    def __init__(self, **kwargs):
        """
        :param kwargs: keyword arguments (see class header for available keywords)
        """
        # update kwargs
        for key, val in kwargs.items():
            if key in self._parent_kwargs.keys():
                self._parent_kwargs[key] = val
            elif key in self._child_kwargs.keys():
                self._child_kwargs[key] = val
            else:
                raise KeyError(f"Invalid keyword argument {key}")

        # initialize parent class object (pyglet.window.Window)
        super().__init__(**self._parent_kwargs)

        # set attributes
        self._max_fps = self._child_kwargs["max_fps"]
        self.current_fps = 0.0
        self.display_center = (self.width // 2, self.height // 2)

        # initialize inputs
        self.mouse = Mouse()
        self.keys = set()

        # initialize
        self.init_gl()

        # set interval for drawing function
        pyglet.clock.schedule_interval(self.my_draw, 1 / self._max_fps)

    def my_draw(self, dt: float):
        """
        Update FPS, clear screen and draw next frame
        :param dt: elapsed time since last frame
        """
        self.current_fps = pyglet.clock.get_fps()
        self.clear()
        self.draw_frame()

    def on_draw(self, *test):
        """
        Override from parent as it is also called when a user input was done. Instead, on_draw_const() is used.
        """
        pass

    @staticmethod
    def run():
        """
        Run application
        """
        pyglet.app.run()

    @abstractmethod
    def init_gl(self) -> None:
        """
        To be overwritten in child class. Initialize OpenGL settings.
        """

    @abstractmethod
    def draw_frame(self) -> None:
        """
        To be overwritten in child class. Draw objects.
        """

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """
        Update mouse object
        :param x: x-position
        :param y: y-position
        :param dx: change in x-direction
        :param dy: change in y-direction
        """
        self.mouse.update(x, y, dx, dy)

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Update pressed keyboard inputs
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

    def close(self):
        """
        Stop clock and close window
        """
        pyglet.clock.unschedule(self.my_draw)
        super().close()
