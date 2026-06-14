from plot import *

t = symbols('t')
cx, cy = 0.6, 0
r = 0.5
add_parametric(r*cos(t) + cx, r*sin(t) + cy, (t, 0, 2*pi),
        label= "ball", color='#505050')
show_plots('geo')
