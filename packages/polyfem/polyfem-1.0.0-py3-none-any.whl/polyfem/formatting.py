import numpy as np
from warnings import filterwarnings

from polyfem.poly_mesher_abstraction import PolyMesh
from polyfem.poly_mesher_domain import RectangleDomain
from polyfem.poly_mesher_main import poly_mesher


filterwarnings(action='ignore', category=FutureWarning)


def write_to_vtk(filepath, poly_mesh: PolyMesh, **kwargs):
    """
    This function writes a (n, 3) numpy array to a VTK file particularly with a focus on use in Paraview.
    :param filepath:
    :param poly_mesh:
    :param kwargs:
    :return:
    """

    if filepath == 'execute':
        filepath = 'python_export.vtk'

    with open(filepath, 'w') as file:
        file.write('# vtk DataFile Version 3.0\n')
        file.write('VTK from Python\n')
        file.write('ASCII\n')
        file.write('DATASET POLYDATA\n')

        vertices = poly_mesh.vertices

        dimensions = vertices.shape[1]

        if dimensions == 2:
            vertices = np.concatenate((vertices, np.zeros((vertices.shape[0], 1), dtype=np.float)), axis=1)
        elif dimensions != 3:
            raise ValueError('"vertices" must have 2 or 3 dimensional points.')

        n_points = vertices.shape[0]

        file.write(f"POINTS {n_points} float\n")

        for i in range(n_points):
            file.write(f"{vertices[i, 0]} {vertices[i, 1]} {vertices[i, 2]}\n")

        file.write('\n')

        n_elements = len(poly_mesh.filtered_regions)
        size = sum([len(element) for element in poly_mesh.filtered_regions]) + n_elements

        file.write(f"POLYGONS {n_elements} {size}\n")

        for i in range(n_elements):
            element = poly_mesh.filtered_regions[i]
            line = f"{len(element)}"
            for point in element:
                line += f" {point}"

            line += '\n'
            file.write(line)

        file.close()


# Section: testing

domain = RectangleDomain(np.array([[0, 1], [0, 1]]))
polygonal_mesh = poly_mesher(domain, max_iterations=1, n_points=100)
write_to_vtk("./polygon_data.vtk", polygonal_mesh)
