#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Demo script; Simple use case for an embedded GL scene within a PySide6 (Qt) application
@File      : test.py
@Project   : pygletPlayground
@Time      : 12.04.24 22:47
@Author    : flowmeadow
"""
import sys

import numpy as np
from PySide6 import QtWidgets, QtCore

from glpg.display.gl_widget import GLWidget

from glpg.camera.camera import Camera
from glpg.rendering.lighting.lights import Lights
from glpg.rendering.methods import draw_text_2D, draw_coordinates
from glpg.rendering.models.model import Model
from glpg.rendering.models.model_generation.geometry import icosphere


class HelloWorldWidget(GLWidget):
    """
    Simple use case for an embedded GL scene within a PySide6 (Qt) application
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # placeholder
        self.cam: Camera = None
        self.lights: Lights = None
        self.earth: Model = None

        # variables
        self.frame_count = 0
        self.rotation = 0

    def init_gl(self):
        # define camera
        self.cam = Camera(camera_pos=(2.0, 2.0, 2.0), camera_view=(-1.0, -1.0, -1.0))

        # define light sources
        self.lights = Lights()
        self.lights.add(  # circling around
            position=(1.0, 1.0, 0.0),
            color=(1.0, 1.0, 0.95),
        )

        # define sphere model
        radius = 0.1
        vertices, indices = icosphere(radius=radius, refinement_steps=5)

        # create earth sphere
        self.earth = Model(
            vertices,
            indices,
            textures="demo_textures/8081_earthmap4k.iba",
            shader="demo_shaders/earth",
            num_lights=self.lights.num_lights,
            scale=5.0,
        )

    def handle_events(self) -> None:
        """
        handle pygame events and do other stuff before drawing
        :return: None
        """
        # update camera position for all objects that use it in their shader
        self.earth.update_camera(self.cam.camera_pos, self.cam.camera_view)

    def draw_world(self) -> None:
        """
        draw objects in the world
        :return: None
        """
        # move sun
        light_speed = 0.002
        new_pos = 10.0 * np.array([np.sin(self.frame_count * light_speed), np.cos(self.frame_count * light_speed), 0.0])
        self.lights[0].update("position", new_pos)

        # transform earth
        self.earth.rotate(self.rotation, 0.0, 0.0, -1.0)
        self.earth.draw()

        draw_coordinates()

        # update frame counter
        self.frame_count += 1

    def draw_screen(self) -> None:
        """
        draw objects onto the screen
        :return: None
        """
        draw_text_2D(10, self.height - 10, f"FPS: {self.current_fps:.2f}")


class MainWidget(QtWidgets.QWidget):
    """
    Main window of the application
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pyglet and QT Example")
        self.shapes = []
        self.setMinimumSize(640, 480)

        # create OpenGL widget
        opengl_widget = HelloWorldWidget()

        # create controls widget
        controls_layout = QtWidgets.QVBoxLayout()

        label_zoom = QtWidgets.QLabel("Zoom")
        slider_zoom = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        slider_zoom.setValue(50)

        def _zoom_callback():
            zoom_factor = 3.0 * slider_zoom.value() / 100
            opengl_widget.cam.camera_pos = 0.5 + zoom_factor * np.array([1.0, 1.0, 1.0])

        slider_zoom.valueChanged.connect(_zoom_callback)

        label_rotate = QtWidgets.QLabel("Rotate")
        slider_rotate = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        slider_rotate.setValue(0)

        def _rotate_callback():
            angle = 360 * slider_rotate.value() / 100
            opengl_widget.rotation = angle

        slider_rotate.valueChanged.connect(_rotate_callback)

        button = QtWidgets.QPushButton("Reset")

        def _reset_callback():
            slider_zoom.setValue(50)
            slider_rotate.setValue(0)

        button.clicked.connect(_reset_callback)

        spacer = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        controls_layout.addWidget(label_zoom)
        controls_layout.addWidget(slider_zoom)
        controls_layout.addWidget(label_rotate)
        controls_layout.addWidget(slider_rotate)
        controls_layout.addItem(spacer)
        controls_layout.addWidget(button)

        controls_widget = QtWidgets.QWidget(parent=self)
        controls_widget.setLayout(controls_layout)
        controls_widget.setFixedWidth(300)

        # pack both widgets horizontally
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(opengl_widget)
        layout.addWidget(controls_widget)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWidget()
    ui.show()  # Calls initializeGL. Do not do any GL stuff before this is called.
    app.exec()  # exec_ in 5.
