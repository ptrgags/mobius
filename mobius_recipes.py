"""
Recipes from the book Indra's Pearls by David Mumford et al.
plus some of my own variations
"""
from mobius import Mobius
import basic_maps

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

def cross_ratio_map(p, q, r):
    """
    From Indra's Pearls Project 3.2
    The map
            (z - P)(Q - R)
    S(z) =  --------------
            (z - R)(Q - P)

    Maps P -> 0
         Q -> 1
         R -> infinity
    """
    P = complex(P)
    Q = complex(Q)
    R = complex(R)

    a = Q - R
    b = Q - P
    return Mobius(a, -P * a, b, -R * b).normalize

def circle_inversion(center, radius, z):
    """
    Invert a point in an arbitrary circle

    Formula:
    C_p_r = T_p * S_r * U * S_r^-1 * T_p^-1

    Where T_p is a translation to the center of the circle
          S_r is a scaling by the radius
          U is a unit circle inversion
    """
    translate = basic_maps.translate(center)
    scale = basic_maps.scale(radius)
    conj_matrix = translate * scale

    # since unit_circle_inversion is not a Mobius object, have to do this
    # manually
    normalized = conj_matrix.inv(z)
    inverted = basic_maps.unit_circle_inversion(normalized)
    return conj_matrix * inverted

def pair_circles(
        center1, radius1, center2, radius2, circle_map=basic_maps.identity):
    """
    Pair 2 circles (C1, r1) and (C2, r2)
    with the following chain of events, including an optional
    map that takes the unit circle to the unit circle:

    M' = T_C2 * S_r2 * Rx_180 * M * S_r1^-1 * T_C1^-1
    Where T stands for translation
          S stands for scaling
          Rx_180 is the map 1/z (180 degree rotation of riemann sphere about x)
          M is an optional map from the unit disk to the unit disk
    """
    T2 = basic_maps.translate(center2)
    S2 = basic_maps.scale(radius2)
    Rx_180 = basic_maps.reciprocal
    S1 = basic_maps.scale(radius1).inv
    T1 = basic_maps.translate(center1).inv
    return T2 * S2 * Rx_180 * circle_map * S1 * T1

def find_mobius_xform(p1, q1, r1, p2, q2, r2):
    """
    Alluded to in Indra's Pearls Project 3.2
    Find the unique mobius map that maps
        P -> P'
        Q -> Q'
        R -> R'

    Using the formula
    M = T^-1 S
    where S is the cross-ratio map for P, Q, R and
    T is the cross-ratio map for P', Q' and R'
    """
    S = cross_ratio_map(p1, q1, r1)
    T = cross_ratio_map(p2, q2, r2)
    return T.inv * S
