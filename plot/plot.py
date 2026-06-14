#!/bin/env python3

from sympy import plot, plot_parametric, symbols, sqrt, cos, sin, log, exp
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


def show_plots(mode = 'func'):
    plt.legend()
    # plt.title("")
    if mode == 'func':
        plt.gca().spines[['left', 'bottom']].set_position('zero')
        plt.gca().spines[['top', 'right']].set_visible(False)
    
    # geometric
    if mode == 'geo':
        plt.gca().set_aspect('equal')

    # plt.grid(True, which='both')
    # plt.axhline(y=0, color='k')
    # plt.axvline(x=0, color='k')

    # function plot

    # bode plot
    if mode == 'loglog':
        plt.gca().spines[['top', 'right']].set_visible(False)
        plt.gca().set_xscale('log')
        plt.gca().set_yscale('log')

    plt.savefig("out.svg", dpi=600, transparent=True)
    # plt.show()

plt.style.use('dark_background')
