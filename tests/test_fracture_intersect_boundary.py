"""
Test of algorithm for constraining a fracture a bounding box.

Since that algorithm uses fracture intersection methods, the tests functions as
partial test for the wider fracture intersection framework as well. Full tests
of the latter are too time consuming to fit into a unit test.

"""
import unittest
import numpy as np

from gridding.fractured.fractures import Fracture, FractureNetwork

class TestFractureBoundaryIntersection():

    def __init__(self):
        self.domain = {'xmin': 0, 'xmax': 1,
                       'ymin': 0, 'ymax': 1,
                       'zmin': 0, 'zmax': 1}

    def setup(self):
        self.f_1 = Fracture(np.array([[0, 1, 1, 0],
                                      [.5, .5, .5, .5],
                                      [0, 0, 1, 1]]))

    def _a_in_b(self, a, b, tol=1e-5):
        for i in range(a.shape[1]):
            if not np.any(np.abs(a[:, i].reshape((-1, 1))\
                                 - b).max(axis=0) < tol):
                return False
        return True

    def _arrays_equal(self, a, b):
        return self._a_in_b(a, b) and self._a_in_b(b, a)

    def test_completely_outside_lower(self):
        self.setup()
        f = self.f_1
        f.p[0] -= 2
        network = FractureNetwork([f])
        network.impose_external_boundary(self.domain)
        assert len(network._fractures) == 0

    def test_outside_west_bottom(self):
        self.setup()
        f = self.f_1
        f.p[0] -= 0.5
        f.p[2] -= 1.5
        network = FractureNetwork([f])
        network.impose_external_boundary(self.domain)
        assert len(network._fractures) == 0

    def test_intersect_one(self):
        self.setup()
        f = self.f_1
        f.p[0] -= 0.5
        f.p[2, :] = [0.2, 0.2, 0.8, 0.8]
        network = FractureNetwork([f])
        network.impose_external_boundary(self.domain)
        p_known = np.array([[0., 0.5, 0.5, 0],
                            [0.5, 0.5, 0.5, 0.5],
                            [0.2, 0.2, 0.8, 0.8]])
        assert len(network._fractures) == 1
        p_comp = network._fractures[0].p
        assert self._arrays_equal(p_known, p_comp)

    def test_intersect_two_same(self):
        self.setup()
        f = self.f_1
        f.p[0, :] = [-0.5, 1.5, 1.5, -0.5]
        f.p[2, :] = [0.2, 0.2, 0.8, 0.8]
        network = FractureNetwork([f])
        network.impose_external_boundary(self.domain)
        p_known = np.array([[0., 1, 1, 0],
                            [0.5, 0.5, 0.5, 0.5],
                            [0.2, 0.2, 0.8, 0.8]])
        assert len(network._fractures) == 1
        p_comp = network._fractures[0].p
        assert self._arrays_equal(p_known, p_comp)

    def test_incline_in_plane(self):
        self.setup()
        f = self.f_1
        f.p[0] -= 0.5
        f.p[2, :] = [0, -0.5, 0.5, 1]
        network = FractureNetwork([f])
        network.impose_external_boundary(self.domain)
        p_known = np.array([[0., 0.5, 0.5, 0],
                            [0.5, 0.5, 0.5, 0.5],
                            [0., 0., 0.5, 0.75]])
        assert len(network._fractures) == 1
        p_comp = network._fractures[0].p
        assert self._arrays_equal(p_known, p_comp)

    def test_full_incline(self):
        p = np.array([[-0.5, 0.5, 0.5, -0.5],
                      [0.5, 0.5, 1.5, 1.5],
                      [-0.5, -0.5, 1, 1]])
        f = Fracture(p)
        network = FractureNetwork([f])
        network.impose_external_boundary(self.domain)
        p_known = np.array([[0., 0.5, 0.5, 0],
                            [5./6, 5./6, 1, 1],
                            [0., 0., 0.25, 0.25]])
        assert len(network._fractures) == 1
        p_comp = network._fractures[0].p
        assert self._arrays_equal(p_known, p_comp)

if __name__ == '__main__':
    unittest.main()
