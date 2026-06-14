#!/bin/env python3

from sympy import plot, plot_parametric, symbols, sqrt, cos, sin
from matplotlib import pyplot as plt
from math import pi

def add_parametric(xt, yt, range, **kwargs):
    p = plot_parametric(xt, yt, range, show=False)
    pts = p[0].get_points()
    plt.plot(pts[0], pts[1], **kwargs)

def add_plot(f, range, **kwargs):
    p = plot(f, range, show=False)
    xs,ys = p[0].get_points()
    mx, my = max(xs), max(ys)
    plt.plot(xs, ys, **kwargs)

def show_plots(aspect_equal = False):
    plt.legend()
    # plt.title("")
    if aspect_equal:
        plt.gca().set_aspect('equal')

    # plt.grid(True, which='both')
    # plt.axhline(y=0, color='k')
    # plt.axvline(x=0, color='k')

    plt.gca().spines[['left', 'bottom']].set_position('zero')
    plt.gca().spines[['top', 'right']].set_visible(False)
    # plt.savefig("out.png", dpi=600, transparent=True)
    plt.savefig("out.svg", dpi=600, transparent=True)
    # plt.show()

plt.style.use('dark_background')

#============================ PLAYGROUND ======================================

t = symbols('t')

rout = 150
T = 1
a1 = 1
a2 = 1.2
w = 2*pi / T
phi = 0
rl = t
tmax = 1.5 * T

timespan = (t,0,tmax)
add_plot(a1*sin(w*t + phi), timespan, label='sin')
add_plot(a2*cos(w*t + phi), timespan, label='cos')
show_plots()


# cx, cy = 0.6, 0
# r = 0.5
# add_parametric(r*cos(t) + cx, r*sin(t) + cy, (t, 0, 2*pi),
#         label= "ball", color='#505050')

# show_plots(True)