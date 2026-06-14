'''
for Ru = "infinity"
A = Vpl/Vph
Rb = R/A
Rf = R/(1-A)
Vb = Vpl/A = Vph
'''

from resistors import *

def toggle_out(Vpl, Vph, Vcc, R):
    ''' Toggle a output from Vpl to Vph
*                  Vcc o
*                      |
*                     [ ] Ru
*         _T_    Rf    |
*      ---o o---[  ]---*-------o Vp  [Vpl .. Vph]
*    _|_               |
*    GND              [ ] Rd
*                     _|_
*                     GND
*
* Returns (Rf, Rd, Ru)
    '''
    # R is the thevenin equivalent @ Vp when
    # button is pressed
    A = Vpl/Vph
    Rb = R/A
    Rf = R/(1-A)
    Rd, Ru = design_div(0, Vcc, Vph, Rb)
    return (Rf, Rd, Ru)


if __name__ == "__main__":
    ideal = toggle_out(1.1,4,5,1000)
    comercial = tuple(get_series_closest(r) for r in ideal)
    ri, rd, ru = comercial
    Vph = vout3(0, ri, 0, rd, 5, ru)
    Vpl = vout2(5, ru, 0 , rd)
    print(f"{Vpl=:.2f}, {Vph=:.2f}")
    print(comercial)