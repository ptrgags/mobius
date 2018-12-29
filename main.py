#!/usr/bin/env python
from mobius_xform import Mobius

def main():
    a = Mobius(1, 0, 0, 1)
    b = Mobius(1j, 2, 2j, 1)

    A = a.inv
    B = b.inv

    print('a', a, a.classify)
    print('A', A, A.classify)
    print('b', b, b.classify)
    print('B', B, b.classify)

if __name__ == '__main__':
    main()
