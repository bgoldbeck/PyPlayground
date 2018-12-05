import wx
from wx import glcanvas
from OpenGL.GL import *
from pyrr import *
import OpenGL.GL.shaders
import time, sys
from src.rendering.Model import Model

vertex_shader = """
# version 330
in layout(location = 0) vec3 positions;
in layout(location = 1) vec3 colors;

out vec3 newColor;

uniform mat4 model;

void main(){
    gl_Position = model * vec4(positions, 1.0);
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


class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(800, 600),
                                   pos=wx.Point(50, 50))
        self.init = False
        self.model = -1
        self.rotate = False
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        self.rot_y = Matrix44.identity()
        self.model_loc = -1
        glClearColor(0.1, 0.15, 0.1, 1.0)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, event):
        size = self.GetClientSize()
        glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        wx.PaintDC(self)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def InitGL(self):

        self.mesh = Model()

        shader = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


        glClearColor(0.1, 0.15, 0.1, 1.0)

        glUseProgram(shader)

        self.model_loc = glGetUniformLocation(shader, "model")


    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        # Rotate
        current_time = time.process_time()
        self.rot_y = Matrix44.from_y_rotation(current_time)
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.rot_y)
        self.Refresh()
        self.mesh.draw()
        self.SwapBuffers()


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.canvas = OpenGLCanvas(self)

        self.SetBackgroundColour("#333333")
        self.SetPosition(wx.Point(100.0, 100.0))
        self.rot_btn = wx.Button(self, -1, label="start/Stop Rotation", pos=(1130, 10))


class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (1280, 720)
        wx.Frame.__init__(self, None, title="LScan", size=self.size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)

        # Make the frame not resizeable.
        self.SetMinSize(self.size)
        self.SetMaxSize(self.size)

        self.panel = MyPanel(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Destroy()
        sys.exit(0)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
