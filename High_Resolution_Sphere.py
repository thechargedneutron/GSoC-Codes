import numpy as np

resolution = 50;
a = 1.0
b = 1.0
c = 1.0

v_range = []
for i in range(0, resolution+1):
    v_range.append((180.0 * 2.0)/(resolution) * i);

edge_list = []
vert_list = []

for v in v_range:
    z_new = c*np.cos(np.deg2rad(v))
    
    for i in range(0, resolution+1):
        ang = (180.0 * 2.0)/(resolution) * i;
        vert_list.append([a*np.sin(np.deg2rad(v))*np.cos(np.deg2rad(ang)),
                          b*np.sin(np.deg2rad(v))*np.sin(np.deg2rad(ang)),
                          c*np.cos(np.deg2rad(v))])

for hor in range(0, resolution):
    for ver in range(0, resolution):
        vert1 = (resolution+1)*hor + ver
        vert2 = (resolution+1)*(hor+1) + ver
        vert3 = (resolution+1)*hor + (ver+1)
        vert4 = (resolution+1)*(hor+1) + (ver+1)
        edge_list.append([vert1, vert2, vert3])
        edge_list.append([vert2, vert4, vert3])
        #four points are (hor, ver) (hor+1, ver) (hor, ver+1) (hor+1, ver+1)
#        make_quad(11*hor + ver, 11*(hor+1) + ver, 11*hor + (ver+1), 11*(hor+1) + (ver+1))
my_vertices = np.array(vert_list)
my_triangles = np.array(edge_list)



import dipy.viz.utils as ut_vtk
from dipy.viz import window

import vtk

my_polydata = vtk.vtkPolyData()


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