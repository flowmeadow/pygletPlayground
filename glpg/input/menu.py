#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Screen object with keyboard interface to manipulate specified settings
@File      : menu.py
@Project   : pygletPlayground
@Time      : 31.03.23 23:13
@Author    : flowmeadow
"""
from dataclasses import dataclass
from typing import List

import numpy as np

from glpg.display.base import Base
from glpg.input.keyboard import KeyManager
from glpg.rendering.methods import draw_rectangle, draw_text_2D
from pyglet.window import key as gl_key


@dataclass
class MenuEntry:
    """
    Data class that manages menu entries
    """

    key_name: str  # code internal name of the entry
    display_name: str  # name of the entry for display
    options: list  # list of possible code internal options
    display_options: list  # list of option names for display
    pointer: int = 0  # pointer selection of the current option
    info_txt: str = ""  # description of the entry

    def current_option(self):
        """
        Returns the currently selected entry value
        """
        return self.display_options[self.pointer]


class Menu:
    """
    Screen object with keyboard interface to manipulate specified settings
    """

    # First lines to display
    welcome_msg = [
        "OPERATION                   KEYS",
        "Select a menu entry:        \u2191,\u2193",
        "Change the entry's value:   \u2192,\u2190",
        "Open and close the menu:    M",
    ]

    pointer = 0  # current entry selection
    text_offset = 30  # pixel offset in x direction from left menu border
    is_visible = True  # allow drawing only if this is True

    # place holders
    max_title_length = None
    max_value_length = None
    menu_txt = None
    initialized = False

    def __init__(self, window: Base, x: int, y: int, w: int, h: int):
        """
        :param window: window object the menu is placed in
        :param x: x position of the menu
        :param y: y position of the menu
        :param w: width of the menu
        :param h: height of the menu
        """
        self.menu_entries = []
        self.menu_size = np.array([w, h])
        self.menu_pos = np.array([x, y])
        self.win_size = np.array(window.size)

        # create a key manager object and assign methods for keys
        self.key_manager = KeyManager(window)
        self.key_manager.assign(gl_key.M, self.press_M)
        self.key_manager.assign(gl_key.UP, self.press_UP)
        self.key_manager.assign(gl_key.DOWN, self.press_DOWN)
        self.key_manager.assign(gl_key.LEFT, self.press_LEFT)
        self.key_manager.assign(gl_key.RIGHT, self.press_RIGHT)

    def add_entry(
        self,
        key_name: str,
        options: list,
        display_name: str = None,
        display_options: List[str] = None,
        info_txt: str = None,
        index: int = 0,
    ):
        """
        Creates a new menu entry
        (See MenuEntry for attribute descriptions)
        """
        display_name = display_name if display_name else key_name
        display_options = display_options if display_options else [str(o) for o in options]
        self.menu_entries.append(MenuEntry(key_name, display_name, options, display_options, index, info_txt))

    def update(self):
        """
        Updates the key manager
        """
        self.key_manager.update()

    def initialize(self):
        """
        Is performed on first draw
        """
        self.max_title_length = max([len(e.display_name) for e in self.menu_entries]) + 2
        self.max_value_length = max([max([len(str(o)) for o in e.display_options]) for e in self.menu_entries]) + 2
        self.initialized = True

    def build_title(self, title: str) -> str:
        """
        Builds a title string
        :param title: name of the title
        :return: string where the title is embedded for menu display
        """
        if not self.max_title_length or not self.max_value_length:
            self.initialize()
        row_length = self.max_title_length + self.max_value_length + 2
        start_idx = row_length // 2 - len(title) // 2
        title_txt = f"{'-' * start_idx} {title} {'-' * start_idx}"
        return title_txt[:row_length]

    def draw(self):
        """
        Draws the menu with current settings
        """

        # initialize on first draw
        if not self.initialized:
            self.initialize()

        # draw only if menu is visible
        if not self.is_visible:
            return

        # draw menu frame
        x, y = self.menu_pos
        draw_rectangle(x - 1, y - 1, *(self.menu_size + 2), color=(1.0, 1.0, 1.0, 0.7))
        draw_rectangle(x, y, *self.menu_size, color=(0.0, 0.0, 0.0, 0.7))

        # build concatenated menu text for ...
        # ... the welcome section
        menu_txt = [self.build_title("WELCOME")] + self.welcome_msg.copy()

        # ... the menu section
        menu_txt.append(self.build_title("MENU"))
        for idx, entry in enumerate(self.menu_entries):
            menu_dot = "\u2022" if idx != self.pointer else "\u25BA"
            entry_title = entry.display_name.ljust(self.max_title_length)
            entry_value = entry.current_option().ljust(self.max_value_length)
            menu_txt.append(f"{menu_dot} {entry_title}{entry_value}")

        # ... the info section
        info_txt = self.menu_entries[self.pointer].info_txt
        if info_txt:
            menu_txt.append("\n" + self.build_title("INFO") + f"\n{info_txt}")
        menu_txt = "".join(f"{s}\n" for s in menu_txt)

        # draw text into menu frame
        draw_text_2D(
            x + self.text_offset,
            y - self.text_offset + self.menu_size[1],
            menu_txt,
            multiline=True,
            width=self.menu_size[0] - self.text_offset * 2,
        )

    def press_M(self):
        """
        Toggle menu visibility
        """
        self.is_visible = not self.is_visible

    def press_UP(self):
        """
        Move entry selector one position up
        """
        if self.is_visible:
            self.pointer = (self.pointer - 1) % len(self.menu_entries)

    def press_DOWN(self):
        """
        Move entry selector one position down
        """
        if self.is_visible:
            self.pointer = (self.pointer + 1) % len(self.menu_entries)

    def press_LEFT(self):
        """
        Move current entry's option selector one position up
        """
        if self.is_visible:
            entry = self.menu_entries[self.pointer]
            self.menu_entries[self.pointer].pointer = (entry.pointer - 1) % len(entry.options)

    def press_RIGHT(self):
        """
        Move current entry's option selector one position down
        """
        if self.is_visible:
            entry = self.menu_entries[self.pointer]
            self.menu_entries[self.pointer].pointer = (entry.pointer + 1) % len(entry.options)

    def get_option(self, key: str):
        """
        Returns the given entry's current option selection
        :param key: name of the entry
        :return: the selected option
        """
        for entry in self.menu_entries:
            if entry.key_name == key:
                return entry.options[entry.pointer]
