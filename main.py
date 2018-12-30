#!/usr/bin/env python
from mobius_xform import Mobius
from cline import Cline

def main():
    # unit circle
    C = Cline.from_circle(0, 1)

    # Translate 2 to the right
    M = Mobius(1, 2, 0, 1)

    C2 = C.transform(M)

    print(C)
    print(C.params)
    print(M)
    print(C2)
    print(C2.params)


if __name__ == '__main__':
    main()
