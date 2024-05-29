import pandas as pd
import pytest

from greer2018 import pth_clean


@pytest.fixture(scope='module')
def data():
    df = pd.read_csv(pth_clean / "net_photosynthesis_max.csv", sep=";", comment="#")
    return df


def test_amax_is_bounded(data):
    for amax in data['amax']:
        assert 0 < amax < 25


def test_ppfd_sat_is_bounded(data):
    for ppfd in data['ppfd_sat']:
        assert 0 < ppfd < 1800


def test_temp_is_correct(data):
    assert sorted(data['temp'].unique()) == list(range(20, 39, 2))
