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
    polys = vtk.vtkCellArray()
    # We need an an array of point id's for InsertNextCell.
    pid = [0, 1000, 0, 0]
    pid[0] = points.InsertNextPoint(p)
    pid[1] = points.InsertNextPoint(q)
    pid[2] = points.InsertNextPoint(r)
    pid[3] = points.InsertNextPoint(s)
    polys.InsertNextCell(4, pid)

    # Create a polydata object
    polydata = vtk.vtkPolyData()

    # Set the points and polys we created as the geometry and
    # topology of the polydata
    polydata.SetPoints(points)
    polydata.SetPolys(polys)

    # Create array of vertex colors
    colorArray = vtk.vtkUnsignedCharArray()
    colorArray.SetNumberOfTuples(4)
    colorArray.SetNumberOfComponents(3)
    colorArray.InsertTuple(0, (255, 0, 0))
    colorArray.InsertTuple(1, (0, 255, 0))
    colorArray.InsertTuple(2, (0, 0, 255))
    colorArray.InsertTuple(3, (255, 255, 255))
    polydata.GetPointData().SetScalars(colorArray)

    # Visualize
    mapper = vtk.vtkOpenGLPolyDataMapper()
    mapper.SetInputData(polydata)

    mapper.SetGeometryShaderCode("""
        //VTK::System::Dec
        //VTK::PositionVC::Dec
        uniform mat4 MCDCMatrix;
        uniform mat4 MCVCMatrix;
        //VTK::PrimID::Dec
        // declarations below aren't necessary because
        // they are already injected by PrimID template
        //in vec4 vertexColorVSOutput[];
        //out vec4 vertexColorGSOutput;
        //in vec4 vertexVCVSOutput[];
        //out vec4 vertexVCVSOutput;
        //VTK::Color::Dec
        //VTK::Normal::Dec
        //VTK::Light::Dec
        //VTK::TCoord::Dec
        //VTK::Picking::Dec
        //VTK::DepthPeeling::Dec
        //VTK::Clip::Dec
        //VTK::Output::Dec

        layout(lines) in;
        layout(triangle_strip, max_vertices = 5) out;

        void build_house(vec4 position)
        {
            vec4 point1 = vec4(-6.0, -6.0, 0.0, 0.0);
            vec4 point2 = vec4(6.0, -6.0, 0.0, 0.0);
            vec4 point3 = vec4(-6.0, 6.0, 0.0, 0.0);
            vec4 point4 = vec4(6.0, 6.0, 0.0, 0.0);
            vec4 point5 = vec4(0.0, 12.0, 0.0, 0.0);

            gl_Position = position + (MCDCMatrix * point1);
            vertexVCGSOutput = vertexVCVSOutput[0] + (MCVCMatrix * point1);
            EmitVertex();
            gl_Position = position + (MCDCMatrix * point2);
            vertexVCGSOutput = vertexVCVSOutput[0] + (MCVCMatrix * point2);
            EmitVertex();
            gl_Position = position + (MCDCMatrix * point3);
            vertexVCGSOutput = vertexVCVSOutput[0] + (MCVCMatrix * point3);
            EmitVertex();
            gl_Position = position + (MCDCMatrix * point4);
            vertexVCGSOutput = vertexVCVSOutput[0] + (MCVCMatrix * point4);
            EmitVertex();
            gl_Position = position + (MCDCMatrix * point5);
            vertexVCGSOutput = vertexVCVSOutput[0] + (MCVCMatrix * point5);
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
    actor.GetProperty().SetRepresentationToWireframe()
    actor.GetProperty().SetPointSize(10)

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
