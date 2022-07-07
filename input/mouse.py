#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : TODO
@File      : mouse.py
@Project   : pygletPlayground
@Time      : 13.10.21 19:45
@Author    : flowmeadow
"""
import attr
from typing import Tuple

@attr.s
class Mouse:
    """
    Description: TODO
    """
    x: int = attr.ib(default=0)
    y: int = attr.ib(default=0)
    dx: int = attr.ib(default=0)
    dy: int = attr.ib(default=0)

    def update(self, x: int, y: int, dx: int, dy: int):
        self.x = x
        self.y = y + 2
        self.dx += dx
        self.dy += dy

    def reset(self):
        self.dx = 0
        self.dy = 0
