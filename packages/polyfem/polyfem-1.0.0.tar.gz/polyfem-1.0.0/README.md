# Poly Mesher

PolyMesher is a package aimed at mathematical and industrial applications where polygonal meshes are required for uses in finite element methods, finite volumes methods amongst many others. This package was adapted from a package developed in MATLAB [[1]](#1). Over recent years, Python has been used more extensively in scientific applications and the need for easy generation of polygonal meshes in Python is now required.

Fundamentally, the meshes generated are Voronoi tessellations, bounded by the computation domain in question. These computational domains can be built up and customised by the user. There is the option for further processing to remove certain artifacts of the Lloyd's algorithm used, including very small edges of machine precision length but note that this removes the Voronoi property. Also included is geometry generation which generates additional information about the mesh. This is then able to used in subsequent numerical methods.

## Examples

1. 800 polygon decomposition of the computational domain $[0, 1]^2$.
   ```python
   import numpy as np
    
   from poly_mesher.poly_mesher_domain import RectangleDomain
   from poly_mesher.poly_mesher_main import poly_mesher

   domain = RectangleDomain(bounding_box=np.array([[0, 1], [0, 1]]))
   poly_mesh = poly_mesher(domain, n_points=800, max_iterations=1)
   ```
   This code will generate the mesh required for a follwing numerical method. Figure .... demonstrates a potential mesh with a finite volumes solution overlapped.

2. Demonstration of ```CircleCircleDomain``` as in Figure 2.

    ```python
    from poly_mesher.poly_mesher_domain import CircleCircleDomain
    from poly_mesher.show_mesh import show_mesh

    domain = CircleCircleDomain()
    mesh = poly_mesher(domain, n_points=800)
    show_mesh(mesh.vertices, mesh.regions, bounding_box = domain.bounding_box)
    ```
    
    |![height="325"](readme_images/800_domain.png)|![height="325"](readme_images/circle_circle_domain.png)|
    |:-:|:-:|
    | Fig. 1 - 800-Polygon decomposition | Fig. 2 - 800-Polygon decomposition of the circle-circle domain |

3. Demonstration of mesh cleaning and geometry generation with a numerical application in DGFEM [[2]](#2).

    ```python
    from poly_mesher.poly_mesher_clean import poly_mesher_cleaner
    from poly_mesher.geometry_generation import GeneralGeometry

    domain = RectangleDomain(bounding_box=np.array([[0, 1], [0, 1]]))
    poly_mesh = poly_mesher(domain, n_points=1024)
    clean_poly_mesh = poly_mesher_cleaner(poly_mesh)
    mesh_geometry = GeneralGeometry(clean_mesh)
    ```
    An image of this is shown in Figure 3.
    
    |![height="325"](readme_images/dg_1024.png) |![height="325"](readme_images/3d_poly_mesher.png)|
    |:-:|:-:|
    | Fig. 3 - 1024 Element Clean Mesh under a DGFEM scheme | Fig. 4 - Example of future 3D meshes |

## Modules

1. ```poly_mesher_main```: This is the main module. It contains the ```poly_mesher``` function which generates the Voronoi spatial decompositions. It also contains additional subfunctions which are not required for general use.
2. ```poly_mesher_domain```: This module contains some prebuilt ```Domain``` sub-classes. These include the ```CircleDomain``` and the ```RectangleDomain``` as well as the more complicated ```LShapeDomain```, ```RectangleCircleDomain``` and ```HornDomain```. These are also additional examples of how to generate the more complicated domains which are possible from the basic distance functions.
3. ```poly_mesher_distance_functions```: This module contains the basic distance functions. The idea is to create a full function which is negative within the computational domain and positive otherwise. Combinations of these functions allows these domains to be built up.
4. ```poly_mesher_clean```: This module contains the clean up algorithm. Artifacts of the bounded Voronoi generation can interfere with the subsequent numerical method. The function ```poly_mesher_cleaner``` generates a ```PseudoVoronoi``` object which contains all the information required for a clean polygonal mesh but lacks the property of being Voronoi (despite being close).
5. ```geometry_generation```: This module contains the dataclass ```GeneralGeometry```. This generates the geometry for a ```PseudoVoronoi``` object. Properties of this dataclass are generated when initialising through the ```.generate()``` method. Properties that are generated include a subtriangulation, normals to each element and separation of edges into interior and boundary edges.
6. ```show_mesh```: This contains one function ```show_mesh``` which displays the generated mesh from its vertices and elements.


## Future Updates

With the code that is in place, there is the option of extending to three dimensions. This is currently being developed and tested with an emphasis on keeping the new code consistent. An early example of which is shown in Figure 4.

## How to install

The current best approach is to use pip to install github packages which are not on pypi or condaforge. The following code run in the approapriate environment is suitable.

```
pip install git+"https://github.bath.ac.uk/mje45/poly_mesher"
```

### References

<a id="1" href="https://link.springer.com/article/10.1007/s00158-011-0706-z">[1]</a> 
Talischi, C., Paulino, G., Pereira, A. and Menezes, I. (2012)
PolyMesher: a general-purpose mesh generator for polygonal elements written in MATLAB

<a id="2" href="https://www.worldscientific.com/doi/abs/10.1142/S0218202514500146">[2]</a>
Cangiani, A., Georgoulis, E. H. and Houston, P. (2014)
hp-version discontinuous Galerkin methods on polygonal and polyhedral meshes
