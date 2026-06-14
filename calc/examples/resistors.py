from math import *

'''
A = Rd/(Rd+Ru)
Rth = Rd || Ru
Rd = Rth/(1-A)
Ru = Rth/A
Vo = A*Vi + (1-A)*Vx

// translator
A = (VoH - VoL)/(ViH - ViL)
Vx = (VoL - A*ViL)/(1 - A)

// another divisor
bindings: Rth = Rd
constrain: Vx = Vdd*A + (1-A)*Vss
A = (Vx - Vss)/(Vdd-Vss)
Rd = Rth/(1-A)
Ru = Rth/A
'''

def design_div(vss, vdd, vx, rth):
    '''thevening equivalent divisor
                           vdd o--
                                  |
                                 [ ] Ru
                                  |
    Vx o--[Rth]--o x   =>         *---o x
                                  |
                                 [ ] Rd
                                  |
                           Vss o--
    Returns (Rd, Ru)
    '''
    A = (vx - vss)/(vdd - vss)
    rd = rth/(1-A)
    ru = rth/A
    return (rd, ru)

def design_3div(vil, vih, vol, voh, vss, vdd, rth):
    ''' input -> output voltage transform
*            vdd o
*                |
*               [ ] Rdd
*         Ri     |
*  Vi o--[  ]----*------o Vo
*                |
*               [ ] Rss
*                |
*            vss o
*
* Returns (Ri, Rss, Rdd)
    '''
    # A = (VoH - VoL)/(ViH - ViL)
    A = (voh - vol)/(vih - vil)
    if A <= 0:
        print("ERROR: need some kind of inversion")
        return None
    if A >= 1:
        print("ERROR: need amplification")
        return None
    ri = rth / A

    vx = (vol - A*vil)/(1-A)

    if not (vss <= vx and vx <= vdd):
        print(f"ERROR: {vx=} is not in [{vss}..{vdd}]")
        return None

    print(f"{vx=}")
    Rss, Rdd = design_div(vss, vdd, vx, rth/(1-A))
    return (ri, Rss, Rdd)

# def scale_tuple(s, t):
#     return tuple(s*c for c in t)

def vout3(v1, r1, v2, r2, v3, r3):
    return (v1/r1 + v2/r2 + v3/r3)/(1/r1 + 1/r2 + 1/r3)
# rt = design_3div(0,5,1,3,47000)
# rs = scale_tuple(47000/rt[0], rt)

def vout2(v1, r1, v2, r2):
    return (v1/r1 + v2/r2)/(1/r1 + 1/r2)

E24 = [
    10,	11,	12,	13,	15,	16,
    18,	20,	22,	24,	27,	30,
    33,	36,	39,	43,	47,	51,
    56,	62,	68,	75,	82,	91,
]

#[10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
E12 = E24[0::2]

# TODO: should 'preferred_closest' also return the relative error? @error-closest
def preferred_closest(v, serie="E12"):
    down, up = preferred_range(v, serie)
    if v - down < up - v:
        return down
    else:
        return up

def preferred_bellow(v, serie="E12"):
    low, high = preferred_range(v, serie)
    return low

def preferred_above(v, serie="E12"):
    low, high = preferred_range(v, serie)
    return high

def preferred_range(v, serie="E12"):
    if serie == "E24":
        step = 1
    elif serie == "E12":
        step = 2
    else:
        raise ValueError(f"invalid serie {serie}")
    power = floor(log10(v))
    m = v/10**power
    idown = 0
    iup = 0
    # print(m)
    while (iup < 24 and E24[iup] < m*10):
        idown = iup
        iup += step
    # index = index % 24
    power -= 1
    down = E24[(idown)%24]*10**power
    if iup == 24:
        up = 10**(power+2)
    else:
        up = E24[iup]*10**power

    # print(f"{v=}, {index=}, {down=}, {up}")
    assert(down <= v and v <= up)
    return (down, up)

# @error-closest
def error_to_standard(v, serie = 'E12'):
    s = preferred_closest(v, serie)
    e = abs(s - v) / v
    if e < 1e-4:
        return 0
    return e

