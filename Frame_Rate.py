import os
from dipy.data import read_viz_icons, fetch_viz_icons
from dipy.viz import ui, window

# Initializing a TextBox to display the Frame Rate
global tb
tb = ui.TextBlock2D()

# A callback function to calculate Frame Rate
def timer_callback(obj, event):
    global show_manager, tb
    tb.message = "Frame Rate : " + str(1.0/show_manager.ren.GetLastRenderTimeInSeconds())
    show_manager.render()

current_size = (600, 600)
global show_manager
show_manager = window.ShowManager(size=current_size, title=" Frame Rate")
show_manager.initialize()
show_manager.ren.add(tb.get_actor())

# Rendering 10 spheres
for i in range(10):
    sphereSource = window.vtk.vtkSphereSource()
    sphereSource.SetCenter(i, 0, 0)

    mapper = window.vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphereSource.GetOutputPort())

    actor = window.vtk.vtkActor()
    actor.SetMapper(mapper)

    show_manager.ren.add(actor)

show_manager.add_timer_callback(True, 200, timer_callback)
show_manager.start()
