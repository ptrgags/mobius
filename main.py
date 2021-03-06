#!/usr/bin/env python
import sys

from mobius import Mobius
from cline import Cline
import mobius_recipes
import group_recipes
from flame import Flame, FlamePack, Palette
import animation

# I want these curves easily accessible
from parametric import *
import param_parser

def const_curve(val):
    """
    "Curve" that doesn't move in space
    """
    return lambda t: complex(val)

def explore_trace_space(trace_a_curve, trace_b_curve, num_steps):
    """
    Use 2 parametric curves to explore the trace space, that is, the
    space of values for two complex traces t_a and t_b.

    trace_a_curve and trace_b_curve are any two parametric curves
    of the form f: [0, 1] -> C where C represents the complex numbers

    dt is the step size within that interval
    """
    dt = 1.0 / num_steps
    for i in range(num_steps):
        t = i * dt
        trace_a = trace_a_curve(t)
        trace_b = trace_b_curve(t)
        yield (trace_a, trace_b)

# Examples given in the textbook
TEXTBOOK_EXAMPLES = FlamePack('TextbookExamples', [
    Flame('ApollonianGasket', group_recipes.apollonian_gasket),
    Flame('GrandmasGasket', group_recipes.grandmas_recipe(
        2, 2, False)),
    Flame('Snails', group_recipes.grandmas_recipe(
        1.87+.1j, 1.87-.1j, True)),
    Flame('Spirals', group_recipes.grandmas_recipe(
        1.91 + .05j, 3, False)),
    Flame('DoubleDoubleSpirals', group_recipes.grandmas_recipe(
        1.91 + .05j, 1.91 + 0.05j, True)),
    Flame('CthulhuSleeps', group_recipes.grandmas_recipe(
        1.887 + .05j, 2, False))
])

def gasket_explosion():
    f_a = const_curve(2)
    f_b = lambda t: 2 - 2 * t
    steps = 100
    vals = list(explore_trace_space(f_a, f_b, steps))
    palette = Palette.random()
    zoom = 1.0
    size = "500 500"
    flames = [
        Flame(
            'Gasket_{}'.format(i),
            group_recipes.grandmas_recipe(t_a, t_b, False),
            palette=palette,
            zoom=zoom,
            size=size)
        for i, (t_a, t_b) in enumerate(vals)]
    pack = FlamePack('GasketExplosion', flames)
    pack.save('output/gasket_explosion.flame')

def still_not_spirals():
    f_a = lambda t: 2 - 2 * t
    f_b = lambda t: 2 + 1j - t * 1j
    steps = 100
    vals = list(explore_trace_space(f_a, f_b, steps))
    palette = Palette.random()
    zoom = 0.5
    size = "500 500"
    flames = [
        Flame(
            'Spirals_{}'.format(i),
            group_recipes.grandmas_recipe(t_a, t_b, False),
            palette=palette,
            zoom=zoom,
            size=size)
        for i, (t_a, t_b) in enumerate(vals)]
    pack = FlamePack('Spirals', flames)
    pack.save('output/spirals.flame')

def gasket_explosion():
    """
    Use with GrandmasAnimation
    """
    return {
        'num_frames': 200,
        'palette': Palette.random(),
        'curve_zoom': ConstCurve(1.0),
        'curve_trace_a': ConstCurve(2.0),
        'plus_root': False,
        'curve_trace_b': LoopedCurve(LineSegment(2.0, 0.01))
    }

def old_main():
    anim = animation.GrandmasAnimation(**gasket_explosion())
    anim.make_animation('GasketExplosion', 'output/gasket_explosion.flame') 

def main():
    fname = sys.argv[1]
    parser = param_parser.ParamParser(fname) 
    parser.make_animation()
    

if __name__ == '__main__':
    main()
