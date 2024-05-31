import numpy as np
import typing
from scipy.spatial import Voronoi
from shapely import Polygon

from polyfem.poly_mesher_visualisation import display_mesh, ColorScheme
from polyfem.poly_mesher_abstraction import PolyMesh, Domain


def poly_mesher(domain: Domain, max_iterations: int = 100, **kwargs) -> PolyMesh:
    """

    :param domain:
    :param max_iterations:
    :param kwargs:
    :return:
    """
    if "n_points" in kwargs:
        n_points = kwargs.get("n_points")
        points = poly_mesher_init_point_set(domain, n_points=n_points)

    elif "n_x" in kwargs and "n_y" in kwargs:
        n_x = kwargs.get("n_x")
        n_y = kwargs.get("n_y")
        points = poly_mesher_init_point_set(domain, n_x=n_x, n_y=n_y)

    else:
        raise AttributeError("key word error: must be just `n_points` or both `n_x` and `n_y`.")

    fixed_points = domain.pFix()  # from here can call domain.fixed_points -- this initialises the property simult
    if fixed_points is not None:
        points = np.concatenate((fixed_points, points), axis=0)
        n_fixed = fixed_points.shape[0]
    else:
        n_fixed = 0

    iteration, error, tolerance = 0, 1.0, 1e-4
    bounding_box = domain.bounding_box
    area = (bounding_box[0, 1] - bounding_box[0, 0]) * (bounding_box[1, 1] - bounding_box[1, 0])
    n_points = points.shape[0]

    voronoi, nodes, elements = None, None, None

    while iteration <= max_iterations and error > tolerance:
        reflected_points = poly_mesher_reflect(points, domain, area)

        voronoi = Voronoi(np.concatenate((points, reflected_points), axis=0), qhull_options='Qbb Qz')
        cond_len = len(voronoi.regions[0]) == 0

        nodes = voronoi.vertices
        if cond_len:
            sorting = [np.where(voronoi.point_region == x)[0][0] for x in range(1, len(voronoi.regions))]
            elements = [x for _, x in sorted(zip(sorting, voronoi.regions[1:]))]
        else:
            empty_ind = voronoi.regions.index([])
            sorting_1 = [np.where(voronoi.point_region == x)[0][0] for x in range(0, empty_ind)]
            sorting_2 = [np.where(voronoi.point_region == x)[0][0] for x in range(empty_ind+1, len(voronoi.regions))]
            sorting = sorting_1 + sorting_2
            regions = voronoi.regions
            del regions[empty_ind]
            elements = [x for _, x in sorted(zip(sorting, regions))]

        points, area, error = poly_mesher_vorocentroid(points, nodes, elements)

        if fixed_points is not None:
            points[:n_fixed, :] = fixed_points

        iteration += 1
        # show_mesh(voronoi.vertices, elements[: n_points], bounding_box=bounding_box, alpha=0.4, edgecolor="#556575")

        if iteration % 10 == 0:
            print(f"Iteration: {iteration}. Error: {error}")

    # editing outputs of the vornoi class to have solely the interior points and regions remaining
    voronoi.filtered_points = points
    voronoi.filtered_regions = elements[: n_points]
    voronoi.domain = domain

    if "show_mesh" in kwargs:
        show_m = kwargs.get("show_mesh")
        assert type(show_m) == bool, "Input 'show_mesh' must be a boolean variable."

        if show_m:
            color_scheme = ColorScheme.default
            if "color_scheme" in kwargs:
                color_scheme = kwargs.get("color_scheme")
                assert type(color_scheme) == ColorScheme

            display_mesh(voronoi, color_scheme=color_scheme)

    return voronoi


