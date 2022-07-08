#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : TODO WIP
@File      : geometry.py
@Time      : 10.09.21 10:50
@Author    : flowmeadow
"""
from typing import Tuple

import numpy as np


def cube(size=1, refinement_steps=0):
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
        print(f"Refinement step: ({step + 1}|{refinement_steps})")
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


def sphere(radius=0.1, refinement_steps=3):
    vertices = np.array([
        [0., 0., -radius],
        [0., radius, 0.],
        [radius, 0., 0.],
        [0., -radius, 0.],
        [-radius, 0., 0.],
        [0., 0., radius],
    ])
    indices = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 4],
        [0, 4, 1],
        [5, 4, 3],
        [5, 3, 2],
        [5, 2, 1],
        [5, 1, 4],
    ])

    # refinement
    for _ in range(refinement_steps):
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


def cylinder(radius: float = 0.1, height: float = 0.2, angle_steps: int = 32, height_steps: int = 8):
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
