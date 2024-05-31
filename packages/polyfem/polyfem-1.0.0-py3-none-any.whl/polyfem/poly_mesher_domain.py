import numpy as np
import typing
import matplotlib.pyplot as plt
import math

import polyfem.poly_mesher_distance_functions as pmdf
from polyfem.poly_mesher_abstraction import Domain


class CircleDomain(Domain):

    def area(self):
        return math.pi * (self.radius ** 2)

    def distances(self, points: np.ndarray) -> np.ndarray:
        d = pmdf.d_sphere(points, self.center, radius=self.radius)
        return d

    def pFix(self) -> typing.Optional[np.ndarray]:
        return self.fixed_points

    def boundary_conditions(self, **kwargs):
        raise NotImplementedError("This is not a standard method for the CircleDomain class and is"
                                  " therefore not implemented")

    def __init__(self, bounding_box=np.array([[-1, 1], [-1, 1]]), fixed_points=None):
        super().__init__(bounding_box=bounding_box, fixed_points=fixed_points)
        self.center = 0.5 * np.array([[self.bounding_box[0, 1] + self.bounding_box[0, 0],
                                       self.bounding_box[1, 1] + self.bounding_box[1, 0]]])
        self.radius = 0.5 * min(self.bounding_box[0, 1] - self.bounding_box[0, 0],
                                self.bounding_box[1, 1] - self.bounding_box[1, 0])


class RectangleDomain(Domain):

    def area(self):
        return (self.bounding_box[0, 1] - self.bounding_box[0, 0]) * (self.bounding_box[1, 1] - self.bounding_box[1, 0])

    def distances(self, points: np.ndarray) -> np.ndarray:
        d = pmdf.d_rectangle(points, self.bounding_box[0, 0], self.bounding_box[0, 1],
                             self.bounding_box[1, 0], self.bounding_box[1, 1])
        return d

    def pFix(self) -> typing.Optional[np.ndarray]:
        return self.fixed_points

    def boundary_conditions(self, **kwargs):
        raise NotImplementedError("This is not a standard method for the CircleDomain class and is"
                                  " therefore not implemented")

    def __init__(self, bounding_box, fixed_points=None):
        super().__init__(bounding_box=bounding_box, fixed_points=fixed_points)


class LShapeDomain(Domain):

    def area(self):
        rect = (self.bounding_box[0, 1] - self.bounding_box[0, 0]) * (self.bounding_box[1, 1] - self.bounding_box[1, 0])
        return 0.75 * rect

    def distances(self, points: np.ndarray) -> np.ndarray:
        b_box = self.bounding_box
        x_m = 0.5 * b_box[0, :].sum()
        y_m = 0.5 * b_box[1, :].sum()
        d_1 = pmdf.d_rectangle(points, b_box[0, 0], b_box[0, 1], b_box[1, 0], b_box[1, 1])
        d_2 = pmdf.d_rectangle(points, x_m, b_box[0, 1], b_box[1, 0], y_m)
        d = pmdf.d_difference(d_1, d_2)
        return d

    def pFix(self) -> typing.Optional[np.ndarray]:
        b_box = self.bounding_box
        x_m = 0.5 * b_box[0, :].sum()
        y_m = 0.5 * b_box[1, :].sum()
        h = 0.005
        f_ps = np.array([[x_m - h, y_m - h], [x_m + h, y_m + h], [x_m - h, y_m + h]])
        return f_ps

    def boundary_conditions(self, **kwargs):
        raise NotImplementedError("This is not a standard method for the CircleDomain class and is"
                                  " therefore not implemented")

    def __init__(self):
        super().__init__(bounding_box=np.array([[0, 1], [0, 1]]))


class RectangleCircleDomain(Domain):

    def area(self):
        rect = (self.bounding_box[0, 1] - self.bounding_box[0, 0]) * (self.bounding_box[1, 1] - self.bounding_box[1, 0])
        radius = 0.5 * min(self.bounding_box[0, 1] - self.bounding_box[0, 0],
                           self.bounding_box[1, 1] - self.bounding_box[1, 0])
        circ = math.pi * (radius ** 2)
        return rect - circ

    def distances(self, points: np.ndarray) -> np.ndarray:
        b_box = self.bounding_box
        d_1 = pmdf.d_rectangle(points, b_box[0, 0], b_box[0, 1], b_box[1, 0], b_box[1, 1])
        d_2 = pmdf.d_sphere(points)
        d = pmdf.d_difference(d_1, d_2)
        return d

    def pFix(self) -> typing.Optional[np.ndarray]:
        return None

    def boundary_conditions(self, **kwargs):
        return None

    def __init__(self):
        super().__init__(bounding_box=np.array([[-2, 2], [-2, 2]]))


