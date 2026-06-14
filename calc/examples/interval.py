import numbers

class NumberRange:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __add__(self, other):
        if isinstance(other, NumberRange):
            return radd(self, other)
        if isinstance(other, numbers.Number):
            r = rnumber(other)
            return radd(self, r)
        raise TypeError("ivalid type")

    def __radd__(self, other):
        if isinstance(other, numbers.Number):
            return radd(self, rnumber(other))
        raise TypeError("ivalid type")


    def __sub__(self, other):
        if isinstance(other, NumberRange):
            return rsub(self, other)
        if isinstance(other, numbers.Number):
            r = rnumber(other)
            return rsub(self, r)
        raise TypeError("ivalid type")

    def __rsub__(self, other):
        if isinstance(other, numbers.Number):
            return rsub(self, rnumber(other))
        raise TypeError("ivalid type")

    def __mul__(self, other):
        if isinstance(other, NumberRange):
            return rmul(self, other)
        if isinstance(other, numbers.Number):
            r = rnumber(other)
            return rmul(self, r)
        raise TypeError("ivalid type")

    def __rmul__(self, other):
        if isinstance(other, numbers.Number):
            return rmul(self, rnumber(other))
        raise TypeError("ivalid type")

    def __truediv__(self, other):
        if isinstance(other, NumberRange):
            return rdiv(self, other)
        if isinstance(other, numbers.Number):
            r = rnumber(other)
            return rdiv(self, r)
        raise TypeError("ivalid type")

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Number):
            return rdiv(self, rnumber(other))
        raise TypeError("ivalid type")


class In(NumberRange):
    def __init__(self, begin, end):
        assert(begin <= end)
        NumberRange.__init__(self, begin, end)
    def __repr__(self):
        return f"In({self.begin},{self.end})"

class Out(NumberRange):
    def __init__(self, begin, end):
        NumberRange.__init__(self, begin, end)
    def __repr__(self):
        return f"Out({self.begin},{self.end})"


def radd(a, b):
    '''
    in + out:
    a < x < b     and    (y < c or d < y)
    a + d < x + y   or   x + y < b + c

    out + out:
    (x < a or b < x)  and  (y < c or d < y)
    x + y < a + c  or b + d < x + y or unrestricted or unrestricted
    unrestricted
    '''
    if isinstance(a, In) and isinstance(b, In):
        return In(a.begin+b.begin, a.end+b.end)
    if isinstance(a, Out) and isinstance(b, Out):
        return Out(0,0) #unrestricted
    if isinstance(a,In) and isinstance(b, Out):
        return Out(a.end + b.begin, a.begin + b.end)
    if isinstance(a, Out) and isinstance(b, In):
        return Out(a.begin + b.end, a.end + b.begin)

    assert(0 and "not implemented")

def rnumber(a):
    return In(a, a)

def rneg(a):
    if isinstance(a, In):
        return In(-a.end, -a.begin)
    if isinstance(a, Out):
        return Out(-a.end, -a.begin)

def rsub(a,b):
    '''
    ab < x < ae       bb < y < be

    ab - be < x - y < ae - ab
    '''
    return radd(a, rneg(b))

def rmul(a,b):
    if isinstance(a, In) and isinstance(b, In):
        l = []
        l.append(a.begin * b.begin)
        l.append(a.begin * b.end)
        l.append(a.end   * b.begin)
        l.append(a.end   * b.end)
        return In(min(l), max(l))

# def rdiv(a,b):
#     if isinstance(a, In) and isinstance(b, In):

def rinv(a):
    if isinstance(a, In):
        if a.begin > 0 or a.end < 0:
            return In(1/a.end, 1/a.begin)
        else:
            return Out(1/a.begin, 1/a.end)
    if isinstance(a, Out):
        if a.begin > 0 or a.end < 0:
            return Out(1/a.end, 1/a.begin)
        else:
            return In(1/a.begin, 1/a.end)

def rdiv(a,b):
    return rmul(a, rinv(b))

def res(v, tol=0.05):
    return In(v*(1-tol), v*(1+tol))

def out2(v1, r1, v2, r2):
    return (v1/r1 + v2/r2)/(1/r1 + 1/r2)

#### TESTS ####################################################################

def test1():
    print(In(3,4))
    print(In(-1,9))
    # print(In(10,5)) invalid interval
    print(Out(1,5))

    a = In(1,3)
    b = In(10,20)
    c = In(500,600)

    print(radd(a,b))
    print(radd(a,c))

    d = In(-3, 3)
    e = In(-5, 4)
    f = In(-5,-2)

    print(rmul(b,d))
    print(rmul(d,e))

    print(rinv(a))
    print(rinv(f))
    print(rinv(e))

def test2():
    a = In(1,3)
    b = Out(-1,1)

    print(radd(a,b))

def test3():
    r1 = res(1500)
    r2 = res(3000)
    Vi = In(6,6)
    t1 = radd(r1, r2)
    t2 = rdiv(r1, t1)
    print(f"{t1=}")
    print(f"{t2=}")
    Vo = rmul(Vi, t2)
    print(Vo)

    low  = out2(6, r2.end, 0, r1.begin)
    high = out2(6, r2.begin, 0, r1.end)
    print(f"{low=}, {high=}")

def test4():
    x = In(0,1)
    one = In(1,1)

    r = rmul(x, rsub(one, x))
    print(f"{r=}")

def test5():
    r1 = res(1500)
    r2 = res(3000)
    Vi = In(6,6)
    Vo = rmul(Vi, rinv(radd(In(1,1), rdiv(r2,r1))))
    print(Vo)

    low  = out2(6, r2.end, 0, r1.begin)
    high = out2(6, r2.begin, 0, r1.end)
    print(f"{low=}, {high=}")

def test6():
    x = In(0,1)
    half = In(1/2,1/2)
    quarter = In(1/4,1/4)

    t1 = rsub(x, half)
    t2 = rmul(t1, t1)
    print(f"{t2=}")
    r = rsub(quarter, t2)
    print(f"{r=}")

def test7():
    x = In(-1,1)

    #f(x) = x²
    f = rmul(x,x)
    print(f"{f=}")
    # we would expect the smallest output value
    # would be 0, because x² can not produce negative
    # values (we are not considering complex numbers)
    # but because there is no coupling, it's like
    # f = x1 * x2, the smalles value for f is
    # obtained for, say x1 = 1 and x2 = -1

def test8():
    t1 = In(1,2) + 3
    print(f"{t1=}")
    t2 = 4.0 + In(1,2)
    print(f"{t2=}")

if __name__ == "__main__":
    test8()

