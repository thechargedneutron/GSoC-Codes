# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 05:13:07 2018

@author: Ashu
"""

import vtk

# Create two points, P0 and P1
p0 = [1.0, 0.0, 0.0]
p1 = [0.0, 1.0, 0.0]

lineSource = vtk.vtkLineSource()
lineSource.SetPoint1(p0)
lineSource.SetPoint2(p1)

# Visualize
colors = vtk.vtkNamedColors()

mapper = vtk.vtkOpenGLPolyDataMapper()
mapper.SetInputConnection(lineSource.GetOutputPort())




#mapper.SetGeometryShaderCode(
#        "uniform vec2 lineWidthNVC;\n"
#        "layout(lines) in;\n"
#        "layout(triangle_strip, max_vertices = 4) out;\n"
#        "void main() {\n"
#        "vec2 normal = normalize(\n"
#        "gl_in[1].gl_Position.xy/gl_in[1].gl_Position.w - gl_in[0].gl_Position.xy/gl_in[0].gl_Position.w);\n"
#        "normal = vec2(-1.0*normal.y,normal.x);\n"
#        "for (int j = 0; j < 4; j++){\n"
#        "int i = j/2;\n"
#        "gl_Position = vec4(\n"
#        "gl_in[i].gl_Position.xy + (lineWidthNVC*normal)*((j+1)%2 - 0.5)*gl_in[i].gl_Position.w, gl_in[i].gl_Position.z, gl_in[i].gl_Position.w);\n"
#        "EmitVertex();\n"
#        "}\n"
#        "EndPrimitive();\n"
#        "}\n"
#        )


actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetLineWidth(4)
actor.GetProperty().SetRenderLinesAsTubes(1)
actor.GetProperty().SetColor(colors.GetColor3d("Peacock"))

renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetWindowName("Line")
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.SetBackground(colors.GetColor3d("Silver"))
renderer.AddActor(actor)

renderWindow.Render()
renderWindowInteractor.Start()
