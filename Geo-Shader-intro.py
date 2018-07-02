import vtk


def main():
    colors = vtk.vtkNamedColors()

    # Create the geometry of a point (the coordinate)
    points = vtk.vtkPoints()
    p = [45.0, -45.0, 10.0]
    q = [45.0, 45.0, 10.0]
    r = [-45.0, 45.0, 10.0]
    s = [-45.0, -45.0, 10.0]

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

    # Set the points and vertices we created as the geometry and topology of the polydata
    point.SetPoints(points)
    point.SetVerts(vertices)

    # Visualize
    mapper = vtk.vtkOpenGLPolyDataMapper()
    mapper.SetInputData(point)
    
    # mapper.AddShaderReplacement(
    # vtk.vtkShader.Geometry,
    # "//VTK::Normal::Dec", # replace the normal block
    # True, # before the standard replacements
    # "//VTK::Normal::Dec\n" # we still want the default
    # "  layout(points) in;\n"
    # "  layout(line_strip, max_vertices=2);\n", #but we add this
    # False # only do it once
    # )
    # mapper.AddShaderReplacement(
    # vtk.vtkShader.Geometry,
    # "//VTK::Normal::Impl", # replace the normal block
    # True, # before the standard replacements
    # "//VTK::Normal::Impl\n" # we still want the default
    # "  gl_Position = gl_in[0].gl_Position + vec4(-20.0, 0.0, 0.0, 0.0);\n", #but we add this
    # False # only do it once
    # )


    # # mapper.SetGeometryShaderCode(
    # # "//VTK::System::Dec\n"  # always start with this line
    # # "layout(points) in;\n"
    # # "layout(line_strip, max_vertices = 64) out;\n"
    # # "//VTK::Normal::Dec\n"
    # # "void main () {\n"
    # # "  gl_Position = gl_in[0].gl_Position + vec4(-80.0, 0.0, 0.0, 0.0);\n"
    # # " EmitVertex();\n"
    # # "EndPrimitive;\n"
    # # "}\n"
    # # )


    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
    actor.GetProperty().SetPointSize(2)

    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("Point")
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d("Black"))

    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()