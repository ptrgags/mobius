"""
Transformations that rotate the Riemann sphere
to get a different view
"""
from mobius import Mobius
import basic_maps

# 180 degree rotations of the sphere
Rx_180 = Mobius(0, 1, 1, 0).normalize
Ry_180 = Mobius(0, -1, 1, 0).normalize
Rz_180 = Mobius(-1, 0, 0, 1).normalize

# 90 degree rotations of the sphere
Rz_90 = Mobius(1j, 0, 0, 1).normalize
Rx_90 = Mobius(1, 1j, 1j, 1).normalize
Ry_90 = Rx_90.conjugate_by(Rz_90)

# Arbitrary rotations of the sphere
# A basic rotation is around the z axis of the sphere
rotate_z = basic_maps.rotate

def rotate_x(theta):
    """
    Rotating around x can be done by rotating the x-axis to the z-axis,
    rotating the desired amount, then rotating back
    """
    return basic_maps.rotate(theta).conjugate_by(Ry_90)

def rotate_y(theta):
    """
    Same idea as rotate_x, but this time we want to rotate around the y-axis
    """
    return basic_maps.rotate(theta).conjugate_by(Rx_90.inv)
