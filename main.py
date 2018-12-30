#!/usr/bin/env python
from mobius import Mobius
from cline import Cline
import mobius_recipes
import group_recipes
from flame import Flame, FlamePack

def main():
    flames = [
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
    ]
    flame_pack = FlamePack('MobiusTest', flames)
    flame_pack.save('test.flame')


if __name__ == '__main__':
    main()
