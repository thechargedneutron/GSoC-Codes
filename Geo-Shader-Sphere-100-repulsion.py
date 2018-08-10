# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 17:40:55 2018

@author: Ashu
"""

import vtk
import dipy
import numpy as np
import dipy.viz.utils as ut_vtk
from dipy.viz.utils import set_input


    
colors = vtk.vtkNamedColors()

# Create the geometry of a point (the coordinate)
points = vtk.vtkPoints()
p = [65.0, -65.0, 0.0]
q = [65.0, 65.0, 0.0]
r = [-65.0, 65.0, 0.0]
s = [-65.0, -65.0, 0.0]

# Create the topology of the point (a vertex)
vertices = vtk.vtkCellArray()
# We need an an array of point id's for InsertNextCell.
pid = [0, 1000, 0, 0]
pid[0] = points.InsertNextPoint(p)
pid[1] = points.InsertNextPoint(q)
pid[2] = points.InsertNextPoint(r)
pid[3] = points.InsertNextPoint(s)
vertices.InsertNextCell(4, pid)

# Create a polydata object
point = vtk.vtkPolyData()

# Set the points and vertices we created as the geometry and
# topology of the polydata
point.SetPoints(points)
point.SetVerts(vertices)

# Create array of vertex colors
colorArray = vtk.vtkUnsignedCharArray()
colorArray.SetNumberOfTuples(4)
colorArray.SetNumberOfComponents(3)
colorArray.InsertTuple(0, (255, 0, 0))
colorArray.InsertTuple(1, (0, 255, 0))
colorArray.InsertTuple(2, (0, 0, 255))
colorArray.InsertTuple(3, (255, 255, 255))
point.GetPointData().SetScalars(colorArray)

# Visualize
mapper = vtk.vtkOpenGLPolyDataMapper()
mapper.SetInputData(point)

#LOAD THE DIPY 100 Repulsion FILE
sphere = np.load('C:/Users/Ashu/Downloads_New/dipy-master/dipy/data/files/repulsion100.npz')
faces = sphere['faces'].astype('i8')
vertices = sphere['vertices']
#    sphere = dipy.data.get_sphere("repulsion100")
#    faces = sphere.faces
#    vertices = sphere.vertices

my_polydata = vtk.vtkPolyData()
ut_vtk.set_polydata_vertices(my_polydata, vertices)
ut_vtk.set_polydata_triangles(my_polydata, faces)
#    mapper = set_input(vtk.vtkOpenGLPolyDataMapper(), my_polydata)
mapper.Update()

mapper.SetGeometryShaderCode("""
    //VTK::System::Dec
    //VTK::PositionVC::Dec
    uniform mat4 MCDCMatrix;
    uniform vec3 vertices[100];
    uniform vec3 red[3];
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
    layout(triangle_strip, max_vertices = 256) out;
    in VS_OUT {
              vec3 color;
    } gs_in[];
    out vec3 fColor;
    void build_house(vec4 position)
    {
        //fColor = gs_in[1].color;
        for(int g=0;g<100;g++){
        gl_Position = position + (MCDCMatrix * vec4(vertices[g].x, vertices[g].y, vertices[g].z, 0.0));
        EmitVertex();
        }
        //gl_Position = position + (MCDCMatrix * vec4(red[0].x, red[0].y, red[0].z, 0.0));
        //EmitVertex();
        //gl_Position = position + (MCDCMatrix * vec4(red[1].x, red[1].y, 0.0, 0.0));
        //EmitVertex();
        //gl_Position = position + (MCDCMatrix * vec4(-6.0, 6.0, 0.0, 0.0));
        //EmitVertex();
        //gl_Position = position + (MCDCMatrix * vec4(6.0, 6.0, 0.0, 0.0));
        //EmitVertex();
        //gl_Position = position + (MCDCMatrix * vec4(0.0, 12.0, 0.0, 0.0));
        //fColor = vec3(1.0, 1.0, 1.0)
        //EmitVertex();
        EndPrimitive();
    }
    void main() {
        vertexColorGSOutput = vertexColorVSOutput[0];
        build_house(gl_in[0].gl_Position);
    }
""")

vertices = vertices * 10 #To increase radius of sphere

@vtk.calldata_type(vtk.VTK_OBJECT)
def vtkShaderCallback(caller, event, calldata=None):
    program = calldata
    if program is not None:
        for i in range(100):
            program.SetUniform3f("vertices[%d]"%(i), vertices[i].tolist())
        program.SetUniform3f("red[0]", [-6.0,-6.0,0.0])
        #program.SetUniform3f("red[1]", [6.0,-6.0,0.0])
        #program.SetUniform3f("red${2}", [-6.0,6.0,0.0])
        program.SetUniformf("green", float(100/255.0))
        program.SetUniformf("blue", float(100/255.0))


mapper.AddObserver(vtk.vtkCommand.UpdateShaderEvent,vtkShaderCallback)


actor = vtk.vtkActor()
actor.SetMapper(mapper)
# actor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
actor.GetProperty().SetPointSize(2)

renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetWindowName("Point")
renderWindow.SetSize(500, 500)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.AddActor(actor)
renderer.SetBackground(colors.GetColor3d("Black"))

renderWindow.Render()
renderWindowInteractor.Start()
