# interval arithmetic


Interval arithmetic allow us to do computations using intervals. The semantics for a operation is: a math operation with intervals is the range of the function defined by applying the same operation to a independent set of variables, each variable correspoding to a interval defining its domain.

## example

`In(1, 2) + In(30, 40) = In(31, 42)` because if `x` is in `[1 .. 2]` and `y` is in `[30 .. 40]`, `x+y` is in `[31 .. 42]`

## limitation
turns out we can't do interval _algebra_ because variables do not "couple".

let `f(x) = x*(1-x)` and `x in [0 .. 1]`. The range of `f` is in `[0 .. 1/4]` but `In(0, 1) * (In(1, 1) - In(0, 1)) = In(0, 1)`. It contains the range, but it is not thight.