import struct, os
from OpenGL.GL import *


def load_texture_raw(rel_path):
    base = os.path.dirname(__file__)
    path = os.path.join(base, rel_path)

    with open(path, "rb") as f:
        header = f.read(54)
        offset = struct.unpack("<I", header[10:14])[0]
        w = struct.unpack("<I", header[18:22])[0]
        h = struct.unpack("<I", header[22:26])[0]

        f.seek(offset)
        data = f.read(w * h * 3)

    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB,
        w, h, 0, GL_BGR,
        GL_UNSIGNED_BYTE, data
    )

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return tex