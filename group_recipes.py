"""
Groups of transformations
These return lists of transformations including inverses.

Most of these are from Indra's Pearls by David Mumford et al.
"""
from mobius import Mobius
import cmath

def make_group(*xforms):
    """
    Add inverses to a list of transformations
    """
    return list(xforms) + [xform.inv for xform in xforms]

def solve_quadratic(a, b, c):
    """
    Solve the quadratic equation returning
    (root+, root-) even if they are the same
    """
    top_left = -b
    discriminant = b * b - 4 * a * c
    bottom = 2 * a

    sol_plus = (top_left + cmath.sqrt(discriminant)) / bottom
    sol_minus = (top_left - cmath.sqrt(discriminant)) / bottom
    return (sol_plus, sol_minus)

def grandmas_recipe(trace_a, trace_b, plus_root=True):
    """
    Grandma's Special Parabolic Commutator Groups
    From Indra's Pearls p. 229

    This formula is magical, I don't quite understand it
    """
    # make sure we have complex numbers
    trace_a = complex(trace_a)
    trace_b = complex(trace_b)

    # 1 solve for Tr ab
    # t_ab = x in the equation
    # x^2 - Ta * Tb * x + Ta^2 + Tb^2 = 0
    plus, minus = solve_quadratic(
        1, -trace_a * trace_b, trace_a ** 2 + trace_b ** 2)

    # Let the caller decide which root to use. Sometimes this matters
    # when Tab is complex
    trace_ab = plus if plus_root else minus

    # Compute z0
    z0_top = (trace_ab - 2) * trace_b
    z0_bottom = trace_b * trace_ab - 2 * trace_a + 2j * trace_ab
    z0 = z0_top / z0_bottom

    # Compute the coefficients of a
    A = trace_a / 2
    B = (trace_a * trace_ab - 2 * trace_b + 4j) / ((2 * trace_ab + 4) * z0)
    C = (trace_a * trace_ab - 2 * trace_b - 4j) * z0 / (2 * trace_ab - 4)
    D = A
    a = Mobius(A, B, C, D)

    # Compute the coeffients of b
    A = (trace_b - 2j) / 2
    B = trace_b / 2
    C = B
    D = (trace_b + 2j) / 2
    b = Mobius(A, B, C, D)

    # Finally, return it as a group
    return make_group(a, b)

# The Glowing Gasket of Chapter 7 fame
apollonian_gasket = make_group(
    Mobius(1, 0, -2j, 1),
    Mobius(1 - 1j, 1, 1, 1 + 1j))
