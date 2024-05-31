import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from enum import Enum

from polyfem.poly_mesher_abstraction import PolyMesh


class ColorScheme(Enum):
    default = {"alpha": 0.2, "lw": 2, "edgecolor": "black", "facecolor": "blue"}
    blue = {}
    green = {}
    red = {}


def display_mesh(poly_mesh: PolyMesh, **kwargs):

    """
    :param poly_mesh:
    :param kwargs:
    :return:
    """
    fig, ax = plt.subplots()

    dimension = poly_mesh.filtered_points.shape[1]

    color_scheme = kwargs

    if "color_scheme" in kwargs:
        color_scheme = kwargs.get("color_scheme")
        assert type(color_scheme) == ColorScheme, "Input 'color_scheme' must be of type ColorScheme."
        color_scheme = color_scheme.value

    if not color_scheme:
        color_scheme = ColorScheme.default.value

    assert dimension == 2, f"The dimension of the points must be equal to 2 to use this function: the dimention of" \
                           f" the points inputted is {dimension}"

    for region in poly_mesh.filtered_regions:
        ax.add_patch(Polygon(poly_mesh.vertices[region, :], **color_scheme))

    ax.set_xlim(poly_mesh.domain.bounding_box[0, :])
    ax.set_ylim(poly_mesh.domain.bounding_box[1, :])

    plt.show()
