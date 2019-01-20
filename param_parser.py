import json
from flame import Palette
import animation
import parametric

class ParamParser(object):
    # Which animation class to use
    ANIMATORS = {
        'grandma': animation.GrandmasAnimation
    }

    """
    Read animation parameter description from a .json file
    and turn it into a FractalAnimation
    """
    def __init__(self, fname):
        with open(fname, 'r') as f:
            self.params = json.load(f)

    @property
    def animator_type(self):
        """
        Select the right animator for this json file
        """
        animator_id = self.params['animator']
        return self.ANIMATORS[animator_id]

    @property
    def animator_params(self):
        """
        self.params['params'] but all the properties beginning with
        'curve_' are replaced with a ParametricCurve object
        and 'palette' is replaced with a Palette object
        """
        params = self.params['params']
        result = {}
        for key, value in params.items():
            if key.startswith('curve_'):
                # Construct the right parametric curve recursively
                result[key] = self.make_curve(value)
            elif key == 'palette':
                result[key] = self.make_palette(value)
            else:
                # Pass other keys through unaltered
                result[key] = value
        return result

    def make_palette(self, palette_type):
        if palette_type == 'random':
            return Palette.random()

    def make_curve(self, data):
        """
        curve = const_float                        -> ConstCurve (real)
              | [real, imag]                       -> ConstCurve (complex)
              | ["loop", curve]                    -> LoopedCurve
              | ["reverse", curve]                 -> ReverseCurve
              | ["chain", curves...]               -> CurveChain
              | ["line", start, stop]              -> LineSegment
              | ["circle", center, radius, theta0] -> ParametricCircle 
        """
        # Simple case: we have a real number which represents a constant curve
        if isinstance(data, float):
            return parametric.ConstCurve(data)

        # Otherwise, 
        curve_type = data[0]
        args = data[1:]
        if isinstance(curve_type, float):
            val = self.parse_complex(data)
            return parametric.ConstCurve(val)
        elif curve_type == 'loop':
            [curve] = args
            return parametric.LoopedCurve(self.make_curve(curve))
        elif curve_type == 'reverse':
            [curve] = args
            return parametric.ReverseCurve(self.make_curve(curve))
        elif curve_type == 'chain':
            curves = [self.make_curve(curve) for curve in args]
            return parametric.CurveChain(curves)
        elif curve_type == 'line':
            start_val, end_val = args
            start = self.parse_complex(start_val)
            end = self.parse_complex(end_val)
            return parametric.LineSegment(start, end)
        elif curve_type == 'circle':
            return self.parse_circle(args)
        else:
            raise ValueError("{} is not a valid curve!".format(data))

    def parse_circle(self, args):
        """
        Handle the arguments for a circle
        """
        center_coords, radius, theta0, freq = args
        center = self.parse_complex(center_coords)
        return parametric.ParametricCircle(center, radius, theta0, freq) 

    def parse_complex(self, data):
        """
        Turn [real, imag] -> a complex object
        """
        if isinstance(data, float):
            # real number
            return data
        elif len(data) == 2:
            # Complex number
            return complex(*data)
        else:
            raise ValueError("{} not in the form [real, imag]".format(data)) 

    def make_animation(self):
        """
        Make and save an animation
        """
        # Set up the animation
        anim = self.animator_type(**self.animator_params)
        
        # Make the animation
        fname = "output/{}".format(self.params['fname'])
        pack_name = self.params['pack_name']
        anim.make_animation(pack_name, fname)

