"""
Utilities for defining parametric functions
"""
import math
import cmath

class ParametricCurve(object):
    """
    Lightweight wrapper around a function from
    [0.0, 1.0] -> any
    """
    def __init__(self, func):
        self.func = func

    def __call__(self, t):
        return self.func(t)

class ReverseCurve(ParametricCurve):
    """
    Like ParametricCurve, but parameterized backwards
    """
    def __init__(self, curve):
        self.curve = curve

    def __call__(self, t):
        return self.curve(1.0 - t)

class ConstCurve(ParametricCurve):
    """
    a "Curve" which returns the same value regardless of time
    """
    def __init__(self, x):
        self.val = x

    def __call__(self, t):
        return self.val

class LineSegment(ParametricCurve):
    """
    Interpolate between two points
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __call__(self, t):
        return (1.0 - t) * self.start + t * self.end

class ParametricCircle(ParametricCurve):
    """
    Parametric circle

    This always returns a complex number
    """
    def __init__(self, center, radius, theta0, frequency):
        self.center = center
        self.radius = radius
        self.theta0 = theta0
        self.freq = frequency

    def __call__(self, t):
        theta = 2 * cmath.pi * self.freq * t + self.theta0
        return self.center + self.radius * cmath.exp(1j * theta)

class CurveChain(ParametricCurve):
    """
    Chain multiple curves together into one longer animation
    """
    def __init__(self, funcs):
        self.funcs = funcs

    def __call__(self, t): 
        n = len(self.funcs)
        func_index = int(math.floor(n * t))
        func_val = math.fmod(n * t, 1.0)

        if t == 1.0:
            # Technically this winds up in the (n + 1)-th bucket, 
            # but really we want the end of the last bucket anyway
            return self.funcs[-1](1.0)
        else:
            return self.funcs[func_index](func_val)

class LoopedCurve(CurveChain):
    """
    Use a function forwards for the first half of the animation and
    backwards for the second half
    """
    def __init__(self, func):
        fwd = ParametricCurve(func)
        bwd = ReverseCurve(func)
        super(LoopedCurve, self).__init__([fwd, bwd])

    @classmethod
    def looped_curve(cls, func):
        """
        Loop the animation. Remember that you need to double the frame
        count when passing to an Animation!
        """
        return cls([fwd, bwd])