def poly_mesher_init_point_set(domain: Domain, **kwargs) -> np.ndarray:
    """
    This function initialises the point set to be able to use the lloyds algorithm. Can be done uniformly via ```n_x```
    and ```n_y``` or the number of points that reside in the domain via ```n_points```.
    :param domain: Insert the domain of choice here. Must be subclass of the poly_mesher_domain.Domain class.
    :param kwargs: Input either ```n_points``` for number of points within the domain or ```n_x``` and ```n_y``` for
    uniformly spread points throughout the domain (and outside the domain, but these points are simply removed).
    :return: A np.ndarray of points that are within the domain and can be used to intialise the lloyds algorithm.
    """
    # Done: tested fully!
    bounding_box = domain.bounding_box

    if "n_points" in kwargs:
        # This generates a random point set
        n_points = kwargs.get("n_points")
        points = np.full((n_points, 2), -np.inf)
        s = 0
        np.random.seed(1337)
        while s < n_points:
            p_1 = (bounding_box[0, 1] - bounding_box[0, 0]) * np.random.uniform(size=(1, n_points)).T + bounding_box[0,
                                                                                                                     0]
            p_2 = (bounding_box[1, 1] - bounding_box[1, 0]) * np.random.uniform(size=(1, n_points)).T + bounding_box[1,
                                                                                                                     0]
            p = np.concatenate((p_1, p_2), axis=1)
            d = domain.distances(p)
            last_index_negative = np.argwhere(d[:, -1] < 0.0)  # index of the seeds within the domain
            number_added = min(n_points - s, last_index_negative.shape[0])
            points[s:s + number_added, :] = p[last_index_negative[:number_added].T.flatten(), :]
            s += number_added

    elif "n_x" in kwargs and "n_y" in kwargs:
        # This generates a uniformly spread point set
        n_x = kwargs.get("n_x")
        n_y = kwargs.get("n_y")

        x = np.linspace(bounding_box[0, 0], bounding_box[0, 1], n_x + 1)
        y = np.linspace(bounding_box[1, 0], bounding_box[1, 1], n_y + 1)
        x_c = 0.5 * (x[1:] + x[:-1])
        y_c = 0.5 * (y[1:] + y[:-1])
        [X, Y] = np.meshgrid(x_c, y_c)

        X, Y = X.T, Y.T
        points = np.concatenate((np.reshape(X, (-1, 1), order='F'), np.reshape(Y, (-1, 1), order="F")), axis=1)
        d = domain.distances(points)
        log_ind = d[:, -1] < 0.0
        points = points[log_ind, :]

    else:
        raise AttributeError("key word error: must be just `n_points` or both `n_x` and `n_y`.")

    return points


def poly_mesher_reflect(points: np.ndarray, domain: Domain, area: float) -> (np.ndarray, np.ndarray):
    # done
    """
    Compute the reflection point sets
    :param points:
    :param domain:
    :param area:
    :return:
    """
    epsilon = 1.0e-8
    n_points = points.shape[0]
    alpha = 1.5 * np.sqrt(area / float(n_points))

    d = domain.distances(points)
    n_boundary_segments = d.shape[1] - 1

    n_1 = 1.0 / epsilon * (domain.distances(points + np.tile(np.array([epsilon, 0.0]), (n_points, 1))) - d)
    n_2 = 1.0 / epsilon * (domain.distances(points + np.tile(np.array([0.0, epsilon]), (n_points, 1))) - d)

    # singles out the points that are within (1.5x) average side length of a region to the boundary
    log_ind = np.abs(d[:, :n_boundary_segments]) < alpha

    p_1 = np.tile(points[:, 0][:, np.newaxis], (1, n_boundary_segments))
    p_2 = np.tile(points[:, 1][:, np.newaxis], (1, n_boundary_segments))

    p_1 = np.concatenate([p_1[log_ind[:, i], i] for i in range(n_boundary_segments)], axis=0)[:, np.newaxis]
    p_2 = np.concatenate([p_2[log_ind[:, i], i] for i in range(n_boundary_segments)], axis=0)[:, np.newaxis]

    n_1 = np.concatenate([n_1[log_ind[:, i], i] for i in range(n_boundary_segments)], axis=0)[:, np.newaxis]
    n_2 = np.concatenate([n_2[log_ind[:, i], i] for i in range(n_boundary_segments)], axis=0)[:, np.newaxis]

    d = np.concatenate([d[log_ind[:, i], i] for i in range(n_boundary_segments)], axis=0)[:, np.newaxis]

    r_ps = np.concatenate((p_1, p_2), axis=1) - 2.0 * np.concatenate((n_1, n_2), axis=1) * np.tile(d, (1, 2))

    r_p_ds = domain.distances(r_ps)

    logical_rp = np.logical_and(r_p_ds[:, -1] > 0, np.abs(r_p_ds[:, -1]) >= 0.9 * np.abs(d).flatten())

    r_ps = r_ps[logical_rp, :]

    if not r_ps.size == 0:
        r_ps = np.unique(r_ps, axis=0)

    return r_ps


