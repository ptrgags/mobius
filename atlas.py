#!/usr/bin/env python
from mobius import Mobius
import mobius_recipes
import group_recipes
from flame import Flame, FlamePack, Palette

# This determines the size of the grid. This is a 4D grid, so be very
# careful, the space complexity is O(R^4)
RADIUS = 4

def make_flame(trace_a, trace_b, plus_root=False):
    """
    Make a flame in a standard format
    """
    return Flame(
        'Grandma_a_{}_b_{}'.format(trace_a, trace_b),
        group_recipes.grandmas_recipe(trace_a, trace_b, plus_root),
        zoom=0.5,
        size="500 500")

def a_then_b(lattice_points):
    """
    Iterate with trace_a as the slower outer loop and trace_b as the faster
    inner loop
    """
    for trace_a in lattice_points:
        for trace_b in lattice_points:
            yield (trace_a, trace_b)

def b_then_a(lattice_points):
    """
    Same as the above, but now trace_b is the slower, outer loop
    """
    for trace_b in lattice_points:
        for trace_a in lattice_points:
            yield (trace_a, trace_b)


def make_atlas(outer_loop_a=True, plus_root=False):
    # Generate gaussian integers (complex numbers with integer coordinates)
    # in a square centered around the origin
    int_range = range(-RADIUS, RADIUS + 1)
    lattice_points = [
        complex(i, j) 
        for i in int_range 
        for j in int_range]

    # Select settings
    loop_order = a_then_b if outer_loop_a else b_then_a
    order = 'ab' if outer_loop_a else 'ba'
    root = 'plus' if plus_root else 'minus'

    print("-------------------------")
    print("Making atlas radius {}, order {}, root {}".format(
        RADIUS, order, root)) 

    # Generate fractal settings for all of the combinations
    # Yes, all (2 * RADIUS + 1)^4 of them O.o
    flames = []
    invalid_count = 0
    for trace_a, trace_b in loop_order(lattice_points):
        try:
            flame = make_flame(trace_a, trace_b, plus_root)
            flames.append(flame)
        except ZeroDivisionError as e:
            invalid_count += 1
            msg = "Divide by zero at Ta = {}, Tb = {}, sum = {}, diff = {}"  
            print(msg.format(
                trace_a, trace_b, trace_a + trace_b, trace_a - trace_b))
    print("invalid count: {}".format(invalid_count))

    # generate one *very* big .flame file
    pack = FlamePack('Atlas', flames)
    pack.save('output/atlas_{}_{}_{}_root.flame'.format(RADIUS, order, root))


if __name__ == '__main__':
    make_atlas(False, False)
    make_atlas(False, True)
    make_atlas(True, False)
    make_atlas(True, True)
