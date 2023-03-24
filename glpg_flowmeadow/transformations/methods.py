#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : several methods to handle vector transformations
@File      : transformations.py
@Time      : 09.09.21 23:26
@Author    : flowmeadow
"""
import ctypes
from typing import Tuple

import numpy as np
from pyglet.gl import *


def rot_mat(axis: np.ndarray, angle: float) -> np.ndarray:
    """
    build rotation matrix from axis and angle
    :param axis: axis to rotate around [3,]
    :param angle: angle of rotation in degrees
    :return: rotated vector
    """
    angle = np.pi * angle / 180.0
    l, m, n = axis / np.linalg.norm(axis)  # normalize axis vector
    s, c = np.sin(angle), np.cos(angle)
    # build rotation matrix
    rot_transform = np.array(
        [
            [l * l * (1 - c) + c, m * l * (1 - c) - n * s, n * l * (1 - c) + m * s],
            [l * m * (1 - c) + n * s, m * m * (1 - c) + c, n * m * (1 - c) - l * s],
            [l * n * (1 - c) - m * s, m * n * (1 - c) + l * s, n * n * (1 - c) + c],
        ]
    )
    return rot_transform


def rotate_vec(vec: np.ndarray, axis: np.ndarray, angle: float) -> np.ndarray:
    """
    Rotate a vector or an array of vectors along an axis given an angle
    :param vec: vector [3,] or array of vectors [n, 3] to rotate
    :param axis: axis to rotate around [3,]
    :param angle: angle of rotation in degrees
    :return: rotated vector
    """
    rot_transform = rot_mat(axis, angle)
    if vec.ndim == 1:
        result = rot_transform @ vec
    else:
        result = (rot_transform @ vec.T).T
    return result


def rotation_matrix_from_vectors(vec1: np.ndarray, vec2: np.ndarray):
    """
    Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    k_mat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + k_mat + k_mat.dot(k_mat) * ((1 - c) / (s ** 2))
    return rotation_matrix


def euler_angles_from_rotation_matrix(R: np.ndarray) -> np.ndarray:
    """
    compute Euler angles, given a rotation matrix
    :param R: rotation matrix [3, 3]
    :return: Euler angles [3,]
    """
    sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], sy)
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])
        y = np.arctan2(-R[2, 0], sy)
        z = 0
    angles = np.array([x, y, z])
    angles *= 180. / np.pi
    return angles


def compute_normals(indices: np.ndarray, vertices: np.ndarray) -> np.ndarray:
    """
    Given a vertex and index array, the normals for each vertex are computed.
    First the face normals will be calculated. For each vertex the normal results from
    the face normals of its surrounding faces.
    :param indices: indices array [m, 3]
    :param vertices: vertex array [n, 3]
    :return: normal array [n, 3]
    """
    # compute triangle normals by building the cross product of two edges
    triangle_vertices = vertices[indices]
    edge_1 = triangle_vertices[:, 0, :] - triangle_vertices[:, 1, :]
    edge_2 = triangle_vertices[:, 0, :] - triangle_vertices[:, 2, :]
    cross_products = np.cross(edge_1, edge_2)
    # normalize the normal vectors
    triangle_normals = cross_products / np.linalg.norm(cross_products, axis=1)[:, np.newaxis]

    # compute vertex normals
    # TODO: There has to be a more efficient way ...
    vertex_normals = np.zeros(vertices.shape)
    # add up all the surrounding face normals for each vertex
    for idx in range(len(indices)):
        n = triangle_normals[idx]
        f = indices[idx, :]
        vertex_normals[f] += n
    # normalize the normal vectors
    vertex_normals = vertex_normals / np.linalg.norm(vertex_normals, axis=1)[:, np.newaxis]
    return vertex_normals


def flip_inside_out(indices: np.array) -> np.array:
    """
    To shade the inside of the model, the logical order of face vertices has
    to be changed from counterclockwise to clockwise.
    :param indices: indices array [m, 3]
    :return: indices array [m, 3]
    """
    new_indices = indices.copy()
    new_indices[:, 1], new_indices[:, 2] = indices[:, 2], indices[:, 1]
    return new_indices


def get_P(matrix=GL_PROJECTION_MATRIX) -> np.ndarray:
    """
    :return: camera projection matrix as numpy array (4, 4)
    """
    # get projection matrix
    P = np.zeros(16)
    P = (ctypes.c_float * len(P))(*P)
    glGetFloatv(matrix, P)
    P = np.array(P).reshape((4, 4)).T
    return P


def get_M() -> np.ndarray:
    """
    :return: modelview matrix as numpy array (4, 4)
    """
    # get projection matrix
    M = np.zeros(16)
    M = (ctypes.c_float * len(M))(*M)
    glGetFloatv(GL_MODELVIEW_MATRIX, M)
    M = np.array(M).reshape((4, 4)).T
    return M


def get_K(P: np.ndarray, screen_size: Tuple[int, int]) -> np.ndarray:
    """

    :param P: camera projection matrix as numpy array (4, 4)
    :param screen_size: image screen dimension (width, height)
    :return: camera matrix K in OpenCV convention as numpy array (3, 3)
    """
    # compute K from projection matrix
    w, h = screen_size
    K = np.array(
        [
            [P[0, 0] * w / 2.0, 0.0, w * (1.0 - P[0, 2]) / 2.0],
            [0.0, P[1, 1] * h / 2.0, h * (1.0 - P[1, 2]) / 2.0],
            [0.0, 0.0, 1.0],
        ]
    )
    return K


def construct_T(rot_mat: np.ndarray, trans_vec: np.ndarray) -> np.ndarray:
    """
    Combines rotation matrix and translation vector to transformation matrix
    :param rot_mat: array (3, 3)
    :param trans_vec: array (3,)
    :return: array (4, 4)
    """
    T = np.eye(4)
    T[:3, :3] = rot_mat
    T[:3, -1] = trans_vec
    return T
