# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 23:14:06 2018

@author: Ashu
"""

import vtk
import numpy as np
#from random import randint
import random


colors = vtk.vtkNamedColors()

# Create the geometry of a point (the coordinate)
points = vtk.vtkPoints()

# Create the topology of the point (a vertex)
vertices = vtk.vtkCellArray()
# We need an an array of point id's for InsertNextCell.
pid = [0, 1000, 0, 0]

number_of_Spheres = 4

pid = [0]*number_of_Spheres
for i in range(number_of_Spheres):
    pid[i] = points.InsertNextPoint([random.uniform(0, 500), random.uniform(0, 500), random.uniform(0, 500)])

vertices.InsertNextCell(number_of_Spheres, pid)

# Create a polydata object
point = vtk.vtkPolyData()

# Set the points and vertices we created as the geometry and
# topology of the polydata
point.SetPoints(points)
point.SetVerts(vertices)

# Create array of vertex colors
colorArray = vtk.vtkUnsignedCharArray()
colorArray.SetNumberOfTuples(number_of_Spheres)
colorArray.SetNumberOfComponents(3)
for h in range(number_of_Spheres):
    colorArray.InsertTuple(h, (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255)))
point.GetPointData().SetScalars(colorArray)

# Visualize
mapper = vtk.vtkOpenGLPolyDataMapper()
mapper.SetInputData(point)

mapper2 = vtk.vtkOpenGLPolyDataMapper()
mapper2.SetInputData(point)

mapper3 = vtk.vtkOpenGLPolyDataMapper()
mapper3.SetInputData(point)
#LOAD THE DIPY 100 Repulsion FILE
sphere = np.load('/home/geek-at-work/dipy/dipy/data/files/repulsion100.npz')
faces = sphere['faces'].astype('i8')
vertices = sphere['vertices']
#    sphere = dipy.data.get_sphere("repulsion100")
#    faces = sphere.faces
#    vertices = sphere.vertices

##################FINDING LIST OF VERTICES####################
first=0
second=1
def find_instance(faces, first, second):
    found_flag = 0
    for i in range(196):
        if faces[i, 0] == first and faces[i, 1] == second and found_flag == 0:
            found_flag = 1
            temp = faces[i, :]
            x1 = temp[1]
            x2 = temp[2]
            final_vertices_list.append(x2)
            faces[i, :] = np.array([-1,-1,-1])
    if found_flag == 1:
        return find_instance(faces, x1, x2)
    else:
        return 0

final_vertices_list = []
for j in range(196):
    x = faces[j, :] == np.array([-1, -1, -1])
    if x.sum() == 0:
        first = faces[j, 1]
        second = faces[j, 2]
        final_vertices_list.append(faces[j, 0])
        final_vertices_list.append(faces[j, 1])
        final_vertices_list.append(faces[j, 2])
        find_instance(faces, first, second)
############################################################


geometry_shader_code = """
    //VTK::System::Dec
    //VTK::PositionVC::Dec
    uniform mat4 MCDCMatrix;
    uniform vec3 vertices[100];
    uniform vec3 order[330];
    uniform vec3 red[3];
    uniform int delay;
    //VTK::PrimID::Dec
    // declarations below aren't necessary because
    // they are already injected by PrimID template
    //in vec4 vertexColorVSOutput[];
    //out vec4 vertexColorGSOutput;
    //VTK::Color::Dec
    //VTK::Normal::Dec
    //VTK::Light::Dec
    //VTK::TCoord::Dec
    //VTK::Picking::Dec
    //VTK::DepthPeeling::Dec
    //VTK::Clip::Dec
    //VTK::Output::Dec
    layout(points) in;
    layout(triangle_strip, max_vertices = 128) out;
    //in VS_OUT {
    //          vec3 color;
    //} gs_in[];
    out vec3 fColor;
    void build_house(vec4 position)
    {
        //fColor = gs_in[1].color;
        for(int g=0;g<110;g++){
        gl_Position = position + (MCDCMatrix * vec4(vertices[int(order[g+delay].x)].x, vertices[int(order[g+delay].x)].y, vertices[int(order[g+delay].x)].z, 0.0));
        EmitVertex();
        }
        EndPrimitive();
    }
    void main() {
        vertexColorGSOutput = vertexColorVSOutput[0];
        build_house(gl_in[0].gl_Position);
    }
"""
mapper.SetGeometryShaderCode(geometry_shader_code)
mapper2.SetGeometryShaderCode(geometry_shader_code)
mapper3.SetGeometryShaderCode(geometry_shader_code)
vertices = vertices * 25 #To increase radius of sphere

@vtk.calldata_type(vtk.VTK_OBJECT)
def vtkShaderCallback(caller, event, calldata=None):
    program = calldata
    if program is not None:
        for i in range(100):
            program.SetUniform3f("vertices[%d]"%(i), vertices[i].tolist())
        for j in range(330):
            program.SetUniform3f("order[%d]"%(j), [final_vertices_list[j], 0, 0])
        program.SetUniformi("delay", 110)


mapper.AddObserver(vtk.vtkCommand.UpdateShaderEvent,vtkShaderCallback)


@vtk.calldata_type(vtk.VTK_OBJECT)
def vtkShaderCallback2(caller, event, calldata=None):
    program = calldata
    if program is not None:
        for i in range(100):
            program.SetUniform3f("vertices[%d]"%(i), vertices[i].tolist())
        for j in range(330):
            program.SetUniform3f("order[%d]"%(j), [final_vertices_list[j], 0, 0])
        program.SetUniformi("delay", 0)


mapper2.AddObserver(vtk.vtkCommand.UpdateShaderEvent,vtkShaderCallback2)

@vtk.calldata_type(vtk.VTK_OBJECT)
def vtkShaderCallback3(caller, event, calldata=None):
    program = calldata
    if program is not None:
        for i in range(100):
            program.SetUniform3f("vertices[%d]"%(i), vertices[i].tolist())
        for j in range(330):
            program.SetUniform3f("order[%d]"%(j), [final_vertices_list[j], 0, 0])
        program.SetUniformi("delay", 220)


mapper3.AddObserver(vtk.vtkCommand.UpdateShaderEvent,vtkShaderCallback3)


actor = vtk.vtkActor()
actor.SetMapper(mapper)
# actor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
actor.GetProperty().SetPointSize(2)

actor2 = vtk.vtkActor()
actor2.SetMapper(mapper2)
actor2.GetProperty().SetPointSize(2)

actor3 = vtk.vtkActor()
actor3.SetMapper(mapper3)
actor3.GetProperty().SetPointSize(2)

renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetWindowName("Point")
renderWindow.SetSize(500, 500)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.AddActor(actor)
renderer.AddActor(actor2)
renderer.AddActor(actor3)
renderer.SetBackground(colors.GetColor3d("Black"))

renderWindow.Render()
renderWindowInteractor.Start()
