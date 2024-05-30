import pandas as pd
import pytest

from prieto2010 import pth_clean


@pytest.fixture(params=("in", "out", "cloud"))
def meas(request):
    mod = request.param
    return pd.read_csv(pth_clean / f"fig8_{mod}.csv", sep=";", comment="#", parse_dates=['date'], index_col=['date'])


def test_fig8_values_are_not_nan(meas):
    for cname in ('an', 'ppfd', 'temp', 'transpi', 'vpd'):
        assert len(meas[cname]) == len(meas[cname].dropna())
