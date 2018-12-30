import cmath
from mobius import Mobius

class Cline(object):
    """
    Generalized Circle in the extended complex plane

    Such circles satisfy
    |z - center| = r

    Which can be expanded to
    (z * z.conj - z * center.conj
        - z.conj * center + center * center.conj - r^2) = 0

    Upon multiplication by a real number A, we have
    A * z * z.conj + B * z + C * z.conj + D = 0

    Where
    A is any real number
    B = -A * center.conj
    C = -A * center = B.conj
    D = A * center * center.conj - A * r^2
    """
    def __init__(self, a, b, c, d):
        self.a = complex(a)
        self.b = complex(b)
        self.c = complex(c)
        self.d = complex(d)

    def __repr__(self):
        return "{} * |z|^2 + {} * z + {} * z.conj + {} = 0".format(
            self.a, self.b, self.c, self.d)

    def transform(self, mobius):
        """
        Apply a mobius transformation to the Cline

        If the cline is [A B]
                        [C D]
        in matrix form and M is another mobius transformation

        Then:

        C' = M.inv.T * C * M.inv.conj

        where .inv is the inverse mobius transformation
        .T is the transpose mobius transformation
        .conj is the mobius transformation with all the coefficients
            replaced with complex conjugates
        """
        M_inv = mobius.inv
        M_inv_T = M_inv.T
        M_inv_conj = M_inv.conj

        print(mobius, '::', M_inv, '::', M_inv_T, '::', M_inv_conj)

        # The Cline isn't actually a mobius transformation, but
        # it multiplies like one!
        C = Mobius(self.a, self.b, self.c, self.d)

        # Compute the transformed circle/line
        transformed = M_inv_T * C * M_inv_conj

        return Cline(
            transformed.a, transformed.b, transformed.c, transformed.d)

    @property
    def discriminant(self):
        """
        The discriminant determines if this Cline is a circle or line
        discriminant = det [A B] = A * D - B * C
                           [C D]
        """
        return self.a * self.d - self.b * self.c

    @property
    def classify(self):
        """
        use the discriminant to determine which type of shape this
        Cline is:

        A != 0:
            Discriminant < 0: Real Circle
            Discriminant = 0: Point Circle
            Discriminant > 0: Imaginary Circle
        A = 0:
            Discriminant < 0: Straight Line
            Discriminant = 0: Not a Circle
            Discriminant > 0: Impossible
        """
        disc = self.discriminant
        if self.a != 0:
            if disc.real < 0:
                return 'circle'
            elif disc.real == 0:
                return 'point'
            else:
                return 'imag_circle'
        else:
            if disc.real < 0:
                return 'line'
            elif disc.real == 0:
                # Not a circle or line. Not sure
                return 'not_circle'
            else:
                return 'invalid'

    @property
    def params(self):
        """
        If this is a circle, return ('circle', center, radius)
            |z - center| = radius
        If this is a point, return ('point', center)
        If this is a line, return ('line', A, B, C)
            Ax + By = C
        If this is an imaginary circle, return ('imag_circle', center, radius)
            |z - center| = radius, radius is complex
        Otherwise, return ('not_circle', None) or ('invalid', None)
        """
        cline_type = self.classify
        if cline_type == 'circle':
            center = -self.c / self.a

            # Compute the radius
            disc = self.discriminant
            radius = cmath.sqrt(-disc / self.a)
            return ('circle', center, radius)
        elif cline_type == 'point':
            center = -self.c / self.a
            return ('point', center)
        elif cline_type == 'imag_circle':
            raise NotImplementedError('imag circle params')
        elif cline_type == 'line':
            # These were derived as follows:
            # C.conj * z + C * z.conj + D = 0
            # 2 * Re(C.conj * z) = -D
            # 2 * (C.real * x + C.imag * y) = -D
            # C.real * x + C.imag * Y = -D / 2
            # which is in the form Ax + By = C
            A = self.c.real
            B = self.c.imag
            C = -self.d / 2.0
            return ('line', A, B, C)
        else:
            return (cline_type, None)

    @classmethod
    def from_circle(cls, center, radius):
        """
        Compute the 4 parameters
        """
        # Make sure the center is a complex number
        center = complex(center)
        A = 1
        B = -center.conjugate()
        C = B.conjugate()
        D = center * center.conjugate() - radius * radius
        return cls(A, B, C, D)
