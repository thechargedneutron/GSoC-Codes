import numpy as np


import dipy.io.vtk as io_vtk
import dipy.viz.utils as ut_vtk
from dipy.viz import window

import vtk

my_polydata = vtk.vtkPolyData()


a = 1.0
b = 1.0
c = 1.0

v_range = [30.0, 60.0, 90.0, 120.0, 150.0, 180.0]
edge_list = []

vert_list = [[0, 0, c], [0, 0, c], [0, 0, c], [0, 0, c]]

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

my_vertices = np.array(vert_list)
my_triangles = np.array(edge_list)


ut_vtk.set_polydata_vertices(my_polydata, my_vertices)
ut_vtk.set_polydata_triangles(my_polydata, my_triangles.astype('i8'))


sphere_vertices = ut_vtk.get_polydata_vertices(my_polydata)
colors = sphere_vertices * 255
ut_vtk.set_polydata_colors(my_polydata, colors)


sphere_actor = ut_vtk.get_actor_from_polydata(my_polydata)

# renderer and scene
renderer = window.Renderer()
renderer.add(sphere_actor)
window.show(renderer, size=(600, 600), reset_camera=False)