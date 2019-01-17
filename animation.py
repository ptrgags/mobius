import group_recipes
from flame import Flame, FlamePack

class FractalAnimation(object):
    """
    Utility for setting up an animation as a flame pack for Chaotica

    This is an abstract class
    """
    SIZE = "500 500"
    def __init__(self, num_frames, palette, zoom_curve):
        """
        Set up generic animation parameters
        num_frames: number of frames in the animation. if you are using a
        loo
        """
        self.num_frames = num_frames
        self.palette = palette
        self.zoom_curve = zoom_curve

    def make_animation(self, pack_name, fname):
        flames = list(self.make_flames())
        pack = FlamePack(pack_name, flames)
        pack.save(fname)
    
    def make_flames(self):
        raise NotImplementedError("Implement in subclass!")

class GrandmasAnimation(FractalAnimation):
    """
    Animation using "Grandma's recipe" from the book Indra's Pearls
    """
    def __init__(self, trace_a_curve, trace_b_curve, plus_root=True, **kwargs):
        """
        Two new parameters:
        trace_a_curve - a ParametricCurve of [0, 1] -> Complex for trace a
        trace_b_curve - a ParametricCurve of [0, 1] -> Complex for trace b

        plus_root: At one point in Grandma's recipe there's a choice of
        picking a positive sqare root or a negative one. Select one for
        the entire animation to keep things simple
        """
        super(GrandmasAnimation, self).__init__(**kwargs)
        self.trace_a_curve = trace_a_curve
        self.trace_b_curve = trace_b_curve
        self.plus_root = plus_root

    def make_flames(self):
        for i, zoom, trace_a, trace_b in self.animate_params():
            flame_name = "frame_{}_zoom_{:.3f}_tr_a_{}_tr_b_{}".format(
                i, zoom, trace_a, trace_b)
            xforms = group_recipes.grandmas_recipe(
                trace_a, trace_b, self.plus_root)
            yield Flame(
                flame_name,
                xforms,
                palette=self.palette,
                zoom=zoom,
                size=self.SIZE)

    def animate_params(self):
        """
        Generate the parameters
        (frame, zoom, trace_a, trace_b) by mapping thee number of
        frames onto the interval [0.0, 1.0] and passing it into the
        parametric curves
        """
        dt = 1.0 / self.num_frames
        for i in range(self.num_frames):
            t = i * dt
            trace_a = self.trace_a_curve(t)
            trace_b = self.trace_b_curve(t)
            zoom = self.zoom_curve(t)
            yield (i, zoom, trace_a, trace_b)

    def format_complex(self, z): 
        """
        Format a complex number for use in a filename
        """
        return "{:.3f}_{:.3f}i".format(z.real, z.imag)
