"""
Basic mobius maps of
translate/rotate/scale/reciprocal plus some other improper ones
like a circle inversion and mirror reflection that are not true mobius maps
"""
import cmath
from mobius import Mobius

identity = Mobius(1, 0, 0, 1)

def translate(offset):
    """
    Translate by a complex number offset
    """
    return Mobius(1, offset, 0, 1)

def rotate(theta):
    """
    Rotation of theta radians about the origin.
    This is normalized to have determinant 1
    """
    a = cmath.exp(theta)
    return Mobius(a, 0, 0, a.conj)

def scale(k):
    """
    Scale by a complex number. The matrix will be normalized to have
    determinant 1
    """
    sqrt_det = cmath.sqrt(k)
    return Mobius(sqrt_det, 0, 0, complex(1.0) / sqrt_det)

# This transformation rotates the sphere 180 degrees about the x axis
# it is the complex conjugate of a circle inversion.
# Note that this matrix is normalized to have determinant 1
# 1/z = [0 i]
#       [i 0]
reciprocal = Mobius(0, 1j, 1j, 0)

def unit_circle_inversion(z):
    """
    Compute 1/z.conj, a true inversion in the unit circle
    """
    return complex(1) / z.conjugate()
