# vim: ft=python

from fractions import gcd
from collections import deque
from itertools import islice

PX_PER_FRAME = 100004

def consume(it, n):
    deque(islice(it, n), maxlen=0)

def lcm(a, b):
    try:
        return a * b // gcd(a, b)
    except ZeroDivisionError:
        return 0

def gcd_grid(w, h, do_lcm=False):
    background(0)
    max_hw = max(h, w)
    gcdf = gcd if not do_lcm else lcm
    for x in xrange(w):
        for y in xrange(h):
            pushMatrix()
            noStroke()
            colorMode(HSB, 255, 255, 255)
            fill(gcdf(x, y) * 255.0 / (max_hw if not do_lcm else h * w),
                 255, 255)
            scale(float(width) / max_hw, float(height) / max_hw)
            rect(x, y, 1, 1)
            popMatrix()
            yield

def setup():
    global gridsize, is_lcm, draw_generator
    size(1024, 1024)
    gridsize = 8
    is_lcm = False
    draw_generator = gcd_grid(gridsize, gridsize, do_lcm=is_lcm)

def draw():
    consume(draw_generator, PX_PER_FRAME)

def keyPressed():
    global gridsize, is_lcm, draw_generator
    if 0 <= keyCode - ord('0') <= 9:
        gridsize = 8 << (keyCode - ord('0'))
    elif keyCode == UP:
        gridsize <<= 1
    elif keyCode == DOWN:
        gridsize >>= 1
    elif keyCode == ord(' '):
        is_lcm ^= 1
    
    draw_generator = gcd_grid(gridsize, gridsize, do_lcm=is_lcm)
