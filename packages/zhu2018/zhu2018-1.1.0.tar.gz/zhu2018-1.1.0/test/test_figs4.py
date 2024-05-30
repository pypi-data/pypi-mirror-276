import pandas as pd
import pytest

from zhu2018 import pth_clean


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(pth_clean / "figs4.csv", sep=";", comment="#", index_col=['hour'])


def test_meas_are_every_hour(df):
    assert ((df.index[1:] - df.index[:-1]) == 1).all()


def test_meas_are_strictly_positive(df):
    for cname in df.columns:
        assert (df[cname] >= 0).all()
