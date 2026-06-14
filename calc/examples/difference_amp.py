from resistors import *
from prefixed import Float

'''
## battery circuit

input range: 9.8 - 13.2

ref = 2v

map the range from 10 to 14 to the range from 2 to 4

![schematic](high-input.svg)
'''

def design_difference_amplifier():
    ignore =['vcc', 'vref', 'A', 'ins' , '_ins']
    #----------------------------------------------------------

    # set parameters here
    vcc = 5
    vref = 2
    rf = 10000
    A = 1/2
    ins = 13.5/100

    rf = preferred_closest(rf, 'E24')
    ri = rf / A

    assert error_to_standard(ri, 'E24') < 0.01
    ri = preferred_closest(ri, 'E24')

    # ins = rr/(rr+ri)
    # rr = parallel(rf, rb)
    rr_d = ri*ins/(1-ins)
    rb_d = rf*rr_d/(rf-rr_d)


    # _rb = preferred_closest(rb, 'E24')
    # _rb = find_sum(rb)[0]
    # _rb  = preferred_closest(rb, 'E24')

    # TODO: how to choose rb?
    # rb=4300 # worked
    # rb=5600 # worked
    # rb=7500 # worked

    found = False
    for rb in preferred_values(2,4, serie='E24'):

        _rr = paralell(rf, rb)
        _ins = _rr / (_rr + ri)
        # __rr = find_sum(_rr)[0]
        rr = preferred_closest(_rr, 'E24')
        _rr_error = error_to_standard(_rr, 'E24')
        
        if not (_ins < 20/100 and _ins > 10/100):
            # print('invalid ins')
            continue

        if _rr_error > 0.01:
            # print('big error on rr')
            continue

        found = True
        break

    if not found:
        print("no solution found")
        return

    del found
    del _rr
    del _rr_error
    del rr_d
    del rb_d

    #----------------------------------------------------------
    print('\nResults:')
    vars = locals()
    for n in vars:
        if n not in ignore and n != 'ignore':
            if n[0] == 'r':
                print(f'{n:5} = {Float(vars[n]):.1h}')    
            else:
                print(f'{n:5} = {vars[n]}')    

if __name__ == '__main__':
    design_difference_amplifier()
