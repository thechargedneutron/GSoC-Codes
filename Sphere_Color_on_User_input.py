#!/usr/bin/env python
 
# This simple example shows how to do basic rendering and pipeline
# creation.
 
import vtk
# The colors module defines various useful colors.
from vtk.util.colors import tomato
 
# This creates a polygonal cylinder model with eight circumferential
# facets.
cylinder = vtk.vtkSphereSource()
#cylinder.SetResolution(8)
 
# The mapper is responsible for pushing the geometry into the graphics
# library. It may also do color mapping, if scalars or other
# attributes are defined.
cylinderMapper = vtk.vtkOpenGLPolyDataMapper()
cylinderMapper.SetInputConnection(cylinder.GetOutputPort())



# METHOD #1
# Modify the shader to color based on model normal
# To do this we have to modify the vertex shader
# to pass the normal in model coordinates
# through to the fragment shader. By default the normal
# is converted to View coordinates and then passed on.
# We keep that, but add a varying for the original normal.
# Then we modify the fragment shader to set the diffuse color
# based on that normal. First lets modify the vertex
# shader

R = float(raw_input("Enter the Red Component (0-255) "))
G = float(raw_input("Enter the Green Component (0-255) "))
B = float(raw_input("Enter the Blue Component (0-255) "))


# now modify the fragment shader
cylinderMapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,  # in the fragment shader
    "//VTK::Normal::Dec", # replace the normal block
    True, # before the standard replacements
    "//VTK::Normal::Dec\n" # we still want the default
    "  uniform float red;\n"
    "  uniform float green;\n"
    "  uniform float blue;\n",
    False # only do it once
)
cylinderMapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,  # in the fragment shader
    "//VTK::Normal::Impl", # replace the normal block
    True, # before the standard replacements
    "//VTK::Normal::Impl\n" # we still want the default calc
    "  diffuseColor = vec3(red, green, blue);\n", #but we add this
    False # only do it once
)




@vtk.calldata_type(vtk.VTK_OBJECT)
def vtkShaderCallback(caller, event, calldata=None):
    program = calldata
    if program is not None:
    	program.SetUniformf("red", float(R/255.0))
    	program.SetUniformf("green", float(G/255.0))
    	program.SetUniformf("blue", float(B/255.0))

cylinderMapper.AddObserver(vtk.vtkCommand.UpdateShaderEvent,vtkShaderCallback)



 
# The actor is a grouping mechanism: besides the geometry (mapper), it
# also has a property, transformation matrix, and/or texture map.
# Here we set its color and rotate it -22.5 degrees.
cylinderActor = vtk.vtkActor()
cylinderActor.SetMapper(cylinderMapper)
cylinderActor.GetProperty().SetColor(tomato)
cylinderActor.RotateX(30.0)
cylinderActor.RotateY(-45.0)
 
# Create the graphics structure. The renderer renders into the render
# window. The render window interactor captures mouse events and will
# perform appropriate camera or actor manipulation depending on the
# nature of the events.
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
# Add the actors to the renderer, set the background and size
ren.AddActor(cylinderActor)
ren.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(600, 600)
 
# This allows the interactor to initalize itself. It has to be
# called before an event loop.
iren.Initialize()
 
# We'll zoom in a little by accessing the camera and invoking a "Zoom"
# method on it.
ren.ResetCamera()
ren.GetActiveCamera().Zoom(1.5)
renWin.Render()
 
# Start the event loop.
iren.Start()