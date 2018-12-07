from OpenGL.GL import *
import OpenGL.GL.shaders
from pyrr import *
from src.rendering.rendering_engine import RenderingEngine


vertex_shader = """
# version 330
in layout(location = 0) vec3 positions;
in layout(location = 1) vec3 colors;

out vec3 newColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main(){
    gl_Position = projection * view * model *  vec4(positions, 1.0);
    newColor = colors;
}
"""

fragment_shader = """
# version 330
in vec3 newColor;
out vec4 outColor;

void main(){ 
    outColor = vec4(newColor, 1.0);
}
"""


class Material:
    def __init__(self, triangle_data):
        self.shader = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

        glUseProgram(self.shader)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, len(triangle_data) * 4, triangle_data, GL_STATIC_DRAW)

        # Positions input to shader. (Offset here is 0 bytes for the pointer offset in ctypes)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Colors input to shader (Offset here is 12 bytes for the pointer offset in ctypes)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        model_loc = glGetUniformLocation(self.shader, "model")
        view_loc = glGetUniformLocation(self.shader, "view")
        projection_loc = glGetUniformLocation(self.shader, "projection")

        glUniformMatrix4fv(view_loc, 1, GL_FALSE, RenderingEngine.view)
        glUniformMatrix4fv(projection_loc, 1, GL_FALSE, RenderingEngine.projection)

        rot_y = Matrix44.from_y_rotation(0)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, rot_y)

    def set_uniform_matrix4fv(self, key, value):
        # TODO: ensure key is a valid string. ensure value is a valid matrix 4x4
        glUniformMatrix4fv(glGetUniformLocation(self.shader, key), 1, GL_FALSE, value)
