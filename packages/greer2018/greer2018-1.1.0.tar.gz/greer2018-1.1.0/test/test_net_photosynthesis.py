import pandas as pd
import pytest

from greer2018 import pth_clean


@pytest.fixture(scope='module')
def data():
    df = pd.read_csv(pth_clean / "net_photosynthesis.csv", sep=";", comment="#")
    return df


def test_photo_net_is_bounded(data):
    for an in data['photo_net']:
        assert -5 < an < 15


def test_ppfd_is_bounded(data):
    for ppfd in data['ppfd']:
        assert -10 < ppfd < 2100


def test_temp_is_correct(data):
    assert sorted(data['temp'].unique()) == list(range(20, 35, 2))
