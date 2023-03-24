#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Generation methods for vertices and indices of basic geometries
@File      : geometry.py
@Time      : 10.09.21 10:50
@Author    : flowmeadow
"""
from typing import Tuple

import numpy as np
import warnings


def cube(
    size: float = 1.0,
    refinement_steps: int = 0,
    experimental_mode: bool = False,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates vertices and indices of a cube
    :param size: edge length of the cube
    :param refinement_steps: number of triangle refinements
    :param experimental_mode: if True, the number of refinement steps is infinite
    :return: vertices [n, 3], indices [m, 3]
    """
    refinement_steps = max(0, refinement_steps)
    max_step = 9
    if refinement_steps > max_step and not experimental_mode:
        refinement_steps = max_step
        warnings.warn(
            f"\nRefinement step of more than {max_step} is not recommended as the computation increases exponentially."
            f"\nIf you want to compute with higher refinement steps, set the 'experimental_mode' flag."
        )

    vertices = [
        # corners
        [-1.0, -1.0, -1.0],
        [-1.0, -1.0, +1.0],
        [-1.0, +1.0, -1.0],
        [-1.0, +1.0, +1.0],
        [+1.0, -1.0, -1.0],
        [+1.0, -1.0, +1.0],
        [+1.0, +1.0, -1.0],
        [+1.0, +1.0, +1.0],
        # face centers
        [+0.0, +0.0, -1.0],
        [+0.0, +0.0, +1.0],
        [+0.0, -1.0, +0.0],
        [+0.0, +1.0, +0.0],
        [-1.0, +0.0, +0.0],
        [+1.0, +0.0, +0.0],
    ]
    indices = [
        # face 1
        [8, 0, 2],
        [8, 2, 6],
        [8, 6, 4],
        [8, 4, 0],
        # face 2
        [9, 3, 1],
        [9, 7, 3],
        [9, 5, 7],
        [9, 1, 5],
        [10, 1, 0],
        [10, 5, 1],
        [10, 4, 5],
        [10, 0, 4],
        [11, 2, 3],
        [11, 6, 2],
        [11, 7, 6],
        [11, 3, 7],
        [12, 0, 1],
        [12, 2, 0],
        [12, 3, 2],
        [12, 1, 3],
        [13, 5, 4],
        [13, 7, 5],
        [13, 6, 7],
        [13, 4, 6],
    ]
    vertices_per_face = 3
    for step in range(refinement_steps):
        new_vertices, new_indices = vertices, []
        vertices = np.array(vertices)
        for triangle in indices:
            edges = []
            for i in range(vertices_per_face):
                edges.append(vertices[triangle[(i + 1) % vertices_per_face]] - vertices[triangle[i]])
            edges = np.array(edges)
            largest_edge = np.argmax(np.linalg.norm(edges, axis=1))
            new_vertex = vertices[triangle[largest_edge]] + edges[largest_edge] * 0.5

            if new_vertex.tolist() not in new_vertices:
                vertex_idx = len(new_vertices)
                new_vertices.append(new_vertex.tolist())
            else:
                vertex_idx = new_vertices.index(new_vertex.tolist())

            triangle_1 = [triangle[0], triangle[1], triangle[2]]
            triangle_2 = [triangle[0], triangle[1], triangle[2]]

            triangle_1[largest_edge] = vertex_idx
            triangle_2[(largest_edge + 1) % vertices_per_face] = vertex_idx

            new_indices.append(triangle_1)
            new_indices.append(triangle_2)

        vertices, indices = new_vertices, new_indices

    return np.array(vertices) * size, np.array(indices)


