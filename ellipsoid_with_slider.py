import numpy as np


import dipy.io.vtk as io_vtk
import dipy.viz.utils as ut_vtk
from dipy.viz import window, ui

import vtk



# Values of the semi-major axis of the ellipsoid
a = 1.0
b = 1.0
c = 1.0

# This is a low resolution sphere and hence I have used only 6 points of calculation
# On each value of z, I calculate four vertices, Hence only 8*6 trianlges are used.
v_range = [30.0, 60.0, 90.0, 120.0, 150.0, 180.0]

def vertices_triangles(a, b, c):

    edge_list = []
    vert_list = [[0, 0, c], [0, 0, c], [0, 0, c], [0, 0, c]]

    my_polydata = vtk.vtkPolyData() #Initialize the polydata
    for v in v_range:
    	z_new = c*np.cos(np.deg2rad(v))
    	n = len(vert_list)
    	vert_list.append([a*np.sin(np.deg2rad(v)), 0.0, z_new])
    	vert_list.append([0.0, b*np.sin(np.deg2rad(v)), z_new])
    	vert_list.append([-1*a*np.sin(np.deg2rad(v)), 0.0, z_new])
    	vert_list.append([0.0, -1*b*np.sin(np.deg2rad(v)), z_new])
    	edge_list.append([n-4, n, n-3])
    	edge_list.append([n, n+1, n-3])
    	edge_list.append([n-3, n+1, n-2])
    	edge_list.append([n+1, n+2, n-2])
    	edge_list.append([n-2, n+2, n-1])
    	edge_list.append([n+2, n+3, n-1])
    	edge_list.append([n-1, n+3, n-4])
    	edge_list.append([n+3, n, n-4])

    #Converting the list to an array
    my_vertices = np.array(vert_list)
    my_triangles = np.array(edge_list)

    #Converting the vertices and faces to a Polydata
    ut_vtk.set_polydata_vertices(my_polydata, my_vertices)
    ut_vtk.set_polydata_triangles(my_polydata, my_triangles.astype('i8'))

    # Setting colors for the sphere
    sphere_vertices = ut_vtk.get_polydata_vertices(my_polydata)
    colors = sphere_vertices * 255
    ut_vtk.set_polydata_colors(my_polydata, colors)

    sphere_actor = ut_vtk.get_actor_from_polydata(my_polydata)

    return sphere_actor

global sphere_actor
sphere_actor = vertices_triangles(1., 1., 1.)

def change_axis_length(i_ren, obj, slider):
    # A function to change the semi-major axis length
    # using the slider callback
    global a, show_manager, sphere_actor
    a = slider.value
    print(a)
    show_manager.ren.rm(sphere_actor)
    sphere_actor = vertices_triangles(a, 1., 1.)
    show_manager.ren.add(sphere_actor)
    show_manager.render()


#Relevant callbacks
line_slider = ui.LineSlider2D(initial_value=1,
                              min_value=0, max_value=1)

line_slider.add_callback(line_slider.slider_disk,
                         "MouseMoveEvent",
                         change_axis_length)

line_slider.add_callback(line_slider.slider_line,
                         "LeftButtonPressEvent",
                         change_axis_length)

global show_manager
# renderer and scene
show_manager = window.ShowManager(size=(600, 600), title="Ellipsoid")
show_manager.initialize()
show_manager.ren.add(sphere_actor)
show_manager.ren.add(line_slider)
show_manager.start()
