from pytest import approx

# Used for number should be 0 - but there may be rounding over long calcs
def approx_zero():
    return approx(0, abs = 5)

# Used for approximations of percentages - ie < 100
def approx_percent(x):
    return approx(x, abs = 0.1)

# Used for lowish numbers - 1ks
def plus_minus_one(x):
    return approx(x, abs = 1)

# Used for highish numbers - 10k +
def plus_minus_five(x):
    return approx(x, abs = 5)

# All values are (the string) N/A - i.e. null
def are_NA(values):
    assert_ans = True
    for value in values:
        assert_ans *= (value == '-')
    return assert_ans
