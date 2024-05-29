import pandas as pd
import pytest

from medlyn2002 import pth_clean, raw
from medlyn2002.external import kelvin


def test_k25_equals_formalism_at_25():
    tab = pd.read_csv(pth_clean / "tab3.csv", sep=";", comment="#", index_col=['species'])
    tk = kelvin(25)

    for sp, row in tab.iterrows():
        val25 = raw.eq18(tk, kelvin(row['t_opt']), row['k_opt'], row['ha'] * 1e3, row['hd'] * 1e3)

        assert val25 == pytest.approx(row['k25'], abs=0.1)