def poly_mesher_reorder(node: np.ndarray, elements: np.ndarray) -> typing.Tuple[np.ndarray, np.ndarray]:
    # [nodes, elements] -> [nodes, elements]
    concat_elements = np.concatenate([element for element in elements], axis=0)
    _id, _, total_id = np.unique(concat_elements, return_index=True, return_inverse=True)
    node = node[_id, :]
    len_elements = [len(element) for element in elements]
    elements = np.split(total_id.T, len_elements)
    for i in range(len(len_elements)):
        ind = elements[i]
        z1, z2, z3 = node[ind[0], :], node[ind[1], :], node[ind[2], :]
        e2, e3 = z3 - z1, z1 - z2
        area = 0.5 * (-e3[:, 0].T * e2[:, 1] + e3[:, 1].T * e2[:, 0])
        if area < 0.0:
            elements[i] = ind[::-1]

    return node, total_id


# def poly_mesher_remove_smalledge(nodes: np.ndarray, elements: np.ndarray) -> typing.Tuple[np.ndarray, np.ndarray]:
#     # [nodes, elements] -> [nodes, elements]
#     """
#
#     :param nodes:
#     :param elements:
#     :return:
#     """
#     nodes, elements = poly_mesher_reorder(nodes, elements)
#     t_1 = [[element[1:], element[0]] for element in elements]
#     v_0 = np.concatenate((element for element in elements), axis=0).T
#     v_1 = np.concatenate((np.array(element) for element in t_1), axis=0).T
#     total_edge = np.sort(np.concatenate((v_0, v_1), axis=0), axis=0)
#     ind_start, ind_end = np.nonzero(csr_matrix((1, (total_edge[:, 1], total_edge[:, 0]))))
#     z_1, z_2 = nodes[ind_end, :], nodes[ind_start, :]
#     he = np.sqrt(np.sum((z_1 - z_2) ** 2, axis=0))
#     ir = np.nonzero(he < 0.1 * np.max(he))
#     nv_1, nv_2 = ind_end[ir], ind_start[ir]
#     _id, _, total_id = np.unique(v_0, return_index=True, return_inverse=True)
#     total_id = _id[total_id]
#     for i in range(len(nv_2)):
#         v1, v2 = nv_1[i], nv_2[i]
#         total_id[total_id == v2] = v1
#         nv_1[nv_1 == v2], nv_2[nv_2 == v2] = v1, v1
#
#     len_elements = [len(element) for element in elements]
#     elements = np.split(total_id.T, len_elements)
#     for j in range(len(len_elements)):
#         ind = elements[j]
#         _, index = np.unique(ind, return_index=True)
#         elements[j] = ind[np.sort(index)]
#
#     nodes, elements = poly_mesher_reorder(nodes, elements)
#     return nodes, elements


def poly_mesher_vorocentroid(points: np.ndarray, vertices, elements) -> (np.ndarray, float, float):
    # [P, node, elem] -> [Pc,Area,Err]
    """
    This function calculates the centroid of a Voronoi cell
    :param points: A set of points as inputs
    :param vertices: The list of vertices of the whole Voronoi diagram
    :param elements: The list of lists of vertex indicies that make up each Voronoi cell
    :return:
    """
    n_points = points.shape[0]
    center_points = np.full((n_points, 2), -np.inf)
    areas = np.full((n_points,), -np.inf)

    for i in range(n_points):
        region = Polygon(vertices[elements[i]])
        areas[i] = region.area
        center_points[i, :] = np.array(region.centroid.coords.xy).T.flatten()

    total_area = areas.sum()
    error = np.sqrt(np.sum((areas ** 2) * np.sum((center_points - points) ** 2, 1), 0)) * n_points / total_area ** 1.5

    return center_points, total_area, error


