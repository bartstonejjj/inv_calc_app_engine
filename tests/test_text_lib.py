from text_lib import *
from pandas.util.testing import assert_series_equal, assert_frame_equal
import pandas as pd
import numpy as np

def test_signifigicant_figures_str():
    assert signifigicant_figures_str(1234) == '1.23k'
    assert signifigicant_figures_str(1234.0) == '1.23k'
    assert signifigicant_figures_str(1234.01) == '1.23k'

    assert signifigicant_figures_str(-1234) == '-1.23k'
    assert signifigicant_figures_str(-1234.0) == '-1.23k'
    assert signifigicant_figures_str(-1234.01) == '-1.23k'

    assert signifigicant_figures_str(123) == '123'
    assert signifigicant_figures_str(123.4) == '123'
    assert signifigicant_figures_str(123.0) == '123'

    assert signifigicant_figures_str(-123) == '-123'
    assert signifigicant_figures_str(-123.4) == '-123'
    assert signifigicant_figures_str(-123.0) == '-123'

    assert signifigicant_figures_str(12.34) == '12.3'
    assert signifigicant_figures_str(12.0) == '12' # always clip zero fraction
    assert signifigicant_figures_str(12) == '12'

def test_signifigicant_figures_str_bad_vars():
    assert signifigicant_figures_str(0) == '0'
    assert signifigicant_figures_str(None) is None
    assert signifigicant_figures_str('Hello') == 'Hello'
    assert signifigicant_figures_str({1:2}) == {1:2}
    assert_frame_equal(signifigicant_figures_str(pd.DataFrame([0])),
        pd.DataFrame([0]))
    assert_series_equal(signifigicant_figures_str(pd.Series([0])),
        pd.Series([0]))
    assert signifigicant_figures_str(np.nan) == '-'