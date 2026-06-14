from plot import *

x = symbols('x')

add_plot(-x**2, (x, -2, 2), label='-x**2')
add_plot(exp(x), (x, -2, 2), label='exp(x)')
show_plots()
