from plot import *

f = symbols('f')
r = 3.4e3
c = 47e-9
abs_a = 1/sqrt(1 + (2*pi*r*c*f)**2)

'''
proof on how to hack a bode plot with log-log scaling,
so we don't need that db bullshit
'''
add_plot(abs_a, (f, 10, 1e5), label='abs(A)')
show_plots("loglog")