# def poly_mesher_collapse_small_edges(vertices: np.ndarray, regions: list, tolerence: float = 0.1):
#     while True:
#         collapsed_edge = None
#         for region in regions:
#             n_verts = len(region)
#             if n_verts < 4:
#                 # we don't want to collapse triangles
#                 continue
#             region_verts = vertices[region, :]
#             beta = np.arctan2(region_verts[:, 1] - region_verts[:, 1].sum() / n_verts,
#                               region_verts[:, 0] - region_verts[:, 0].sum() / n_verts)
#
#             beta = (np.roll(beta, -1) - beta) % (2 * np.pi)
#             beta_ideal = 2.0 * np.pi / n_verts
#             edges = np.concatenate((np.array(region)[np.newaxis, ].T,
#                                     np.roll(np.array(region)[np.newaxis, ].T, -1)), axis=1)
#             beta_cond = beta < tolerence * beta_ideal
#             additional_edges = edges[beta_cond, :]
#             if collapsed_edge is None:
#                 collapsed_edge = additional_edges
#                 if collapsed_edge.size == 0:
#                     collapsed_edge = None
#             else:
#                 if additional_edges.size != 0:
#                     print(additional_edges, collapsed_edge)
#                     collapsed_edge = np.concatenate((collapsed_edge, additional_edges), axis=0)
#
#         if collapsed_edge is None:
#             break
#
#         collapsed_edge = np.unique(collapsed_edge, axis=0)
#         collapsed_nodes = [i for i in range(vertices.shape[0])]
#         for i in range(collapsed_edge.shape[0]):
#             collapsed_nodes[collapsed_edge[i, 1]] = collapsed_nodes[collapsed_edge[i, 0]]
#
#         out_verts, out_regions = poly_mesher_rebuild_lists(vertices, regions, collapsed_nodes)
#
#         return out_verts, out_regions


# def poly_mesher_rebuild_lists(vertices, regions, collapsed_nodes):
#     out_regions = []
#     _, indices, inverses = np.unique(collapsed_nodes, axis=0, return_index=True, return_inverse=True)
#
#     if vertices.shape[0] > len(indices):
#         indices[-1] = max(collapsed_nodes)
#
#     out_verts = vertices[indices, :]
#     for i in range(len(regions)):
#         region = np.unique(inverses[regions[i]])
#         region_verts = vertices[region]
#         n_verts = region_verts.shape[0]
#         permutation = np.argsort(np.arctan2(region_verts[:, 1] - region_verts[:, 1].sum() / n_verts,
#                                             region_verts[:, 0] - region_verts[:, 0].sum() / n_verts))
#         out_regions.append(region[permutation])
#
#     return out_verts, out_regions


# def unique_points(points, atol=1e-8):
#     """Get unique (within atol) rows of a 2D np.array A."""
#     remove = np.zeros(points.shape[0], dtype=bool)  # Row indexes to be removed.
#     for i in range(points.shape[0]):  # Not very optimized, but simple.
#         equals = np.all(np.isclose(points[i, :], points[(i + 1):, :], atol=atol), axis=1)
#         remove[(i + 1):] = np.logical_or(remove[(i + 1):], equals)
#     return points[np.logical_not(remove)]


# def sort_xy(x, y):
#     """
#     This takes lists of x and y coordinates and sorts the associated points in an anticlockwise manner
#     :param x: List/array of x-coordinates
#     :param y: List/array of y-coordinates
#     :return: x, y but sorted in an anticlockwise manner
#     """
#     x0, y0 = np.mean(x), np.mean(y)
#     r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
#     angles = np.where((y - y0) > 0, np.arccos((x - x0) / r), 2 * np.pi - np.arccos((x - x0) / r))
#     mask = np.argsort(angles)
#     x_sorted, y_sorted = x[mask], y[mask]
#     return x_sorted, y_sorted
