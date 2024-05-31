import numpy as np
import typing
import matplotlib.pyplot as plt


def d_sphere(p: np.ndarray, center: typing.Optional[np.ndarray] = None, radius: float = 1.0) -> np.ndarray:
    """
    Input a array of coordinates in ```p``` in the form [p_0; p_1; ...; p_n] for p_i = [x_i, y_i] or [x_i, y_i, z_i].
     From here, the distance from the center of the sphere is calculated. This will be "translated" by the radius to
     generate a function which is negative for the interior of the sphere and positive outside of the sphere.
    :param p: The array of points of the form [p_0; p_1; ...; p_n] for p_i = [x_i, y_i] or [x_i, y_i, z_i].
    :param center: The center of the spherical domain. If ```None``` inputted, then defaults to the origin for the
     dimension of the points inputted.
    :param radius: Radius of the spherical domain required -- defaults to 1.0.
    :return: An array of distances in the form [d_0, d_0; d_1, d_1; ...; d_n, d_n]
    """

    if center is None:
        center = np.zeros((1, p.shape[1]))

    p_shape = p.shape[1]
    center_shape = center.shape
    if not 2 <= p_shape <= 3:
        raise Exception(f"p must contain points of dimention 2 or 3: p has points of dimension {p_shape}")

    if center_shape == (p_shape,):
        center = center[:, np.newaxis].T
    elif not center_shape == (1, p_shape):
        raise Exception(f"center must be a points of equal to those in p: center has points of dimension"
                        f" {center_shape}: must be either ({p_shape},) or (1, {p_shape})")

    d = (np.sqrt(np.sum((p - center) ** 2, axis=1)) - radius)[:, np.newaxis]
    d = np.concatenate((d, d), axis=1)

    return d


def d_rectangle(p: np.ndarray, x1: float, x2: float, y1: float, y2: float) -> np.ndarray:
    d = [x1 - p[:, 0], p[:, 0] - x2, y1 - p[:, 1], p[:, 1] - y2]
    d = np.vstack(d)
    max_d = np.max(d, axis=0)
    d = np.vstack((d, max_d)).T
    return d


def d_line(p: np.ndarray, x1: float, y1: float, x2: float, y2: float) -> np.ndarray:
    a = np.array([x2 - x1, y2 - y1])
    a = a/np.linalg.norm(a)
    p[:, 0] = p[:, 0] - x1
    p[:, 1] = p[:, 1] - y1
    d = (p[:, 0] * a[1] - p[:, 1] * a[0])[:, np.newaxis]
    d = np.concatenate((d, d), axis=1)
    return d


def d_intersect(d1: np.ndarray, d2: np.ndarray) -> np.ndarray:
    # todo: test this function

    d = _d_combination(d1, d2, "max")
    return d


def d_union(d1: np.ndarray, d2: np.ndarray) -> np.ndarray:
    # todo: test this function

    d = _d_combination(d1, d2, "min")
    return d


def d_difference(d1: np.ndarray, d2: np.ndarray) -> np.ndarray:
    # test this function

    d = _d_combination(d1, d2, "diff")
    return d


def _d_combination(d1: np.ndarray, d2: np.ndarray, functionality: str) -> np.ndarray:
    # todo: test this function alongside the other d_union and d_intersection functions

    if functionality == "min":
        func_d = np.min(np.concatenate((d1[:, -1][:, np.newaxis], d2[:, -1][:, np.newaxis]), axis=1), axis=1)[:,
                 np.newaxis]
    elif functionality == "max":
        func_d = np.max(np.concatenate((d1[:, -1][:, np.newaxis], d2[:, -1][:, np.newaxis]), axis=1), axis=1)[:,
                 np.newaxis]
    elif functionality == "diff":
        func_d = np.max(np.concatenate((d1[:, -1][:, np.newaxis], -d2[:, -1][:, np.newaxis]), axis=1), axis=1)[:,
                 np.newaxis]
    else:
        raise ValueError("The input for functionality is invalid: poly_mesher_distance_functionc._d_combination")

    d1 = d1[:, :d1.shape[1] - 1]
    d2 = d2[:, :d2.shape[1] - 1]
    if len(d1.shape) == 1 or len(d2.shape) == 1:
        d = np.concatenate((d1[:, np.newaxis], d2[:, np.newaxis]), axis=1)
    else:
        d = np.concatenate((d1, d2), axis=1)

    d = np.concatenate((d, func_d), axis=1)
    return d


def main():
    # out = d_sphere(np.array([[0.1 * i, 0.1 * i] for i in range(-20, 20)]), np.array([0, 0]))
    x, y = np.meshgrid(np.linspace(-1, 2, 100), np.linspace(-1, 2, 100))
    x_copy = x.copy()
    y_copy = y.copy()
    x = x.reshape((-1, 1))
    y = y.reshape((-1, 1))
    out = d_rectangle(np.c_[x, y], 0, 1, 0, 1)

    print(out)

    out = out[:, -1].reshape((100, 100))

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_surface(x_copy, y_copy, out)
    plt.show()


if __name__ == "__main__":
    main()
