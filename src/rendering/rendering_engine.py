from pyrr import *
from src.rendering.camera import Camera


class RenderingEngine:
    view = matrix44.create_from_translation(Vector3([0.0, 0.0, -3.0]))
    projection = matrix44.create_perspective_projection_matrix(75.0, 4/3, 0.1, 100.0)
    camera = Camera()
    canvas = None