def preferred_values(dec_ini, dec_end, serie = 'E12'):
    if serie == "E24":
        vals = E24
    elif serie == "E12":
        vals = E12
    else:
        raise ValueError(f"invalid serie {serie}")
    # list all series value in range
    for p in range(dec_ini, dec_end):
        for m in vals:
            yield m*10**p

def series(ra,rb):
    '''Returns req'''
    return ra+rb

def paralell(ra,rb):
    '''Returns req'''
    return ra*rb/(ra+rb)

class Rat:
    def __init__(self, int_part, num, den):
        self.int_part = int_part
        self.num = num
        self.den = den

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            sn = self.int_part*self.den + self.num
            sd = self.den

            on = other.int_part*other.den + other.num
            od = other.den

            return sn * od == on * sd
        else:
            return False

    def __repr__(self):
        if self.int_part:
            return f"{self.int_part}+{self.num}/{self.den}"
        else:
            return f"{self.num}/{self.den}"

def find_series2(v, serie='E12'):
    '''find equivalent to a series of 2 preferred values'''
    e = 1
    # vals = {}
    best = (-1,e,)
    for v1 in preferred_values(2, 5, serie):
        for v2 in preferred_values(2, 5, serie):
            s = v1+v2
            # vals[v1+v2] = (v1,v2)
            e = abs(v-s)/v
            if e < best[1]:
                best = (s, e, v1, v2)
    return best

'''
# rationalize derivation

a0 + 1/a1

r0 = a0

r1 = (a0*(a1+x) + 1) / (a1+x)
= (a0 * a1 * xd + a0 * xn + xd) / (a1 * xd + xn)
= (xd * (a0 * a1 + 1) + xn * (a0)) / (xd * a1 + xn * 1)

xn1/xd1 = 1/(a2 + y) = xd2/(a2 * xd2 + xn2)


xn[i] = xd[i+1]
xd[i] = a[i+1] * xd[i+1] + xn[i+1]


r = (a * xn[i] + b * xd[i])/(c * xn[i] + d * xd[i])
= (a * xd[i+1] + b * a[i+1] * xd[i+1] + b * xn[i+1]) / (c * xd[i+1] + d * a[i+1] * xd[i+1] + d * xn[i+1])
= ({b} * xn[i+1] + {a + b * a[i+1]} * xd[i+1])/({d} * xn[i+1] + {c + d * a[i+1]} * xd[i+1])

a[i+1] = b[i]
b[i+1] = a[i] + b[i] * v[i+1]
c[i+1] = d[i]
d[i+1] = c[i] + d[i] * v[i+1]


r2 = a0 + 1/(a1 + 1/a2)
= a0 + 1/((a1*a2 + 1)/a2)
= a0 + a2/(a1*a2 + 1)
= (a0*a1*a2 + a0 + a2)/(a1*a2 + 1)

initialization:
r[0] = v[0]
r[1] = (v[0]*v[1] + 1) / v[1]

r[1] = (a[1] * xn[1] + b[1] * xd[1]) / (c[1] * xn[1] + d[1] * xd[1]) for xn = 0 and xd = 1
= b[1]/d[1]
...
b[1] = v[0]*v[1] + 1 = a[0] + b[0] * v[1]
d[1] = v[1] = c[0] + d[0] * v[1]

a[0] = 1
b[0] = v[0] = a[-] + b[-] * v[0]
c[0] = 0
d[0] = 1 = c[-] + d[-] * v[0]

a[-] = 0
b[-] = 1
c[-] = 1
d[-] = 0

we can compute sequentially with:
    t = a
    a = b
    b = t + b * v
    t = c
    c = d
    d = t + d * v

# reference
- continued fratctions
'''
def rationalize(x, maxsteps=10, mixed=True):
    '''approximate x to a rational form'''
    a = 0
    b = 1
    c = 1
    d = 0
    rem = x
    v0 = 0

    if mixed:
        v0 = int(rem)
        rem = rem - v0
        a,b,c,d = b, a, d, c
        if (rem < 1e-6):
            return Rat(v0,0,1)
        rem = 1/rem

    for i in range(maxsteps):
        v = int(rem)
        a,b,c,d = b, a + b * v, d, c + d * v
        rem = rem - v
        if rem < 1e-6:
            break
        rem = 1/rem

    return Rat(v0,b,d)

