#!/usr/bin/env python
from mobius import Mobius
from cline import Cline
import mobius_recipes
import group_recipes
from flame import Flame, FlamePack

def main():
    # unit circle
    C = Cline.from_circle(1, 1)

    # Transform to the imaginary line
    K = mobius_recipes.cayley_map
    C2 = C.transform(K)

    print(C)
    print(K)
    print(C2)
    print(C2.params)

    flames = [
        Flame('ApollonianGasket', group_recipes.apollonian_gasket)
    ]
    flame_pack = FlamePack('MobiusTest', flames)
    flame_pack.save('test.flame')


if __name__ == '__main__':
    main()