def sphere(
    radius: float = 0.1,
    refinement_steps: int = 0,
    experimental_mode: bool = False,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates vertices and indices of a sphere
    :param radius: radius of the sphere
    :param refinement_steps: number of triangle refinements
    :param experimental_mode: if True, the number of refinement steps is infinite
    :return: vertices [n, 3], indices [m, 3]
    """
    warnings.warn("\n'sphere' method is inefficient for sphere mesh generation. Use 'icosphere' instead.")
    refinement_steps = max(0, refinement_steps)
    max_step = 4
    if refinement_steps > max_step and not experimental_mode:
        refinement_steps = max_step
        warnings.warn(
            f"\nRefinement step of more than {max_step} is not recommended as the computation increases exponentially."
            f"\nIf you want to compute with higher refinement steps, set the 'experimental_mode' flag."
        )
    vertices = np.array(
        [
            [0.0, 0.0, -radius],
            [0.0, radius, 0.0],
            [radius, 0.0, 0.0],
            [0.0, -radius, 0.0],
            [-radius, 0.0, 0.0],
            [0.0, 0.0, radius],
        ]
    )
    indices = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 4],
            [0, 4, 1],
            [5, 4, 3],
            [5, 3, 2],
            [5, 2, 1],
            [5, 1, 4],
        ]
    )

    # refinement
    for r_idx in range(refinement_steps):
        new_indices, edges = [], []
        for triangle in indices:
            vert_index = len(vertices)
            new_vert = np.mean(vertices[triangle], axis=0)
            new_vert = (new_vert / np.linalg.norm(new_vert)) * radius
            vertices = np.append(vertices, [new_vert], axis=0)
            new_indices.append([vert_index, triangle[0], triangle[1]])
            new_indices.append([vert_index, triangle[1], triangle[2]])
            new_indices.append([vert_index, triangle[2], triangle[0]])
        indices = np.array(new_indices)
        # edge flipping
        for idx in range(len(indices)):
            triangle = indices[idx]
            c_triangle, c_idx = 0, 0
            for c_idx in range(len(indices)):
                c_triangle = indices[c_idx]
                if triangle[1] in c_triangle and triangle[2] in c_triangle and triangle[0] not in c_triangle:
                    break
            c_vert = c_triangle[np.where((c_triangle != triangle[1]) & (c_triangle != triangle[2]))[0]]

            edge_1 = [triangle[1], triangle[2]]
            edge_2 = [triangle[0], c_vert[0]]

            dist_1 = np.linalg.norm(vertices[edge_1[0]] - vertices[edge_1[1]])
            dist_2 = np.linalg.norm(vertices[edge_2[0]] - vertices[edge_2[1]])

            if dist_1 > dist_2:
                # perform edge flip
                indices[idx] = [edge_1[0], edge_2[1], edge_2[0]]
                indices[c_idx] = [edge_1[1], edge_2[0], edge_2[1]]
    return vertices, indices


def icosphere(
    radius: float = 0.1,
    refinement_steps: int = 0,
    experimental_mode: bool = False,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates vertices and indices of an icosphere
    :param radius: radius of the icosphere
    :param refinement_steps: number of triangle refinements
    :param experimental_mode: if True, the number of refinement steps is infinite
    :return: vertices [n, 3], indices [m, 3]
    """
    refinement_steps = max(0, refinement_steps)
    max_step = 6
    if refinement_steps > max_step and not experimental_mode:
        refinement_steps = max_step
        warnings.warn(
            f"\nRefinement step of more than {max_step} is not recommended as the computation increases exponentially."
            f"\nIf you want to compute with higher refinement steps, set the 'experimental_mode' flag. "
        )

    vertices = np.array(
        [
            [0.0, 0.0, -1.0],
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 4],
            [0, 4, 1],
            [5, 4, 3],
            [5, 3, 2],
            [5, 2, 1],
            [5, 1, 4],
        ]
    )
    # refinement
    for r_idx in range(refinement_steps):
        # update each face
        edges = {}
        new_faces = np.zeros((faces.shape[0] * 4, 3)).astype(np.uint)
        for f_idx, face in enumerate(faces):
            # define face edges
            e_1 = [face[0], face[1]]
            e_2 = [face[1], face[2]]
            e_3 = [face[2], face[0]]

            # TODO: more efficient
            new_v_idcs = np.zeros((3,))
            for e_idx, edge in enumerate([e_1, e_2, e_3]):
                sorted_edge = tuple(np.sort(edge))
                if sorted_edge not in edges.keys():
                    # create new vertex
                    new_vert = np.array([np.mean(vertices[edge], axis=0)])
                    # append new vertex and store vertex id
                    v_idx = vertices.shape[0]
                    vertices = np.concatenate([vertices, new_vert])
                    # mark current edge as processed and store the vertex id
                    edges[sorted_edge] = v_idx
                else:
                    v_idx = edges[sorted_edge]
                # store vertex index of current edge
                new_v_idcs[e_idx] = v_idx

            # create new faces
            new_faces[f_idx * 4 + 0] = np.array([face[0], new_v_idcs[0], new_v_idcs[2]])
            new_faces[f_idx * 4 + 1] = np.array([face[1], new_v_idcs[1], new_v_idcs[0]])
            new_faces[f_idx * 4 + 2] = np.array([face[2], new_v_idcs[2], new_v_idcs[1]])
            new_faces[f_idx * 4 + 3] = np.array([new_v_idcs[0], new_v_idcs[1], new_v_idcs[2]])

        faces = new_faces

    # move all vertices to the sphere surface
    lengths = np.linalg.norm(vertices, axis=1)
    for idx in range(3):
        vertices[:, idx] /= lengths

    # apply radius
    vertices = vertices * radius
    return vertices, faces


def cylinder(
    radius: float = 0.1,
    height: float = 0.2,
    angle_steps: int = 32,
    height_steps: int = 8,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates vertices and indices of a cylinder

    :param radius: cylinder radius
    :param height: cylinder height
    :param angle_steps: angular resolution
    :param height_steps: vertical resolution
    :return: vertices [n, 3], indices [m, 3]
    """
    angles = np.linspace(0, 2 * np.pi, angle_steps, endpoint=False)  # get values of all angles

    vertices, indices = [], []
    # create the vertices
    for h in np.linspace(0, height, height_steps):
        vertices.append([0, 0, h])
        for a in angles:
            vertices.append([np.sin(a) * radius, np.cos(a) * radius, h])

    # create the indices
    for i in range(1, angle_steps + 1):
        # top and bottom triangles
        indices.append([0, i, i % angle_steps + 1])
        offset = (angle_steps + 1) * (height_steps - 1)
        indices.append([offset, offset + i, offset + i % angle_steps + 1])
        # side triangles
        for h in range(height_steps - 1):
            offset_1 = (angle_steps + 1) * h
            offset_2 = (angle_steps + 1) * (h + 1)
            indices.append([offset_1 + i, offset_2 + i % angle_steps + 1, offset_1 + i % angle_steps + 1])
            indices.append([offset_1 + i, offset_2 + i, offset_2 + i % angle_steps + 1])
    return np.array(vertices), np.array(indices)
