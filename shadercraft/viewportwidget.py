import logging as Log
import OpenGL.GL as GL
from PySide6.QtWidgets import QWidget
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QOpenGLContext
from PySide6.QtCore import QTimer

from .asserts import assertRef, assertTrue
from .gfx import GFX, GFXRenderable


class ViewportWidget(QOpenGLWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.fallback_shader = GFX.createFallbackShaderProgram()
        self.preview_geo: GFXRenderable = GFX.createTriangleRenderable()
        GFX.bindRenderableShader(self.preview_geo, self.fallback_shader)

    def initializeGL(self) -> None:
        """Initialise graphics context for this widget"""
        Log.info("Attempting to initialise OpenGL context")
        Log.info(f"OpenGL Version: {GL.glGetString(GL.GL_VERSION).decode()}")
        self.context().makeCurrent(self.context().surface())
        self.shader = GFX.createFallbackShaderProgram()
        self.triangle = GFX.createTriangleRenderable()
        GFX.bindRenderableShader(self.triangle, self.shader)
 

    def paintGL(self) -> None:
        """Redraw GL surface"""
        self.makeCurrent()

        GL.glClearColor(0.33, 0.33, 0.33, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glBindVertexArray(self.preview_geo.vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.preview_geo.vbo)
        GL.glUseProgram(self.fallback_shader)
        GL.glBindVertexArray(self.preview_geo.vao)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    def resizeGL(self, w: int, h: int) -> None:
        """
        Event handler invoked when the GL surface is resized.
        This can happen when the actual widget is resized by QT layout engine.
        """
        Log.debug("Resizing OpenGL viewport widget")
        GL.glViewport(0, 0, w, h)

    def requestRedraw(self) -> None:
        """Redraws the OpenGL viewport"""
        self.update()
