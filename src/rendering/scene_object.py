from src.rendering.model import Model
from pyrr import *


class SceneObject:
    def __init__(self):
        self.model = None
        self.rotation = Vector3([0.0, 0.0, 0.0])
        self.position = Vector3([0.0, 0.0, 0.0])
        self.scale = Vector3([1.0, 1.0, 1.0])

    def draw(self):
        if self.model is not None:
            self.model.translate(self.position[0], self.position[1], self.position[2])
            self.model.rotate(self.rotation[0], self.rotation[1], self.rotation[2])
            self.model.scale(self.scale[0], self.scale[1], self.scale[2])
            self.model.draw()

    def set_position(self, x, y, z):
        self.position = Vector3([x, y, z])

    def set_rotation(self, rx, ry, rz):
        self.rotation = Vector3([rx, ry, rz])

    def set_scale(self, x, y, z):
        self.scale = Vector3([x, y, z])

    def load_model(self, file_path):
        self.model = Model(file_path)

