#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : TODO
@File      : base.py
@Project   : pygletPlayground
@Time      : 02.10.21 12:26
@Author    : flowmeadow
"""
from abc import abstractmethod

import pyglet
from input.mouse import Mouse
from pyglet.window import key


class Base(pyglet.window.Window):
    parent_kwargs = dict(
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

    child_kwargs = dict(
        max_fps=120,
    )

    def __init__(self, **kwargs):
        # update kwargs
        for key, val in kwargs.items():
            if key in self.parent_kwargs.keys():
                self.parent_kwargs[key] = val
            elif key in self.child_kwargs.keys():
                self.child_kwargs[key] = val
            else:
                raise KeyError(f"Invalid keyword argument {key}")

        # initialize parent class object (pyglet.window.Window)
        super().__init__(**self.parent_kwargs)

        # set attributes
        self._max_fps = self.child_kwargs["max_fps"]
        self._elapsed_time = 0.0
        self.update_time = 0.1
        self.current_fps = 0.0
        self.display_center = (self.width // 2, self.height // 2)

        # initialize inputs
        self.mouse = Mouse()
        self.keys = set()

        # initialize
        self.init_gl()

        pyglet.clock.schedule_interval(self.on_draw, 1 / self._max_fps)

    def on_draw(self, *args):
        """
        TODO
        Override from parent
        :return:
        """
        self.current_fps = pyglet.clock.get_fps()
        self.clear()
        self.draw_frame()

    @staticmethod
    def run():
        pyglet.app.run()

    @abstractmethod
    def init_gl(self) -> None:
        """
        TODO
        :return: None
        """

    @abstractmethod
    def draw_frame(self) -> None:
        """
        TODO
        :return: None
        """

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.update(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        if symbol in [key.Q, key.ESCAPE]:
            self.close()
        self.keys.add(symbol)

    def on_key_release(self, symbol, modifiers):
        self.keys.discard(symbol)

    def size(self):
        return self.width, self.height
