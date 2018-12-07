import wx
from wx import glcanvas
from OpenGL.GL import *
from pyrr import *
import time, sys
from src.rendering.scene import Scene
from src.rendering.scene_object import SceneObject


class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        self.size = (700, 500)
        self.aspect_ratio = self.size[0] / self.size[1]
        glcanvas.GLCanvas.__init__(self, parent, -1, size=self.size,
                                   pos=wx.Point(50, 100))

        self.init = False
        self.wire_frame = False
        self.model = -1
        self.rotate = False
        self.scene = None

        self.parent = parent
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        self.rot_y = Matrix44.identity()
        self.model_loc = -1

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

        self.scene = Scene()


        glClearColor(0.1, 0.15, 0.1, 1.0)

        glEnable(GL_DEPTH_TEST)



    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.wire_frame:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Rotate
        if self.rotate:
            self.Refresh()

        self.scene.draw()

        self.SwapBuffers()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.wf_btn = wx.Button(self, -1, label="Wire frame", pos=(400, 100))
        self.wf_btn.BackgroundColour = [255, 255, 255]
        self.wf_btn.ForegroundColour = [0, 0, 0]

        self.rot_btn = wx.Button(self, -1, label="Rotate", pos=(400, 200))
        self.rot_btn.BackgroundColour = [255, 255, 255]
        self.rot_btn.ForegroundColour = [0, 0, 0]

        self.canvas = OpenGLCanvas(self)
        self.parent = parent
        self.SetBackgroundColour("#333333")

        self.Bind(wx.EVT_BUTTON, self.on_wire_frame, self.wf_btn)
        self.Bind(wx.EVT_BUTTON, self.on_rotate, self.rot_btn)

        self.parent.Layout()

    def on_rotate(self, event):
        if not self.canvas.rotate:
            self.canvas.rotate = True
        else:
            self.canvas.rotate = False
        self.canvas.Refresh()

    def on_wire_frame(self, event):
        if not self.canvas.wire_frame:
            self.canvas.wire_frame = True
        else:
            self.canvas.wire_frame = False
        self.canvas.Refresh()

class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (1280, 720)
        wx.Frame.__init__(self, None, title="LScan", size=self.size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)

        # Make the frame not resizeable.
        self.SetMinSize((1024, 640))
        #self.SetMaxSize(self.size)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.panel = MyPanel(self)

    def on_close(self, event):
        self.Destroy()
        sys.exit(0)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        #frame.Centre()
        frame.Show()
        #frame.Fit()
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
