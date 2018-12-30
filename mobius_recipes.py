"""
Recipes from the book Indra's Pearls by David Mumford et al.
plus some of my own variations
"""
from mobius import Mobius

def upper_half_plane(a, b, c, d):
    """
    Recipe I (Indra's Pearls pp. 85-87)
    Upper Half Plane Group: Mobius transformations in SL(2, R)
    (matricies with real entries and determinant 1). These map
    the upper half plane to the upper half plane.
    """
    # Make it inconvenient to input anything besides real numbers
    A = float(a)
    B = float(b)
    C = float(c)
    D = float(d)
    return Mobius(A, B, C, D)

# Recipe II (Indra's Pearls pp. 87-88)
# The Cayley Map K(z) is a 120 degree rotation of the Riemann sphere such
# that infinity -> 1, 1 -> -i, -i -> infinity
# This maps the upper half plane to the unit disk
# Note that this map has determinant 2i, so must be normalized if not using
# it for conjugating other transformations
cayley_map = Mobius(1, -1j, 1, 1j)

def unit_circle_map(u, v):
    """
    Recipe III (Indra's Pearls pp. 88-89)
    Map the unit circle to itself

    using a mobius transformation

    [u      v     ]
    [u.conj v.conj]
    """
    U = complex(u)
    V = complex(v)
    return Mobius(U, V, V.conjugate(), U.conjugate())

def unit_circle_map_cayley(mobius):
    """
    Recipe III but this time done by conjugating by a mobius transformation

    The input mobius transformation cannot be strictly loxodromic
    """
    if mobius.classify == 'loxodromic':
        raise ValueError("Cannot make unit circle map from loxodromic xform!")

    return mobius.conjugate_by(cayley_map)

def special_stretch_map(u):
    """
    This is a special case of Recipe III that takes 1 parameter

    u is real and u > 1
    """
    if u <= 1.0:
        raise ValueError("u must be > 1")
    v = math.sqrt(u * u - 1)
    return Mobius(u, v, v, u)
