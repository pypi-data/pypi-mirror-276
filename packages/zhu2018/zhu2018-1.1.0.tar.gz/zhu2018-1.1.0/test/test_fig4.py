import pandas as pd
import pytest

from zhu2018 import pth_clean


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(pth_clean / "fig4.csv", sep=";", comment="#", index_col=['hour'])


def test_sim_are_every_hour(df):
    assert ((df.index[1:] - df.index[:-1]) == 1).all()


def test_sim_are_defined_for_each_hour(df):
    for cname in df.columns:
        if cname.endswith("_sim"):
            assert pd.notna(df[cname]).all()
