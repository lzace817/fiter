from plot import *

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
