import math
import pandas as pd

def years_in_words(years):
    if not years:
        return years
    if type(years) == str or not years: # safeguard erroneous inputs
        return years

    y = math.floor(years) # take the year component by flooring
    m = math.ceil((years - y) * 12) # take the month ceiling
    
    if m == 12: # special case due to ceiling
        y += 1
        m = 0
    
    def get_str(value, word):
        s = '' if value <= 1 else 's'
        return '{} {}'.format(value, word) + s if value != 0 else ''
    
    a = get_str(y, 'year')
    b = get_str(m, 'month')
    
    if not a and not b:
        return '0 years'
    elif not a and b:
        return b
    elif a and not b:
        return a
    else:
        return a + ' and ' + b

def signifigicant_figures_str(x, sig_figs = 3, null_value = '-'):
    if isinstance(x, pd.DataFrame) or isinstance(x, pd.Series):
        return x

    if x == None:
        return x

    if x == 0:
        return '0'

    if pd.isnull(x):
        return null_value
    
    try:
        ans = round(x, -int(math.floor(math.log10(abs(x))) - (sig_figs - 1)))
        
        def clip_zero_fraction(num):
            if math.modf(num)[0]: # If it has a non-zero fractional part
                return num
            else:
                return int(math.modf(num)[1])
        
        if abs(x) >= 1000:
            ans = ans / 1000
            ans = clip_zero_fraction(num = ans)
            return str(ans) + 'k'
        else:
            return str(clip_zero_fraction(num = ans))  
            
    except:
        return x

def apply_signifigicant_figures_str_to_dict(dct):
    for k,v in dct.items():
        dct[k] = signifigicant_figures_str(v)
    return dct