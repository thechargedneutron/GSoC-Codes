# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 01:53:49 2018

@author: Ashu
"""

import vtk


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
        layout(triangle_strip, max_vertices = 5) out;
        void build_house(vec4 position)
        {
            gl_Position = position + (MCDCMatrix * vec4(-6.0, -6.0, 0.0, 0.0));
            EmitVertex();
            gl_Position = position + (MCDCMatrix * vec4(6.0, -6.0, 0.0, 0.0));
            EmitVertex();
            gl_Position = position + (MCDCMatrix * vec4(-6.0, 6.0, 0.0, 0.0));
            EmitVertex();
            gl_Position = position + (MCDCMatrix * vec4(6.0, 6.0, 0.0, 0.0));
            EmitVertex();
            gl_Position = position + (MCDCMatrix * vec4(0.0, 12.0, 0.0, 0.0));
            EmitVertex();
            EndPrimitive();
        }
        void main() {
            vertexColorGSOutput = vertexColorVSOutput[0];
            build_house(gl_in[0].gl_Position);
        }
    """)

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

if __name__ == '__main__':
    main()
