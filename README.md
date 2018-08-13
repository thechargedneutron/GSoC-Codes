## Code Documentation and Description

This repository contains all the work done during the GSoC period. The work started with simple shapes in Vertex and Fragment Shader and ends with arbitrary shapes generated using VS, FS and Geometry Shaders as well. All the individual code snippets are explained here and the same can be understood and observed by running the code after proper libraries installed.

## Requirements

Python 3.6+ along with the following libraries

```
1. os
2. dipy
3. vtk (8.0.1 or newer)
4. numpy
5. random
```

## Description of the Code

All the individual snippets are explained here along with a demonstration of the same.

### Frame Rate Calculation (_Frame_Rate.py_)
The motivation to try this example was to understand the functioning of a timer callback function. The frame rate is calculated by finding the difference between the current callback and the previous callback time. The inverse of the difference in seconds gives the Frame Rate in Hz. This example additionally has 10 spheres which rotate on mouse drag events. The demo can be seen here: https://youtu.be/KZv6qBAq5ig

### Sphere with user-defined color (_Sphere_Color_on_User_Input.py_)
This example was a good introduction to use SetUniform method to inject uniform values in the Shaders. The RGB values were individually injected into the shader using the `SetUniformf` method. This introduced me to the concept of injecting variables to the shader and later it is used extensively. The demo can be seen here: https://youtu.be/xPwqEfEgnCE

### Slider to change axes value of an ellipsoid (_ellipsoid_with_slider.py_)
This is more or less similar to the previous example but this time the passing of values is dynamic. Previously a sphere can have RGB values defined only at the start of the program and then it remains the same. In this case, the slider changes and the ellipsoid is rendered and updated continuously. Proper callbacks have been used to achieve this. The demo can be seen here: https://youtu.be/o0LJGDgcxUc

### Low and High Resolution Spheres (_Low_Resolution_Sphere.py_ & _High_Resolution_Sphere.py_)
Any 3D shape is made up of planar triangles. To understand how any 3D structure is formed, I used triangles to make the sphere from scratch. As the name suggests, the two spheres have a different number of triangles and thus the one with more number of triangles looked better than the one with fewer triangles. Demo here: Low Resolution: https://youtu.be/iCxQ49bhReU , High Resolution: https://youtu.be/PfKZr4vDgt8

### Geometry Shader - 1D rendering of extended lines (_Geo-Shader-Working-Example.py_)
Geometry Shader was given due importance in this project. This example was the first working example produced. This just amplifies one vertex to 10 vertices and joins them to form a wired frame of the polygon. The Geometry Shader code is injected by using the method `SetGeometryShaderCode`. The demo  is shown below: https://youtu.be/_k8jkBmq2ds

### Geometry Shader - 2D rendering of triangle strips (_Geo-Shader-Polygon.py_)
This was initially achieved by simply changing the `line_strips` to `triangle_strips`. Then, to achieve proper rotation of the polygon, with the help of my mentor David, the offset values were multiplied with the MCDC matrix to obtain the correct transformation. The demo is shown below: https://youtu.be/FiJSYcEHWSE

### Geometry Shader - 3D rendering of spheres (_Geo-Shader-Sphere.py_ & _Geo-Shader-Sphere-100-repulsion.py_ & _Geo-Shader-Sphere-100-repulsion-max-128.py_)
This is unarguably the most import part of the implementation and a big achievement to the final GSoC product. This overcomes all the shortcoming of previous attempts to Geometry Shader. The code Geometry-Shader-Sphere uses previously developed Low-Resolution-Sphere and converts injects it into Geometry Shader to develop several copies to the same shape. The implementation of Geo-Shader-Sphere-100-repulsion and Geo-Shader-Sphere-100-repulsion-max-128 uses the repulsion100 model of sphere vertices and faces to produce spheres and inject into the shader code. The later code works on systems with 128 as the amplification limit. The demonstration can be seen here: https://youtu.be/uiSrS602vQY

This is very interesting since we can use the same code with slight modification and produce as many as 30k or even more spheres without much lag. This is illustrated here: https://youtu.be/pOayomvwDNA  (MUST WATCH!!!!)

### Other Helping and Debugging Codes (_Geo-Shader-VTK-Issue.py_ & _Wide-Line-GS.py_)
These codes were made to try out the WideLine Geometry Shader Code provided by vtk library. There are known issues with this implementation and functions like `AddGeometryShaderReplacement` are broken. These were reported to vtk.
