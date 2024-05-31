import numpy as np
from scipy.spatial import Delaunay
from scipy.sparse import csr_matrix, find
from polyfem.poly_mesher_abstraction import PolyMesh

from dataclasses import dataclass
import pickle


@dataclass
class GeneralGeometry:

    def __init__(self, polygonal_mesh: PolyMesh, **kwargs):
        self.mesh = polygonal_mesh

        self.n_nodes = polygonal_mesh.vertices.shape[0]
        self.n_elements = len(polygonal_mesh.filtered_regions)

        self.nodes = polygonal_mesh.vertices
        self.p = polygonal_mesh.filtered_points
        self.elements = polygonal_mesh.filtered_regions

        self.elem_bounding_boxes = None  # Assume correct.....
        self.n_triangles = None  # Correct
        self.boundary_edges = None  # Correct
        self.boundary_edges_to_element = None  # Correct
        self.interior_edges = None  # Correct
        self.interior_edges_to_element = None  # Correct
        self.boundary_normals = None  # Correct
        self.interior_normals = None  # Correct

        self.subtriangulation = None  # Correct
        self.triangle_to_polygon = None  # Correct
        self.node_to_triangle_element = None  # Correct
        self.interior_edge_triangle = None  # Correct
        self.boundary_edge_triangle = None  # Correct
        self.interior_edges_to_element_triangle = None  # Correct
        self.boundary_edges_to_element_triangle = None  # Correct

        self.order = None
        self.direction = None

        if "ordering_direction" in kwargs:
            self.direction = kwargs.pop("ordering_direction")
            dists = []
            for i in range(len(self.mesh.filtered_regions)):
                dists.append((self.mesh.filtered_points[i, :] * self.direction).sum())

            self.order = np.argsort(dists)

        self.generate()

    # @staticmethod
    # def elem_share_edge(edge, total_edge, elem_total_edges):
    #
    #     t = total_edge - np.kron(edge[np.newaxis, :], np.ones((total_edge.shape[0], 1), dtype=np.int))
    #
    #     t = np.sum(np.abs(t), axis=1)
    #     idx = np.where(t == 0)
    #     edge_to_elem = []
    #
    #     for i in idx[0]:
    #         t = elem_total_edges - i
    #         ids = np.where(np.minimum(t, 0) == 0)
    #         edge_to_elem.append(ids[0][0])
    #
    #     return edge_to_elem

    # @staticmethod
    # def elem_share_node(triangle_idx, total_triangle_node, elem_total_nodes):
    #
    #     """
    #
    #     :param triangle_idx: The idx of the triangle in question
    #     :param total_triangle_node: The node indices - total_triangle_node[3 * triangle_idx : 3 * (triangle_idx + 1)]
    #     are the associated nodes for the given triangle index
    #     :param elem_total_nodes: indices for above
    #     :return:
    #     """
    #
    #     # node_idx = triangle_idx
    #     # total_trian
    #
    #     t = total_triangle_node[:, np.newaxis] - np.kron(triangle_idx, np.ones((total_triangle_node.shape[0], 1),
    #                                                                            dtype=np.int))
    #     t = np.sum(np.abs(t), axis=1)
    #
    #     idx = np.where(t == 0)[0]
    #     edge_to_elem = []
    #
    #     for i in idx:
    #         _t = elem_total_nodes - i
    #         print(_t)
    #         idxs = np.where(np.minimum(_t, 0, dtype=np.int) == 0)[0]
    #         edge_to_elem.append(idxs[0])
    #
    #     return edge_to_elem

    def generate(self, max_n: int = 20):
        # elem = np.empty((self.n_elements, 2))
        self.nodes *= 1e8
        self.nodes /= 1e8

        # elem = {'elem': {}, 'bounds': {}}

        edges_per_elem = []

        subtriangulation_0 = np.zeros((max_n, self.n_elements), dtype=np.int) - 1
        subtriangulation_1 = np.zeros((max_n, self.n_elements), dtype=np.int) - 1
        subtriangulation_2 = np.zeros((max_n, self.n_elements), dtype=np.int) - 1

        total_edge_x = np.zeros((max_n, self.n_elements), dtype=np.int) - 1
        total_edge_y = np.zeros((max_n, self.n_elements), dtype=np.int) - 1

        tri_to_poly = []
        elem_bounding_boxes = []

        for i, elem_i in enumerate(self.elements):

            elem_bounding_boxes.append([np.min(self.nodes[elem_i, 0]), np.max(self.nodes[elem_i, 0]),
                                        np.min(self.nodes[elem_i, 1]), np.max(self.nodes[elem_i, 1])])

            local_sub_tri = Delaunay(self.nodes[elem_i, :])

            n_triangles = local_sub_tri.simplices.shape[0]

            tri_to_poly += n_triangles * [i]

            subtriangulation_0[:n_triangles, i] = elem_i[local_sub_tri.simplices[:, 0]]
            subtriangulation_1[:n_triangles, i] = elem_i[local_sub_tri.simplices[:, 1]]
            subtriangulation_2[:n_triangles, i] = elem_i[local_sub_tri.simplices[:, 2]]

            n_edges = len(elem_i)

            total_edge_x[:n_edges, i] = elem_i
            total_edge_y[:n_edges, i] = np.roll(elem_i, -1)

            edges_per_elem.append(n_edges)

        subtriangulation_0 = subtriangulation_0.flatten(order="F")
        subtriangulation_1 = subtriangulation_1.flatten(order="F")
        subtriangulation_2 = subtriangulation_2.flatten(order="F")

        ind = subtriangulation_0 != -1

        subtriangulation = np.concatenate((subtriangulation_0[ind, np.newaxis],
                                           subtriangulation_1[ind, np.newaxis],
                                           subtriangulation_2[ind, np.newaxis]), axis=1)

        self.triangle_to_polygon = tri_to_poly
        self.subtriangulation = subtriangulation
        self.elem_bounding_boxes = elem_bounding_boxes

        total_edge_x = total_edge_x.flatten(order="F")
        total_edge_y = total_edge_y.flatten(order="F")

        non_zeros = total_edge_x != -1

        total_edge = np.concatenate((total_edge_x[non_zeros, np.newaxis], total_edge_y[non_zeros, np.newaxis]), axis=1)

        # classify all edges

        total_edge = np.sort(total_edge, axis=1)

        sparse_mat = csr_matrix((np.tile([1], total_edge.shape[0]), (total_edge[:, 1], total_edge[:, 0])))
        i, j, s = find(sparse_mat)

        self.boundary_edges = np.concatenate((j[s == 1, np.newaxis], i[s == 1, np.newaxis]), axis=1)
        self.interior_edges = np.concatenate((j[s == 2, np.newaxis], i[s == 2, np.newaxis]), axis=1)

        int_0 = [[j for j, _element in enumerate(self.elements) if self.interior_edges[i, 0] in _element]
                 for i in range(self.interior_edges.shape[0])]

        int_1 = [[j for j, _element in enumerate(self.elements) if self.interior_edges[i, 1] in _element]
                 for i in range(self.interior_edges.shape[0])]

        self.interior_edges_to_element = np.array(
            [sorted(list(set(int_0[i]).intersection(set(int_1[i])))) for i in range(self.interior_edges.shape[0])]
        )

        bd_0 = [[j for j, _element in enumerate(self.elements) if self.boundary_edges[i, 0] in _element]
                for i in range(self.boundary_edges.shape[0])]

        bd_1 = [[j for j, _element in enumerate(self.elements) if self.boundary_edges[i, 1] in _element]
                for i in range(self.boundary_edges.shape[0])]

        self.boundary_edges_to_element = np.array([list(set(bd_0[i]).intersection(set(bd_1[i])))
                                                   for i in range(self.boundary_edges.shape[0])]).flatten()

        # OPUNV for edges

        bd_tan_vec = self.nodes[self.boundary_edges[:, 0], :] - self.nodes[self.boundary_edges[:, 1], :]
        int_tan_vec = self.nodes[self.interior_edges[:, 0], :] - self.nodes[self.interior_edges[:, 1], :]

        bd_normalisation_consts = np.sqrt(bd_tan_vec[:, 0] ** 2 + bd_tan_vec[:, 1] ** 2)

        bd_tan_vec = np.roll(bd_tan_vec, -1, axis=1)
        bd_tan_vec[:, 1] *= -1
        bd_nor_vec = np.divide(bd_tan_vec, bd_normalisation_consts[:, np.newaxis])

        int_normalisation_consts = np.sqrt(int_tan_vec[:, 0] ** 2 + int_tan_vec[:, 1] ** 2)

        int_tan_vec = np.roll(int_tan_vec, -1, axis=1)
        int_tan_vec[:, 1] *= -1
        int_nor_vec = np.divide(int_tan_vec, int_normalisation_consts[:, np.newaxis])

        bd_outward = self.nodes[self.boundary_edges[:, 0],
                                :] - self.p[self.boundary_edges_to_element.flatten(order="F"), :]

        int_outward = self.nodes[self.interior_edges[:, 0], :] - self.p[self.interior_edges_to_element[:, 0], :]

        bd_index = np.maximum(np.sum(bd_nor_vec * bd_outward, axis=1), 0)
        int_index = np.maximum(np.sum(int_nor_vec * int_outward, axis=1), 0)

        i = np.argwhere(bd_index == 0)
        m = np.argwhere(int_index == 0)
        bd_nor_vec[i, :] = -bd_nor_vec[i, :]
        int_nor_vec[m, :] = -int_nor_vec[m, :]

        self.boundary_normals = bd_nor_vec
        self.interior_normals = int_nor_vec

        # Information for the subtriangulation

        self.n_triangles = subtriangulation.shape[0]

        total_tri_edge = np.zeros((3 * self.n_triangles, 2), dtype=np.int) - 1

        total_tri_edge[::3, :] = np.concatenate((np.atleast_2d(subtriangulation[:, 0]).T,
                                                 np.atleast_2d(subtriangulation[:, 1]).T), axis=1)
        total_tri_edge[1::3, :] = np.concatenate((np.atleast_2d(subtriangulation[:, 1]).T,
                                                  np.atleast_2d(subtriangulation[:, 2]).T), axis=1)
        total_tri_edge[2::3, :] = np.concatenate((np.atleast_2d(subtriangulation[:, 2]).T,
                                                  np.atleast_2d(subtriangulation[:, 0]).T), axis=1)

        node_to_elem_tri = {i: np.where((subtriangulation == i).any(axis=1))[0] for i in range(self.nodes.shape[0])}

        self.node_to_triangle_element = node_to_elem_tri

        total_tri_edge = np.sort(total_tri_edge, axis=1)

        sparse_mat = csr_matrix((np.tile([1], total_tri_edge.shape[0]), (total_tri_edge[:, 1], total_tri_edge[:, 0])))
        i, j, s = find(sparse_mat)
        bd_edge_tri = np.concatenate((j[s == 1, np.newaxis], i[s == 1, np.newaxis]), axis=1)
        int_edge_tri = np.concatenate((j[s == 2, np.newaxis], i[s == 2, np.newaxis]), axis=1)

        self.boundary_edge_triangle = bd_edge_tri
        self.interior_edge_triangle = int_edge_tri

        int_0_tri = [[j for j in range(self.subtriangulation.shape[0])
                      if self.interior_edge_triangle[i, 0] in self.subtriangulation[j, :]]
                     for i in range(self.interior_edge_triangle.shape[0])]

        int_1_tri = [[j for j in range(self.subtriangulation.shape[0])
                      if self.interior_edge_triangle[i, 1] in self.subtriangulation[j, :]]
                     for i in range(self.interior_edge_triangle.shape[0])]

        self.interior_edges_to_element_triangle = np.array(
            [sorted(list(set(int_0_tri[i]).intersection(set(int_1_tri[i]))))
             for i in range(self.interior_edge_triangle.shape[0])]
        )

        bd_0_tri = [[j for j in range(self.subtriangulation.shape[0])
                     if self.boundary_edge_triangle[i, 0] in self.subtriangulation[j, :]]
                    for i in range(self.boundary_edge_triangle.shape[0])]

        bd_1_tri = [[j for j in range(self.subtriangulation.shape[0])
                     if self.boundary_edge_triangle[i, 1] in self.subtriangulation[j, :]]
                    for i in range(self.boundary_edge_triangle.shape[0])]

        self.boundary_edges_to_element_triangle = np.array([list(set(bd_0_tri[i]).intersection(set(bd_1_tri[i])))
                                                            for i in range(self.boundary_edge_triangle.shape[0])])\
            .flatten()

    def save_geometry(self, filepath: str, save_mesh: bool = False):
        with open(filepath, "wb") as file:
            pickle.dump({k: v for k, v in self.__dict__.items() if k != ('mesh' if save_mesh else '')}, file)


