from resistors import *
from prefixed import Float

def design1():
    delta = 0.2
    rt = design_3div(11, 13, 2.5-delta, 2.5 + delta, 0, 5, 1000)
    if rt:
        rs = scale_tuple(47000/rt[0], rt)
        print(rs)
        print(vout(13, 47000, 0, 12000, 5, 470000))
        print(vout(11, 47000, 0, 12000, 5, 470000))


def design2():
    delta = 0.15
    mid = 2.0
    rt = design_3div(11, 13, mid-delta, mid + delta, 0, 3.3, 1000)
    if rt:
        rs = scale_tuple(47000/rt[0], rt)
        # print(rs)
        ri, rss ,rdd = rs
        print(f"{ri=}, {rss=}, {rdd=}")
        ri = preferred_closest(ri)
        rss = standard_above(rss)
        rdd = standard_above(rdd)
        print(f"{ri=}, {rss=}, {rdd=}")
        print(vout3(13, ri, 0, rss, 3.3, rdd))
        print(vout3(11, ri, 0, rss, 3.3, rdd))


def print_outs(ru, rd):
    out13 = vout2(13, ru, 0, rd)
    out11 = vout2(11, ru, 0, rd)
    print(f"{out11=:.2f}, {out13=:.2f}")

def design3():
    r = design_div(0, 13, 2.4, 1000)
    s = scale_tuple(47000/r[0], r)

    serie = "E12"
    tol = 10/100

    ru = preferred_closest(s[1], serie)
    rd = preferred_closest(s[0], serie)
    ss = (rd, ru)
    print(f"{ss=}")

    print("biggest")
    print_outs(ru*(1-tol), rd*(1+tol))

    print("lowest")
    print_outs(ru*(1+tol), rd*(1-tol))

def design4():
    # ![picture](high-input.svg)
    # results = {}
    ignore =['vcc', 'vref', 'ins', 'vth', 'rth', 'A']
    vcc = 5
    vref = 2
    rf = 3300
    A = 1/2
    ins = 15/100
    ri = rf / A
    # initially rn = rp = ri

    ri = preferred_closest(ri)
    rf = preferred_closest(rf)

    # ins = common mode input scaling
    # ins = rr/(rr+ri)
    # 1/ins = 1 + ri/rr
    # (1-ins)/ins = ri/rr
    # rr/ri = ins/(1-ins)
    rr = ri*ins/(1-ins)
    rb = rf*rr/(rf-rr)

    __rr = preferred_closest(rr)
    __ins = __rr/(__rr + ri)
    __rb = rf * __rr /(rf - __rr)
    # __rb = rationalize(__rb)
    temp = preferred_closest(__rb)
    print(temp, '<->', __rb)
    # __rb = preferred_closest(rb)

    ignore.append('rr')
    ignore.append('rb')

    # rr = rationalize(rr)
    # rb = rationalize(rb)
    # rb = preferred_closest(rb)

    # print("Rf =", rf)
    # print("Ri =", ri)
    # print("Rp =", ri)
    # print("Rr =", rr) # replaced by divider
    # print("Rb =", rb) # lumped with rn

    # negative
    # res = design_div(0,5,3.71,4290)

    # now I have 10 Volts to Rn and vref to Rb
    vth = vout2(10, ri, vref, rb)
    assert vth < vcc
    # print(f"vth ({vth}) should be in the reach for vcc({vcc})")
    rth = paralell(ri, rb)
    vnd,vnu = design_div(0, vcc, vth, rth)
    # vnd,vnu = rationalize(vnd), rationalize(vnu)
    # print(f"negative div: {vnd=} {vnu=}")

    # positive
    vpd,vpu = design_div(0, vcc, vref, rr)
    # vpd, vpu = rationalize(vpd), rationalize(vpu)
    # print(f"positive div: {vpd=} {vpu=}")

    # collect results
    # results['rf'] = rf
    # results['ri'] = ri
    # results['vnd'] = vnd
    # results['vnu'] = vnu
    # results['vpd'] = vpd
    # results['vpu'] = vpu

    # print('\nrational values')
    # for name in results:
    #     r = rationalize(results[name])
    #     print(f'    {name} = {r}')

    # print('\nE24 series values:')
    # for name in results:
    #     closest = preferred_closest(results[name], "E24")
    #     print(f'    {name} = {closest}')

    print('\nResults:')
    vars = locals()
    for n in vars:
        if n not in ignore and n != 'ignore':
            print(f'{n} = {vars[n]}')


def design5():
    ignore =['i', 'j', 'x', 'y']
    #----------------------------------------------------------

    perfect_ratio = []
    min_error = 1
    min_index = -1
    for a in E12:
        for b in E12:
            pe = fabs(2*b - a) / a
            if pe < min_error:
                min_error = pe
                min_index = (a, b)
    del pe
    del a
    del b
    #----------------------------------------------------------
    print('\nResults:')
    vars = locals()
    for n in vars:
        if n not in ignore and n != 'ignore':
            print(f'{n} = {vars[n]}')


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

def design8():
    ignore =['i', 'j', 'x', 'y']
    #----------------------------------------------------------

    vcc = 5
    vref = 2
    rf = 36000
    A = 0.5
    ins = 0.15
    ri = 72000
    rb = 18000
    rr = 12000
    ins = 0.14285714285714285

    vth = vout2(10, ri, vref, rb)
    assert vth < vcc
    rth = paralell(ri, rb)
    vnd,vnu = design_div(0, vcc, vth, rth)

    # _vnd = rationalize(vnd)
    # _vnu = rationalize(vnu)
    _vnd = preferred_closest(vnd, 'E24')
    vnd_error = abs(_vnd - vnd) / vnd

    # positive
    vpd,vpu = design_div(0, vcc, vref, rr)

    # ![result](probe-up.txt)
    #----------------------------------------------------------
    print('\nResults:')
    vars = locals()
    for n in vars:
        if n not in ignore and n != 'ignore':
            print(f'{n} = {vars[n]}')

def design7():
    for a in preferred_values(0,2, 'E24'):
        for b in preferred_values(0,2, 'E24'):
            p = paralell(a,b)
            c = preferred_closest(p)
            if c == p:
                print(a, b)

if __name__ == "__main__":
    design8()
