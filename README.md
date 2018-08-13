# GSoC-Codes
This repository contains code which I have written at the initial phase of my GSoC project.

## Code Documentation and Description

This repository contains all the work done during the GSoC period. The work started with simple shapes in Vertex and Fragment Shader and ends with arbitraty shapes generated using VS, FS and Geometry Shaders as well. All the indivual code snippets are explained here and the same can be understood and observed by running the code after proper libraries installed.

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
The motivation to try this example was to understand about the functioning of a timer callback function. The frame rate is calulated by finding the difference between current callback and the previous callback time. The inverse of the difference in seconds give the Frame Rate in Hz. This example additionally has 10 spheres which rotates on mouse drag events. Demo can be seen here:

(DEMO)

### 
