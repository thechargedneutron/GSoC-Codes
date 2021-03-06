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
        layout(line_strip, max_vertices = 11) out;
        const float PI = 3.1415926;
        void main() {
            vertexColorGSOutput = vertexColorVSOutput[0];

            for (int i = 0; i <= 10; i++) {
                float ang = PI * 2.0 / 10.0 * i;

                vec4 offset = vec4(cos(ang)*60, -sin(ang) * 60, 0.0, 0.0);
                gl_Position = gl_in[0].gl_Position + offset;

                EmitVertex();
            }
            EndPrimitive();
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
