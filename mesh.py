import numpy as np
from OpenGL.GL import *
import ctypes
import math

class Mesh:
    def __init__(self, vertices, indices):
        self.count = len(indices)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        stride = 8 * 4

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)


def create_pyramid():
    vertices = np.array([
        # base
        -1, 0, -1,  0,-1,0,  0,0,
         1, 0, -1,  0,-1,0,  1,0,
         1, 0,  1,  0,-1,0,  1,1,
        -1, 0,  1,  0,-1,0,  0,1,
        # tip
         0, 1.5, 0,  0,1,0,  0.5,0.5,
    ], dtype=np.float32)

    indices = np.array([
        0,1,2, 0,2,3,     # base
        0,1,4,
        1,2,4,
        2,3,4,
        3,0,4
    ], dtype=np.uint32)

    return Mesh(vertices, indices)


def create_cube():
    # unchanged cube used elsewhere
    vertices = np.array([
        -1,-1,-1, 0,0,-1, 0,0,  1,-1,-1,0,0,-1,1,0,
         1, 1,-1,0,0,-1,1,1, -1, 1,-1,0,0,-1,0,1,
        -1,-1, 1,0,0, 1,0,0,  1,-1, 1,0,0,1,1,0,
         1, 1, 1,0,0,1,1,1, -1, 1, 1,0,0,1,0,1
    ], dtype=np.float32)

    indices = np.array([
        0,1,2, 0,2,3, 4,5,6, 4,6,7,
        0,4,7, 0,7,3, 1,5,6, 1,6,2,
        3,2,6, 3,6,7, 0,1,5, 0,5,4
    ], dtype=np.uint32)

    return Mesh(vertices, indices)


def create_sphere(segments=32, rings=32):
    verts = []
    inds = []

    for y in range(rings+1):
        for x in range(segments+1):
            xSeg = x / segments
            ySeg = y / rings
            xPos = math.cos(xSeg*2*math.pi)*math.sin(ySeg*math.pi)
            yPos = math.cos(ySeg*math.pi)
            zPos = math.sin(xSeg*2*math.pi)*math.sin(ySeg*math.pi)
            verts += [xPos,yPos,zPos, xPos,yPos,zPos, xSeg,ySeg]

    for y in range(rings):
        for x in range(segments):
            i = y*(segments+1)+x
            inds += [i,i+segments+1,i+1, i+1,i+segments+1,i+segments+2]

    return Mesh(np.array(verts,np.float32), np.array(inds,np.uint32))
