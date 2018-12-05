from OpenGL.GL import *
import numpy


class Model:
    def __init__(self):
        # Triangle    vertices           colors
        triangle = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                    0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                    0.0, 0.5, 0.0, 0.0, 0.0, 1.0]

        triangle = numpy.array(triangle, dtype=numpy.float32)

        self.vao = glGenVertexArrays(1)
        self.bind()

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, len(triangle) * 4, triangle, GL_STATIC_DRAW)

        # Positions input to shader. (Offset here is 0 bytes for the pointer offset in ctypes)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Colors input to shader (Offset here is 12 bytes for the pointer offset in ctypes)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        self.unbind()

    def bind(self):
        glBindVertexArray(self.vao)

    def unbind(self):
        glBindVertexArray(0)

    def draw(self):
        self.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        self.unbind()
