import glm
import numpy as np
from mesh import Mesh
import math

class Object3D:
    def __init__(self, mesh, texture=None):
        self.mesh = mesh
        self.texture = texture
        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)

    def model_matrix(self):
        m = glm.mat4(1.0)
        m = glm.translate(m, self.position)
        m = glm.rotate(m, self.rotation.x, glm.vec3(1, 0, 0))
        m = glm.rotate(m, self.rotation.y, glm.vec3(0, 1, 0))
        m = glm.rotate(m, self.rotation.z, glm.vec3(0, 0, 1))
        m = glm.scale(m, self.scale)
        return m


def create_sphere(radius=1.0, sectors=36, stacks=18):
    vertices = []
    indices = []

    for i in range(stacks + 1):
        stack_angle = math.pi / 2 - i * math.pi / stacks
        xy = radius * math.cos(stack_angle)
        z = radius * math.sin(stack_angle)

        for j in range(sectors + 1):
            sector_angle = j * 2 * math.pi / sectors

            x = xy * math.cos(sector_angle)
            y = xy * math.sin(sector_angle)

            nx, ny, nz = x / radius, y / radius, z / radius
            s = j / sectors
            t = i / stacks

            vertices.extend([x, y, z, nx, ny, nz, s, t])

    for i in range(stacks):
        k1 = i * (sectors + 1)
        k2 = k1 + sectors + 1

        for j in range(sectors):
            if i != 0:
                indices.extend([k1 + j, k2 + j, k1 + j + 1])
            if i != (stacks - 1):
                indices.extend([k1 + j + 1, k2 + j, k2 + j + 1])

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    return Mesh(vertices, indices)