# Section: Testing

# from poly_mesher.poly_mesher_domain import RectangleDomain
# from poly_mesher.poly_mesher_main import poly_mesher
# from poly_mesher.poly_mesher_clean import poly_mesher_cleaner
# from poly_mesher.show_mesh import show_mesh
# import matplotlib.pyplot as plt
# from matplotlib.patches import Polygon

# np.random.seed(1337)

# domain = RectangleDomain(bounding_box=np.array([[0, 1], [0, 1]]))
# voronoi = poly_mesher(domain, max_iterations=100, n_points=10)
# pseudo_voronoi = poly_mesher_cleaner(voronoi)
#
# ouput = GeneralGeometry(pseudo_voronoi)

# show_mesh(pseudo_voronoi.vertices, pseudo_voronoi.filtered_regions, bounding_box=np.array([[0, 1], [0, 1]]))
# show_mesh(ouput.nodes, ouput.subtriangulation, bounding_box=np.array([[0, 1], [0, 1]]))
#
#
# # Test triangle to polygon
#
# fig, ax = plt.subplots()
# for k, element in enumerate(ouput.subtriangulation):
#     ax.add_patch(Polygon(ouput.nodes[element, :], linewidth=1.0, edgecolor="black"))
#     centroid = np.mean(ouput.nodes[element, :], axis=0)
#     ax.annotate(f"{ouput.triangle_to_polygon[k]}", centroid)
#
# ax.set_xlim(domain.bounding_box[0, :])
# ax.set_ylim(domain.bounding_box[1, :])
#
# plt.show()
#
# # Test boundary edges + normals
#
# fig, ax = plt.subplots()
# for k, edge in enumerate(ouput.boundary_edges):
#     ax.plot(ouput.nodes[edge, 0], ouput.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(ouput.nodes[edge, :], axis=0)
#     ax.quiver(*centroid, *ouput.boundary_normals[k])
#
# plt.show()
#
# # Test interior edges + normals
#
# fig, ax = plt.subplots()
# for k, edge in enumerate(ouput.interior_edges):
#     ax.plot(ouput.nodes[edge, 0], ouput.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(ouput.nodes[edge, :], axis=0)
#     ax.quiver(*centroid, *ouput.interior_normals[k])
#
# plt.show()
#
# # Test boundary edges to element
#
# fig, ax = plt.subplots()
#
# for k, element in enumerate(ouput.elements):
#     centroid = np.mean(ouput.nodes[element, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
# for k, edge in enumerate(ouput.boundary_edges):
#     ax.plot(ouput.nodes[edge, 0], ouput.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(ouput.nodes[edge, :], axis=0)
#     ax.annotate(f"{ouput.boundary_edges_to_element[k]}", centroid)
#
# ax.set_xlim(domain.bounding_box[0, :])
# ax.set_ylim(domain.bounding_box[1, :])
#
# plt.show()
#
# # Test interior edges to element
#
# fig, ax = plt.subplots()
#
# for k, element in enumerate(ouput.elements):
#     centroid = np.mean(ouput.nodes[element, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
# for k, edge in enumerate(ouput.interior_edges):
#     ax.plot(ouput.nodes[edge, 0], ouput.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(ouput.nodes[edge, :], axis=0)
#     ax.annotate(f"{ouput.interior_edges_to_element[k]}", centroid)
#
# ax.set_xlim(domain.bounding_box[0, :])
# ax.set_ylim(domain.bounding_box[1, :])
#
# plt.show()
#
# # Test boundary edge triangle
#
# fig, ax = plt.subplots()
#
# for k, element in enumerate(ouput.subtriangulation):
#     ax.add_patch(Polygon(ouput.nodes[element, :], linewidth=1.0, edgecolor="black"))
#     centroid = np.mean(ouput.nodes[element, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
# for k, edge in enumerate(ouput.boundary_edge_triangle):
#     ax.plot(ouput.nodes[edge, 0], ouput.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(ouput.nodes[edge, :], axis=0)
#     ax.annotate(f"{ouput.boundary_edges_to_element_triangle[k]}", centroid)
#
# plt.show()
#
# # Test interior edge triangle
#
# fig, ax = plt.subplots()
#
# for k, element in enumerate(ouput.subtriangulation):
#     ax.add_patch(Polygon(ouput.nodes[element, :], linewidth=1.0, edgecolor="black"))
#     centroid = np.mean(ouput.nodes[element, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
# for k, edge in enumerate(ouput.interior_edge_triangle):
#     ax.plot(ouput.nodes[edge, 0], ouput.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(ouput.nodes[edge, :], axis=0)
#     ax.annotate(f"{ouput.interior_edges_to_element_triangle[k]}", centroid)
#
# plt.show()
#
# # Test node to triangle element
#
# fig, ax = plt.subplots()
#
# for k, element in enumerate(ouput.subtriangulation):
#     ax.add_patch(Polygon(ouput.nodes[element, :], linewidth=1.0, edgecolor="black"))
#     centroid = np.mean(ouput.nodes[element, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
#
# for k in range(ouput.nodes.shape[0]):
#     ax.plot(ouput.nodes[k, 0], ouput.nodes[k, 1], 'o', ls='-', ms=8, c="r")
#     ax.annotate(f"{ouput.node_to_triangle_element[k]}", ouput.nodes[k, :])
#
#
# ax.set_xlim(domain.bounding_box[0, :])
# ax.set_ylim(domain.bounding_box[1, :])
#
# plt.show()
