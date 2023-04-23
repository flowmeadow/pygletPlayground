#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Simple key handler class
@File      : keyboard.py
@Project   : pygletPlayground
@Time      : 01.04.23 00:06
@Author    : flowmeadow
"""
from typing import Callable

from glpg.display.base import Base


class KeyManager:
    """
    Simple key handler class
    """

    def __init__(self, window: Base):
        """
        :param window: current application window
        """
        self.keys = window.keys
        self.pressed = []
        self.functions = {}

    def assign(self, key: int, function: Callable):
        """
        Assigns a method execution with a key press event
        :param key: key reference (see pyglet.window.key)
        :param function: method to execute on keypress
        """
        self.functions[key] = function

    def update(self):
        """
        checks pressed keys and executes assigned methods
        :return:
        """
        released = list(set(self.pressed) - set(self.keys))  # check which keys have been released

        # execute each function assigned to a released key
        for key in released:
            if key in self.functions.keys():
                self.functions[key]()

        # update currently pressed keys
        self.pressed = self.keys.copy()
