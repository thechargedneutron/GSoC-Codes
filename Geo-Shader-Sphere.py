# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 20:21:03 2018

@author: Ashu
"""

import vtk
import numpy as np

def main():
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

    mapper.SetGeometryShaderCode("""
        //VTK::System::Dec
        //VTK::PositionVC::Dec
        uniform mat4 MCDCMatrix;
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
        int resolution=4;
        int radius = 20;
        void build_house(vec4 position, vec4 vert1, vec4 vert2, vec4 vert3)
        {
            gl_Position = position + (MCDCMatrix * vert1);
            EmitVertex();
            gl_Position = position + (MCDCMatrix * vert2);
            EmitVertex();
            gl_Position = position + (MCDCMatrix * vert3);
            EmitVertex();
            EndPrimitive();
        }
        void main() {
            vertexColorGSOutput = vertexColorVSOutput[0];
            for(int i=0; i<resolution; i++){
                for(int j=0; j<resolution; j++){
                    float theta_1 = (3.1415 * 2.0)/(resolution) * i;
                    float theta_2 = (3.1415 * 2.0)/(resolution) * (i+1);
                    float phi_1 = (3.1415)/(resolution) * j;
                    float phi_2 = (3.1415)/(resolution) * (j+1);
                    vec4 a = vec4(radius*sin(phi_1)*cos(theta_1), radius*sin(phi_1)*sin(theta_1), radius*cos(phi_1), 0);
                    vec4 b = vec4(radius*sin(phi_1)*cos(theta_2), radius*sin(phi_1)*sin(theta_2), radius*cos(phi_1), 0);
                    vec4 c = vec4(radius*sin(phi_2)*cos(theta_1), radius*sin(phi_2)*sin(theta_1), radius*cos(phi_2), 0);
                    vec4 d = vec4(radius*sin(phi_2)*cos(theta_2), radius*sin(phi_2)*sin(theta_2), radius*cos(phi_2), 0);
                    //vec4 a = vec4(60.0, 60.0, 0.0, 0.0);
                    //vec4 b = vec4(0.0, 60.0, 0.0, 0.0);
                    //vec4 c = vec4(60.0, 0.0, 0.0, 0.0);
                    build_house(gl_in[0].gl_Position, a, b, c);
                    build_house(gl_in[0].gl_Position, b, d, c);
                }
            }
            //build_house(gl_in[0].gl_Position, vec4(60.0, 60.0, 60.0, 0.0), vec4(61.0, 60.0, 0.0, 0.0), vec4(60.0, 0.0, 0.0, 0.0));
            //build_house(gl_in[0].gl_Position, vec4(80.0, -80.0, 0.0, 0.0));
        }
    """)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # actor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
    actor.GetProperty().SetPointSize(2)

    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
#    renderWindow.SetWindowName("Point")
    renderWindow.SetSize(500, 500)
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d("Black"))

    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
