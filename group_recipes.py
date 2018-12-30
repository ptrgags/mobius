"""
Groups of transformations
These return lists of transformations including inverses.

Most of these are from Indra's Pearls by David Mumford et al.
"""
from mobius import Mobius

def make_group(*xforms):
    return list(xforms) + [xform.inv for xform in xforms]

# The Glowing Gasket of Chapter 7 fame
apollonian_gasket = make_group(
    Mobius(1, 0, -2j, 1),
    Mobius(1 - 1j, 1, 1, 1 + 1j))
