#!/usr/bin/env python

def f(x):
    icount=-500000000
    while icount < 500000000:
        x*x
        icount+=1

if __name__ == '__main__':
    f(3.3)

