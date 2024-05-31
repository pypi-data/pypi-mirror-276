import numpy as np
import itertools

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee

from polyfem.poly_mesher_abstraction import PolyMesh


# Section: source

def poly_mesher_extract_nodes(nodes: np.ndarray, filtered_elements: list) -> (np.ndarray, list):

    linked_elements = np.array(list((itertools.chain.from_iterable(filtered_elements))))
    unique_ = np.unique(linked_elements)  # these are the points solely used by the elements
    c_nodes = np.arange(nodes.shape[0])
    c_nodes[list(set(c_nodes).difference(set(unique_)))] = max(unique_)
    nodes, elements = poly_mesher_rebuild_lists(nodes, filtered_elements, c_nodes)

    return nodes, elements


def poly_mesher_collapse_small_edges(nodes: np.ndarray, elements: list, tolerance: float) -> (np.ndarray, list):

    while True:

        c_edge = np.array([[]])
        for element in elements:
            n_v = len(element)

            if n_v <= 3:
                continue  # this is the case when the element is a triangle -- can't collapse

            v_ = nodes[element]
            beta = np.arctan2(v_[:, 1] - np.sum(v_[:, 1])/n_v, v_[:, 0] - np.sum(v_[:, 0])/n_v)
            beta = np.mod(np.roll(beta, -1) - beta, 2 * np.pi)
            beta_ideal = 2 * np.pi / n_v
            edges = np.concatenate((np.array(element)[:, np.newaxis], np.roll(element, -1)[:, np.newaxis]), axis=1)
            idx = beta < tolerance * beta_ideal
            if (e_ := edges[idx, :]).size != 0:
                if c_edge.size == 0:
                    c_edge = np.atleast_2d(e_)
                else:
                    c_edge = np.concatenate((c_edge, np.atleast_2d(e_)), axis=0)

        if c_edge.size == 0:
            break

        c_edge = np.unique(np.sort(c_edge), axis=0)
        c_nodes = np.arange(nodes.shape[0])
        c_nodes[c_edge[:, 1]] = c_nodes[c_edge[:, 0]]

        nodes, elements = poly_mesher_rebuild_lists(nodes, elements, c_nodes)

    return nodes, elements


def poly_mesher_resequence_nodes(nodes: np.ndarray, elements: list) -> (np.ndarray, list):

    n_nodes = nodes.shape[0]
    n_n_square = sum((len(element) ** 2 for element in elements))
    i, j, s = np.zeros((n_n_square, )), np.zeros((n_n_square, )), np.zeros((n_n_square, ))
    idx = 0
    for element in elements:
        elem_set = np.arange(idx, idx + len(element) ** 2)
        i[elem_set] = np.tile(np.array(element), len(element))
        j[elem_set] = np.kron(np.array(element), np.ones((len(element),), dtype=np.int))
        s[elem_set] = 1
        idx += len(element) ** 2

    sprse = csr_matrix((s, (i, j)), shape=(n_nodes, n_nodes), dtype=np.int)
    perm = reverse_cuthill_mckee(sprse, symmetric_mode=True)

    c_nodes = np.arange(n_nodes)
    c_nodes[perm] = c_nodes

    nodes_elements = poly_mesher_rebuild_lists(nodes, elements, c_nodes)

    return nodes_elements


def poly_mesher_rebuild_lists(nodes: np.ndarray, elements: list, c_nodes: np.ndarray) -> (np.ndarray, list):
    elems_ = []
    _, idx, r_idx = np.unique(c_nodes, return_index=True, return_inverse=True)

    # idx are the indices of the unique elements -- ie the unique nodes

    if nodes.shape[0] > len(idx):
        idx[-1] = np.max(c_nodes)

    nodes = nodes[idx, :]

    for elem in elements:
        temp_elem = np.unique(r_idx[elem])
        v_ = nodes[temp_elem]
        n_v = len(temp_elem)

        perm = np.argsort(np.arctan2(v_[:, 1] - np.sum(v_[:, 1])/n_v,
                                     v_[:, 0] - np.sum(v_[:, 0])/n_v))

        elems_.append(temp_elem[perm])

    return nodes, elems_


def poly_mesher_cleaner(poly_mesh: PolyMesh, tolerence: float = 0.1) -> PolyMesh:
    """
    This is a wrapper function for a voronoi mesh output from poly_mesher_py.poly_mesher.poly_mesher function call. This
    simplifies the mesh and removes the small edges -- doesn't reorder the nodes as this is not particularly nessesary.
    :param poly_mesh:
    :param tolerence:
    :return:
    """

    vertices, regions = poly_mesher_extract_nodes(poly_mesh.vertices, poly_mesh.filtered_regions)
    vertices, regions = poly_mesher_collapse_small_edges(vertices, regions, tolerence)
    # nodes, elements = poly_mesher_resequence_nodes(nodes, elements)

    return PolyMesh(vertices, regions, poly_mesh.filtered_points, poly_mesh.ridge_points, poly_mesh.domain)


# Section: testing
#
# dom = RectangleDomain(np.array([[0.0, 1.0], [0.0, 1.0]]))
# mesh = poly_mesher(dom, max_iterations=10, n_points=100)
# clean_mesh = poly_mesher_cleaner(mesh, tolerence=0.01)
#
# for element_ in clean_mesh.filtered_regions:
#     array = np.concatenate((clean_mesh.vertices[element_, :],
#                             np.atleast_2d(clean_mesh.vertices[element_[0], :])), axis=0)
#     plt.plot(array[:, 0], array[:, 1])
#
# plt.scatter(clean_mesh.filtered_points[:, 0], clean_mesh.filtered_points[:, 1], marker='*', c='r')
# plt.show()