class HornDomain(Domain):

    def area(self):
        raise NotImplementedError

    def distances(self, points: np.ndarray) -> np.ndarray:
        d_1 = pmdf.d_sphere(points)
        d_2 = pmdf.d_sphere(points, center=np.array([-0.4, 0]), radius=0.55)
        d_3 = pmdf.d_line(points, 0, 0, 1, 0)
        d = pmdf.d_intersect(d_3, pmdf.d_difference(d_1, d_2))
        return d

    def pFix(self) -> typing.Optional[np.ndarray]:
        return None

    def boundary_conditions(self, **kwargs):
        return None

    def __init__(self):
        super().__init__(bounding_box=np.array([[-1, 1], [0, 1]]))


class CircleCircleDomain(Domain):

    def area(self):
        raise NotImplementedError

    def distances(self, points: np.ndarray) -> np.ndarray:
        d_1 = pmdf.d_sphere(points)
        d_2 = pmdf.d_sphere(points, center=np.array([0.2, 0]), radius=0.5)
        d = pmdf.d_difference(d_1, d_2)
        return d

    def pFix(self) -> typing.Optional[np.ndarray]:
        return None

    def boundary_conditions(self, **kwargs):
        return None

    def __init__(self):
        super().__init__(bounding_box=np.array([[-1, 1], [-1, 1]]))


