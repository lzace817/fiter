from resistors import *
from prefixed import Float

'''
## histeresys circuit

non-inverting

suply: 5V
vtl = 2.5V
vth = 3.5V

Vth = ((Ri+Rf)*Vref - Ri*Vol)/Rf
Vtl = ((Ri+Rf)*Vref - Ri*Voh)/Rf
HYST = Vth - Vtl
HYST = (Voh-Vol)*Ri/Rf
'''

def design_comparator():
    ignore =['vcc', 'vtl', 'vth', '_rg', '_ri' , 'found', 'simple_mode', 'x', 'e', 's']
    #----------------------------------------------------------

    # set parameters here
    vcc = 5
    vtl = 2.5
    vth = 3.5
    vol = 0.2
    rp = 470

    rf = 10000
    rip = (vth - vtl)/(vcc - 0)*rf

    simple_mode = False
    if simple_mode:
        vref = vth * rf/(rip + rf)
    else:
        vref = (vth * rf + rip*vol)/(rip + rf)
    # x = ((ri + rf) * vref - ri * vcc) / rf
    # y =  ((ri + rf) * vref - ri * 0) / rf
    
    rg, rin = design_div(0, vcc, vref, 1000)
    found = False
    for x in preferred_values(2,3):
        s = x/rin
        rg, rin = s*rg, s*rin
        e = error_to_standard(rg)
        if e < 0.01:
            rg = preferred_closest(rg)
            found = True
            break
    if not found:
        print('no solution found')
        return


'''
vtl = (rf*vref + rr*vol)/(rr+rf)
vth = (rf*vref + rr*Voh)/(rr+rf)
HYST = vth - vtl
HYST = (Voh - vol)*rr/(rr+rf)
'''
def design_inv_comp():
    ignore =['vcc', '_rg', '_ri' , 'found', 'simple_mode', 'x', 's']
    #----------------------------------------------------------

    # set parameters here
    vcc = 3.7
    vtl = 50e-3
    vth = 200e-3
    rp = 470
    eseries = 'E12'
    # eseries = 'E24'

    vol = 0.2
    voh = vcc


    # rf = 12000
    # found = False
    # for rf in preferred_values(2, 4, eseries):
    rf = 15e3
    rf = preferred_closest(rf, eseries)
    A = (vth - vtl)/(voh - vol)
    # rf = rth/A
    _rr = rf * A /(1-A)

    # vref1 = (vth * (rf + _rr) - _rr*voh)/rf
    vref = (vtl * (rf + _rr) - _rr*vol)/rf

    rg, rv = design_div(0, vcc, vref, _rr)

    # eg = error_to_standard(rg, eseries)
    # ev = error_to_standard(rv, eseries)
    rg = preferred_closest(rg, eseries)
    rv = preferred_closest(rv, eseries)
    rr = paralell(rg, rv)

    vref = vcc*rg/(rg+rv)
    vtl_ = (rf*vref + rr*vol)/(rr+rf)
    vth = (rf*vref + rr*voh)/(rr+rf)
    # print(rationalize(vtl_))
    e = abs(vtl_ - vtl) / vtl
    # if e < 0.01:
    #     found = True
    #     break


    # if not found:
    #     print('not found')
    #     return

    #----------------------------------------------------------
    print('\nResults:')
    vars = locals()
    for n in vars:
        if n not in ignore and n != 'ignore':
            if n[0] == 'r':
                print(f'{n:5} = {Float(vars[n]):.2h}')    
            else:
                print(f'{n:5} = {vars[n]}')    

if __name__ == '__main__':
    design_inv_comp()
