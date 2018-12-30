import cmath
from enum import Enum

class Mobius(object):
    """
    Class that represents a Mobius map (a.k.a linear fractional transformation)

    Mobius maps are functions of the form
    M: Complex -> Complex
    M(z) = (a * z + b) / (c * z + d),

    where a, b, c, d and z are all complex numbers. They can also be
    represented in matrix form:

    M = [a b]    where the entries are the same as above
           [c d]
    """

    def __init__(self, a, b, c, d):
        """
        Initialize the mobius transformation. This does NOT normalize
        the parameter
        """
        self.a = complex(a)
        self.b = complex(b)
        self.c = complex(c)
        self.d = complex(d)

    def __repr__(self):
        """
        Format the mobius transform. Note that this displays 0s explicitly
        """
        # TODO: Hide 0 values
        return "({}z + {}) / ({}z + {})".format(
            self.a, self.b, self.c, self.d)

    def __call__(self, z):
        """
        Apply the mobius transformation to a point
        """
        # TODO: Check for divide by 0 error and return infinity
        return (self.a * z + self.b) / (self.c * z + self.d)

    @property
    def fixed_points(self):
        """
        return the fixed point(s) of T

        They are solutions to the quadratic equation in C[x]:

        z = M(z)

        Fix M = ((a - d) +/- sqrt((Tr M)^2 - 4)) / (2 * c)

        If there is only one fixed point, this method returns
        (Fix M, None)

        Otherwise, return
        (Fix+ M, Fix- M) where the signs match that in the quadratic formula
        """

        # Apply the quadratic formula
        top_left = self.a - self.d
        bottom = 2 * self.c
        discriminant = self.tr ** 2 - 4

        # Only 1 fixed point if the discriminant is 0
        # (happens when the transformation is parabolic)
        if discriminant == 0:
            return (top_left / bottom, None)

        # Otherwise, finish the quadratic formula
        top_right = cmath.sqrt(discriminant)

        return (
            (top_left + top_right) / bottom,
            (top_left - top_right) / bottom)

    def __mul__(self, other):
        """
        Multiply matricies together to compose mobius transformations
        [a b] * [e f] = [ae + bg  af + bh]
        [c d]   [g h]   [ce + dg  cf + dh]
        """
        a = self.a * other.a + self.b * other.c
        b = self.a * other.b + self.b * other.d
        c = self.c * other.a + self.d * other.c
        d = self.c * other.b + self.d * other.d
        return Mobius(a, b, c, d)

    @property
    def from_one(self):
        """
        Calculate M(1) = (a + b) / (c + d), the point where 1 ends up
        """
        return (self.a + self.b) / (self.c + self.d)

    @property
    def from_zero(self):
        """
        Calculate M(0) = b / d, the point where 0 ends up
        """
        return self.b / self.d

    @property
    def from_inf(self):
        """
        Calculate M(inf) = a / c, the point where infinity ends up
        """
        return self.a / self.c

    @property
    def to_one(self):
        """
        Calculate M^-1(1) = (d - b) / (a - c), the point that maps to 1
        """
        return (self.d - self.b) / (self.a - self.c)

    @property
    def to_zero(self):
        """
        Calculate M^-1(0) = - b / a, the point that maps to 0
        """
        return - self.b / self.a

    @property
    def to_inf(self):
        """
        Calculate M^-1(inf) = - d / c, the point that maps to infinity
        """
        return - self.d / self.c

    @property
    def inv(self):
        """
        Find the inverse transformation:

        M^-1 = [d -b]
               [-c a]
        """
        return Mobius(self.d, -self.b, -self.c, self.a)

    @property
    def det(self):
        """
        Compute the determinant of the matrix.

        det M = a * d - b * c
        """
        return self.a * self.d - self.b * self.c

    @property
    def normalize(self):
        """
        Normalize the matrix so it has determinant 1. This way we can
        multiply matrices together without introducing a scaling factor

        M' = M / sqrt(det M)
        """
        sdet = cmath.sqrt(self.det)
        a = self.a / sdet
        b = self.b / sdet
        c = self.c / sdet
        d = self.d / sdet
        return Mobius(a, b, c, d)

    @property
    def tr(self):
        """
        Compute the trace of the matrix

        tr M = a + d
        """
        return self.a + self.d

    @property
    def T(self):
        """
        Compute the transpose of the matrix as a new Mobius object.

        M^T = Ry(pi) * M^-1 * Ry(pi)^-1
        where Ry(pi)(z) = -1/z, a 180 degree rotation of the riemann sphere
            about the +y axis

        Note that Ry(pi)^-1 = Ry(pi)
        """
        return Mobius(self.a, self.c, self.b, self.d)

    @property
    def conj(self):
        """
        Compute the conjugate of the matrix. This is the same
        as conjugating by the map X(z) = z.conj

        M.conj = X * M * X^-1

        Note that X = X^-1
        """
        return Mobius(
            self.a.conjugate(),
            self.b.conjugate(),
            self.c.conjugate(),
            self.d.conjugate())

    @property
    def classify(self):
        """
        Classify a mobius transformation by its trace:

        tr M strictly complex: loxodromic
        |tr M| > 2: hyperbolic
        |tr M| < 2: elliptic
        otherwise: parabolic
        """
        t = self.tr
        if t.imag != 0:
            return 'loxodromic'
        elif abs(t) > 2:
            return 'hyperbolic'
        elif abs(t) < 2:
            return 'elliptic'
        else:
            return 'parabolic'
