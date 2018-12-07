from pyrr import Vector3, Matrix44, vector, vector3
from math import sin, cos, radians


# Code is attributed to totex/PyOpenGL_season_02
# -Attila Toth from GitHub.
class Camera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 0.0, 5.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.25
        self.yaw = -90.0
        self.pitch = 0.0
        self.update()

    def get_view_matrix(self):
        return self.look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def translate(self, direction, distance):
        self.camera_pos += direction * distance


    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 45.0:
                self.pitch = 45.0
            if self.pitch < -45.0:
                self.pitch = -45.0

        self.update()

    def update(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    def look_at(self, position, target, world_up):
        # 1.Position = known
        # 2.Calculate cameraDirection
        z_axis = vector.normalise(position - target)
        # 3.Get positive right axis vector
        x_axis = vector.normalise(vector3.cross(vector.normalise(world_up), z_axis))
        # 4.Calculate the camera up vector
        y_axis = vector3.cross(z_axis, x_axis)

        # create translation and rotation matrix
        translation = Matrix44.identity()
        translation[3][0] = -position.x
        translation[3][1] = -position.y
        translation[3][2] = -position.z

        rotation = Matrix44.identity()
        rotation[0][0] = x_axis[0]
        rotation[1][0] = x_axis[1]
        rotation[2][0] = x_axis[2]
        rotation[0][1] = y_axis[0]
        rotation[1][1] = y_axis[1]
        rotation[2][1] = y_axis[2]
        rotation[0][2] = z_axis[0]
        rotation[1][2] = z_axis[1]
        rotation[2][2] = z_axis[2]

        self.update()

        return translation * rotation