# class HexagonDomain(Domain):
#
#     def distances(self, points: np.ndarray) -> np.ndarray:
#
#         d0 = pmdf.d_line(points, 11.0, -8.0*math.sqrt(3)/2.0, 11.5, -7.0*math.sqrt(3)/2.0)
#         d1 = pmdf.d_line(points, 11.5, -7.0*math.sqrt(3)/2.0, 11.0, -6.0*math.sqrt(3)/2.0)
#         d2 = pmdf.d_line(points, 11.0, -6.0*math.sqrt(3)/2.0, 11.5, -5.0*math.sqrt(3)/2.0)
#         d3 = pmdf.d_line(points, 11.5, -5.0*math.sqrt(3)/2.0, 11.0, -4.0*math.sqrt(3)/2.0)
#         d4 = pmdf.d_line(points, 11.0, -4.0*math.sqrt(3)/2.0, 11.5, -3.0*math.sqrt(3)/2.0)
#         d5 = pmdf.d_line(points, 11.5, -3.0*math.sqrt(3)/2.0, 11.0, -2.0*math.sqrt(3)/2.0)
#         d6 = pmdf.d_line(points, 11.0, -2.0*math.sqrt(3)/2.0, 11.5, -1.0*math.sqrt(3)/2.0)
#         d7 = pmdf.d_line(points, 11.5, -1.0*math.sqrt(3)/2.0, 11.0, 0.0)
#         d8 = pmdf.d_line(points, 11.0, 0.0, 11.5, 1.0*math.sqrt(3)/2.0)
#         d9 = pmdf.d_line(points, 11.5, 1.0*math.sqrt(3)/2.0, 11.0, 2.0*math.sqrt(3)/2.0)
#         d10 = pmdf.d_line(points, 11.0, 2.0*math.sqrt(3)/2.0, 11.5, 3.0*math.sqrt(3)/2.0)
#         d11 = pmdf.d_line(points, 11.5, 3.0*math.sqrt(3)/2.0, 11.0, 4.0*math.sqrt(3)/2.0)
#         d12 = pmdf.d_line(points, 11.0, 4.0*math.sqrt(3)/2.0, 11.5, 5.0*math.sqrt(3)/2.0)
#         d13 = pmdf.d_line(points, 11.5, 5.0*math.sqrt(3)/2.0, 11.0, 6.0*math.sqrt(3)/2.0)
#         d14 = pmdf.d_line(points, 11.0, 6.0*math.sqrt(3)/2.0, 11.5, 7.0*math.sqrt(3)/2.0)
#         d15 = pmdf.d_line(points, 11.5, 7.0*math.sqrt(3)/2.0, 11.0, 8.0*math.sqrt(3)/2.0)
#
#         d16 = pmdf.d_line(points, 11.0, 8.0*math.sqrt(3)/2.0, 10.0, 8.0*math.sqrt(3)/2.0)
#         d17 = pmdf.d_line(points, 10.0, 8.0*math.sqrt(3)/2.0, 9.5, 9.0*math.sqrt(3)/2.0)
#         d18 = pmdf.d_line(points, 9.5, 9.0*math.sqrt(3)/2.0, 8.5, 9.0*math.sqrt(3)/2.0)
#         d19 = pmdf.d_line(points, 8.5, 9.0*math.sqrt(3)/2.0, 8.0, 10.0*math.sqrt(3)/2.0)
#         d20 = pmdf.d_line(points, 8.0, 10.0*math.sqrt(3)/2.0, 7.0, 10.0*math.sqrt(3)/2.0)
#         d21 = pmdf.d_line(points, 7.0, 10.0*math.sqrt(3)/2.0, 6.5, 11.0*math.sqrt(3)/2.0)
#         d22 = pmdf.d_line(points, 6.5, 11.0*math.sqrt(3)/2.0, 5.5, 11.0*math.sqrt(3)/2.0)
#         d23 = pmdf.d_line(points, 5.5, 11.0*math.sqrt(3)/2.0, 5.0, 12.0*math.sqrt(3)/2.0)
#         d24 = pmdf.d_line(points, 5.0, 12.0*math.sqrt(3)/2.0, 4.0, 12.0*math.sqrt(3)/2.0)
#         d25 = pmdf.d_line(points, 4.0, 12.0*math.sqrt(3)/2.0, 3.5, 13.0*math.sqrt(3)/2.0)
#         d26 = pmdf.d_line(points, 3.5, 13.0*math.sqrt(3)/2.0, 2.5, 13.0*math.sqrt(3)/2.0)
#         d27 = pmdf.d_line(points, 2.5, 13.0*math.sqrt(3)/2.0, 2.0, 14.0*math.sqrt(3)/2.0)
#         d28 = pmdf.d_line(points, 2.0, 14.0*math.sqrt(3)/2.0, 1.0, 14.0*math.sqrt(3)/2.0)
#         d29 = pmdf.d_line(points, 1.0, 14.0*math.sqrt(3)/2.0, 0.5, 15.0*math.sqrt(3)/2.0)
#         d30 = pmdf.d_line(points, 0.5, 15.0*math.sqrt(3)/2.0, -0.5, 15.0*math.sqrt(3)/2.0)
#         d31 = pmdf.d_line(points, -0.5, 15.0*math.sqrt(3)/2.0, -1.0, 14.0*math.sqrt(3)/2.0)
#         d32 = pmdf.d_line(points, -1.0, 14.0*math.sqrt(3)/2.0, -2.0, 14.0*math.sqrt(3)/2.0)
#         d33 = pmdf.d_line(points, -2.0, 14.0*math.sqrt(3)/2.0, -2.5, 13.0*math.sqrt(3)/2.0)
#         d34 = pmdf.d_line(points, -2.5, 13.0*math.sqrt(3)/2.0, -3.5, 13.0*math.sqrt(3)/2.0)
#         d35 = pmdf.d_line(points, -3.5, 13.0*math.sqrt(3)/2.0, -4.0, 12.0*math.sqrt(3)/2.0)
#         d36 = pmdf.d_line(points, -4.0, 12.0*math.sqrt(3)/2.0, -5.0, 12.0*math.sqrt(3)/2.0)
#         d37 = pmdf.d_line(points, -5.0, 12.0*math.sqrt(3)/2.0, -5.5, 11.0*math.sqrt(3)/2.0)
#         d38 = pmdf.d_line(points, -5.5, 11.0*math.sqrt(3)/2.0, -6.5, 11.0*math.sqrt(3)/2.0)
#         d39 = pmdf.d_line(points, -6.5, 11.0*math.sqrt(3)/2.0, -7.0, 10.0*math.sqrt(3)/2.0)
#         d40 = pmdf.d_line(points, -7.0, 10.0*math.sqrt(3)/2.0, -8.0, 10.0*math.sqrt(3)/2.0)
#         d41 = pmdf.d_line(points, -8.0, 10.0*math.sqrt(3)/2.0, -8.5, 9.0*math.sqrt(3)/2.0)
#         d42 = pmdf.d_line(points, -8.5, 9.0*math.sqrt(3)/2.0, -9.5, 9.0*math.sqrt(3)/2.0)
#         d43 = pmdf.d_line(points, -9.5, 9.0*math.sqrt(3)/2.0, -10, 8.0*math.sqrt(3)/2.0)
#
#         d44 = pmdf.d_line(points, -10.0, 8.0*math.sqrt(3)/2.0, -11.0, 8.0*math.sqrt(3)/2.0)
#         d45 = pmdf.d_line(points, -11.0, 8.0*math.sqrt(3)/2.0, -11.5, 7.0*math.sqrt(3)/2.0)
#         d46 = pmdf.d_line(points, -11.5, 7.0*math.sqrt(3)/2.0, -11.0, 6.0*math.sqrt(3)/2.0)
#         d47 = pmdf.d_line(points, -11.0, 6.0*math.sqrt(3)/2.0, -11.5, 5.0*math.sqrt(3)/2.0)
#         d48 = pmdf.d_line(points, -11.5, 5.0*math.sqrt(3)/2.0, -11.0, 4.0*math.sqrt(3)/2.0)
#         d49 = pmdf.d_line(points, -11.0, 4.0*math.sqrt(3)/2.0, -11.5, 3.0*math.sqrt(3)/2.0)
#         d50 = pmdf.d_line(points, -11.5, 3.0*math.sqrt(3)/2.0, -11.0, 2.0*math.sqrt(3)/2.0)
#         d51 = pmdf.d_line(points, -11.0, 2.0*math.sqrt(3)/2.0, -11.5, 1.0*math.sqrt(3)/2.0)
#         d52 = pmdf.d_line(points, -11.5, 1.0*math.sqrt(3)/2.0, -11.0, 0.0)
#         d53 = pmdf.d_line(points, -11.0, 0.0, -11.5, -math.sqrt(3)/2.0)
#         d54 = pmdf.d_line(points, -11.5, -1.0*math.sqrt(3)/2.0, -11.0, -2.0*math.sqrt(3)/2.0)
#         d55 = pmdf.d_line(points, -11.0, -2.0*math.sqrt(3)/2.0, -11.5, -3.0*math.sqrt(3)/2.0)
#         d56 = pmdf.d_line(points, -11.5, -3.0*math.sqrt(3)/2.0, -11.0, -4.0*math.sqrt(3)/2.0)
#         d57 = pmdf.d_line(points, -11.0, -4.0*math.sqrt(3)/2.0, -11.5, -5.0*math.sqrt(3)/2.0)
#         d58 = pmdf.d_line(points, -11.5, -5.0*math.sqrt(3)/2.0, -11.0, -6.0*math.sqrt(3)/2.0)
#         d59 = pmdf.d_line(points, -11.5, -6.0*math.sqrt(3)/2.0, -11.5, -7.0*math.sqrt(3)/2.0)
#         d60 = pmdf.d_line(points, -11.5, -7.0*math.sqrt(3)/2.0, -11.0, -8.0*math.sqrt(3)/2.0)
#
#         d61 = pmdf.d_line(points, -11.0, -8.0*math.sqrt(3)/2.0, -10.0, -8.0*math.sqrt(3)/2.0)
#         d62 = pmdf.d_line(points, -10.0, -8.0*math.sqrt(3)/2.0, -9.5, -9.0*math.sqrt(3)/2.0)
#         d63 = pmdf.d_line(points, -9.5, -9.0*math.sqrt(3)/2.0, -8.5, -9.0*math.sqrt(3)/2.0)
#         d64 = pmdf.d_line(points, -8.5, -9.0*math.sqrt(3)/2.0, -8.0, -10.0*math.sqrt(3)/2.0)
#         d65 = pmdf.d_line(points, -8.0, -10.0*math.sqrt(3)/2.0, -7.0, -10.0*math.sqrt(3)/2.0)
#         d66 = pmdf.d_line(points, -7.0, -10.0*math.sqrt(3)/2.0, -6.5, -11.0*math.sqrt(3)/2.0)
#         d67 = pmdf.d_line(points, -6.5, -11.0*math.sqrt(3)/2.0, -5.5, -11.0*math.sqrt(3)/2.0)
#         d68 = pmdf.d_line(points, -5.5, -11.0*math.sqrt(3)/2.0, -5.0, -12.0*math.sqrt(3)/2.0)
#         d69 = pmdf.d_line(points, -5.0, -12.0*math.sqrt(3)/2.0, -4.0, -12.0*math.sqrt(3)/2.0)
#         d70 = pmdf.d_line(points, -4.0, -12.0*math.sqrt(3)/2.0, -3.5, -13.0*math.sqrt(3)/2.0)
#         d71 = pmdf.d_line(points, -3.5, -13.0*math.sqrt(3)/2.0, -2.5, -13.0*math.sqrt(3)/2.0)
#         d72 = pmdf.d_line(points, -2.5, -13.0*math.sqrt(3)/2.0, -2.0, -14.0*math.sqrt(3)/2.0)
#         d73 = pmdf.d_line(points, -2.0, -14.0*math.sqrt(3)/2.0, -1.0, -14.0*math.sqrt(3)/2.0)
#         d74 = pmdf.d_line(points, -1.0, -14.0*math.sqrt(3)/2.0, -0.5, -15.0*math.sqrt(3)/2.0)
#         d75 = pmdf.d_line(points, -0.5, -15.0*math.sqrt(3)/2.0, 0.5, -15.0*math.sqrt(3)/2.0)
#         d76 = pmdf.d_line(points, 0.5, -15.0*math.sqrt(3)/2.0, 1.0, -14.0*math.sqrt(3)/2.0)
#         d77 = pmdf.d_line(points, 1.0, -14.0*math.sqrt(3)/2.0, 2.0, -14.0*math.sqrt(3)/2.0)
#         d78 = pmdf.d_line(points, 2.0, -14.0*math.sqrt(3)/2.0, 2.5, -13.0*math.sqrt(3)/2.0)
#         d79 = pmdf.d_line(points, 2.5, -13.0*math.sqrt(3)/2.0, 3.5, -13.0*math.sqrt(3)/2.0)
#         d80 = pmdf.d_line(points, 3.5, -13.0*math.sqrt(3)/2.0, 4.0, -12.0*math.sqrt(3)/2.0)
#         d81 = pmdf.d_line(points, 4.0, -12.0*math.sqrt(3)/2.0, 5.0, -12.0*math.sqrt(3)/2.0)
#         d82 = pmdf.d_line(points, 5.0, -12.0*math.sqrt(3)/2.0, 5.5, -11.0*math.sqrt(3)/2.0)
#         d83 = pmdf.d_line(points, 5.5, -11.0*math.sqrt(3)/2.0, 6.5, -11.0*math.sqrt(3)/2.0)
#         d84 = pmdf.d_line(points, 6.5, -11.0*math.sqrt(3)/2.0, 7.0, -10.0*math.sqrt(3)/2.0)
#         d85 = pmdf.d_line(points, 7.0, -10.0*math.sqrt(3)/2.0, 8.0, -10.0*math.sqrt(3)/2.0)
#         d86 = pmdf.d_line(points, 8.0, -10.0*math.sqrt(3)/2.0, 8.5, -9.0*math.sqrt(3)/2.0)
#         d87 = pmdf.d_line(points, 8.5, -9.0*math.sqrt(3)/2.0, 9.5, -9.0*math.sqrt(3)/2.0)
#         d88 = pmdf.d_line(points, 9.5, -9.0*math.sqrt(3)/2.0, 10, -8.0*math.sqrt(3)/2.0)
#         d89 = pmdf.d_line(points, 10, -8.0*math.sqrt(3)/2.0, 11, -8.0*math.sqrt(3)/2.0)
#
#         d = pmdf.d_union(d0, d1)
#         for i in range(1, 91):
#             d = pmdf.d_union(d, globals().get(f"d{i % 90}"))
#
#         return d
#
#     def pFix(self) -> typing.Optional[np.ndarray]:
#         # need to add the points where the inner corners of teh boundary are! -- there are a lot.....
#         fp_s = np.array([[10.5, 1.0*math.sqrt(3)/2.0], [10.5, 3.0*math.sqrt(3)/2.0], [10.5, 5.0*math.sqrt(3)/2.0],
#                          [10.5, 7.0*math.sqrt(3)/2.0],
#                          [9.0,], [7.5,], [6.0,],
#                          [4.5,], [3.0,], [1.5,],
#                          [0.0,],
#                          [-1.5,], [-3.0,], [-4.5,],
#                          [-6.0, ], [-7.5,], [-9.0,],
#                          [-10.5, ], [-10.5, ], [-10.5, ],
#                          [-10.5, ],
#                          ])
#         # I could change all points inside to be fixed points? then at least exact?
#         return fp_s
#
#     def boundary_conditions(self, **kwargs):
#         pass
#
#     def __init__(self):
#         super().__init__(bounding_box=np.array([[-12, 12], [-12, 12]]))


def main():
    x, y = np.meshgrid(np.linspace(-2, 2, 300), np.linspace(-2, 2, 300))
    x_copy = x.copy()
    y_copy = y.copy()
    x = x.reshape((-1, 1))
    y = y.reshape((-1, 1))
    domain = HornDomain()
    out = domain.distances(np.c_[x, y])

    out = out[:, -1].reshape((300, 300))

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_surface(x_copy, y_copy, out)
    plt.show()


if __name__ == "__main__":
    main()
