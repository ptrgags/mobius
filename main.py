#!/usr/bin/env python
from mobius import Mobius
from cline import Cline
import mobius_recipes
import group_recipes
from flame import Flame, FlamePack

def main():
    flames = [
        Flame('ApollonianGasket', group_recipes.apollonian_gasket),
        Flame('GrandmasGasket', group_recipes.grandmas_recipe(2, 2))
    ]
    flame_pack = FlamePack('MobiusTest', flames)
    flame_pack.save('test.flame')


if __name__ == '__main__':
    main()
