""" pytest for objects in _objects.py"""

import numpy as np
import pytest

from optrix import ThinLens, Mirror, FreeSpace, Boundary, System 

class Test_Objects:
    """Test class for optrix objects. """

    def test_ThinLens(self):
        lens_with_f = ThinLens(focal_length=0.5, name = "test lens with f")
        lens_without_f = ThinLens(n=2, radius1=1, radius2=-1, name = "test lens without f")

        initial_point = np.array([1, 1])
        final_point_1 = lens_with_f * initial_point
        final_point_2 = lens_without_f * initial_point

        np.testing.assert_array_equal(final_point_1, np.array([1, -1]))
        np.testing.assert_array_equal(final_point_2, np.array([1, -1]))

    def test_Mirror(self):
        mirror_flat = Mirror(name = "test flat mirror")
        mirror_spherical = Mirror(radius=2, name = "test spherical mirror")
        
        initial_point = np.array([1, 1])
        
        final_point_flat = mirror_flat * initial_point
        final_point_spherical = mirror_spherical * initial_point
        
        np.testing.assert_array_equal(final_point_flat, np.array([1, 1]))
        np.testing.assert_array_equal(final_point_spherical, np.array([1, 2]))

    def test_FreeSpace(self):
        freespace = FreeSpace(length=10, name = "test freespace")
        
        initial_point = np.array([1, 1])
        final_point = freespace * initial_point
        
        np.testing.assert_array_equal(final_point, np.array([11, 1]))

    def test_Boundary(self):
        boundary_flat = Boundary(n1=1, n2=2, name="test flat boundary")
        boundary_spherical = Boundary(n1=1, n2=2, radius=2, name="test spherical boundary")

        initial_point = np.array([1, 1])
        final_point_flat = boundary_flat * initial_point
        final_point_spherical = boundary_spherical * initial_point

        np.testing.assert_array_equal(final_point_flat, np.array([1, 0.5]))
        np.testing.assert_array_equal(final_point_spherical, np.array([1, 0.25]))

    def test_System(self):
        lens = ThinLens(focal_length=0.5, name = "test lens")
        mirror = Mirror(radius=2, name = "test mirror")
        freespace = FreeSpace(length=10, name = "test freespace")
        boundary = Boundary(n1=1, n2=2, radius=2, name="test boundary")

        system = System([lens, mirror, freespace, boundary], name = "test system")

        initial_point = np.array([1, 1])
        final_point = system * initial_point

        np.testing.assert_array_equal(final_point, np.array([3.5, -3.25]))