from OpenGL.GL import *
from stl import mesh
import numpy
from src.rendering.material import Material
from src.rendering.rendering_engine import RenderingEngine
from pyrr import *
import time
import random


class Model:
    def __init__(self, file_path):
        self.model_orientation = Quaternion()
        self.model_translation = Vector3([0.0, 0.0, 0.0])
        self.model_scale = Vector3([1.0, 1.0, 1.0])

        # TODO: confirm valid filepath
        self.mesh_data = mesh.Mesh.from_file(file_path)
        triangle_data = []

        for i in range(len(self.mesh_data.normals)):
                triangle_data.append(self.mesh_data.v2[i][0])
                triangle_data.append(self.mesh_data.v2[i][1])
                triangle_data.append(self.mesh_data.v2[i][2])
                triangle_data.append(0.0)
                triangle_data.append(0.0)
                triangle_data.append(random.uniform(0.7, 1.0))
                triangle_data.append(self.mesh_data.v1[i][0])
                triangle_data.append(self.mesh_data.v1[i][1])
                triangle_data.append(self.mesh_data.v1[i][2])
                triangle_data.append(0.0)
                triangle_data.append(0.0)
                triangle_data.append(random.uniform(0.8, 1.0))
                triangle_data.append(self.mesh_data.v0[i][0])
                triangle_data.append(self.mesh_data.v0[i][1])
                triangle_data.append(self.mesh_data.v0[i][2])
                triangle_data.append(0.0)
                triangle_data.append(0.0)
                triangle_data.append(random.uniform(0.8, 1.0))

        self.vao = glGenVertexArrays(1)

        self.bind()
        self.material = Material(numpy.array(triangle_data, dtype=numpy.float32))
        self.unbind()
        self.rotate(0.0, 1.0, 0.0)
        self.translate(0.0, 1.0, 0.0)
        self.scale(1.0, 1.0, 1.0)


    def translate(self, dx, dy, dz):
        self.model_translation = Vector3([dx, dy, dz])

    def rotate(self, rx, ry, rz):
        orientation = Quaternion()
        rotation_x = Quaternion.from_x_rotation(rx)
        rotation_y = Quaternion.from_y_rotation(ry)
        rotation_z = Quaternion.from_z_rotation(rz)

        self.model_orientation = rotation_x * rotation_z * rotation_y * orientation

    def scale(self, dx, dy, dz):
        self.model_scale = Vector3([dx, dy, dz])

    def bind(self):
        glBindVertexArray(self.vao)

    def unbind(self):
        glBindVertexArray(0)

    def draw(self):
        self.bind()

        # Scale
        scale_matrix = Matrix44.from_scale(self.model_scale)
        # Rotate
        rs_matrix = scale_matrix * self.model_orientation
        # Translate
        trs_matrix = rs_matrix * Matrix44.from_translation(self.model_translation)

        #RenderingEngine.camera.process_mouse_movement(50.0, 500.0)

        self.material.set_uniform_matrix4fv("model", trs_matrix)
        self.material.set_uniform_matrix4fv("view", RenderingEngine.camera.get_view_matrix())

        glDrawArrays(GL_TRIANGLES, 0, len(self.mesh_data.normals) * 3)

        self.unbind()

