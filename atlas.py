#!/usr/bin/env python
from mobius import Mobius
import mobius_recipes
import group_recipes
from flame import Flame, FlamePack, Palette

# This determines the size of the grid. This is a 4D grid, so be very
# careful, the space complexity is O(R^4)
RADIUS = 4

def main():
    # Generate gaussian integers (complex numbers with integer coordinates)
    # in a square centered around the origin
    int_range = range(-RADIUS, RADIUS + 1)
    lattice_points = [
        complex(i, j) 
        for i in int_range 
        for j in int_range]

    # Generate fractal settings for all of the combinations
    # Yes, all (2 * RADIUS + 1)^4 of them O.o
    flames = []
    invalid_count = 0
    for trace_a in lattice_points:
        for trace_b in lattice_points:
            try:
                flame = Flame(
                    'Grandma_a_{}_b_{}'.format(trace_a, trace_b), 
                    group_recipes.grandmas_recipe(trace_a, trace_b, False),
                    zoom=0.5,
                    size="500 500")
                flames.append(flame)
            except ZeroDivisionError as e:
                invalid_count += 1
                print("Divide by zero at Ta = {}, Tb = {}, sum = {}, diff = {}".format(
                    trace_a, trace_b, trace_a + trace_b, trace_a - trace_b))
    print("invalid count: {}".format(invalid_count))

    # generate one *very* big .flame file
    pack = FlamePack('Atlas', flames)
    pack.save('output/atlas_{}.flame'.format(RADIUS))


if __name__ == '__main__':
    main()
