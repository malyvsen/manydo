import pytest
from tqdm import tqdm
from manydo import map


def test_basic():
    assert map(lambda x: x + 3, [1, 2, 3]) == [4, 5, 6]


def test_one_job():
    assert map(lambda x: x + 3, [1, 2, 3], num_jobs=1) == [4, 5, 6]


def test_tqdm(capfd):
    result = map(lambda x: x + 3, tqdm([1, 2, 3]))
    assert result == [4, 5, 6]
    captured = capfd.readouterr()
    assert captured.out == ''
    assert '100%' in captured.err
    assert '█' in captured.err
    assert '3/3' in captured.err
    assert 'it/s' in captured.err


def test_no_output(capfd):
    result = map(lambda x: x + 3, [1, 2, 3])
    assert result == [4, 5, 6]
    captured = capfd.readouterr()
    assert captured.out == ''
    assert captured.err == ''


def test_zero_jobs():
    with pytest.raises(ValueError):
        map(lambda x: x + 3, [1, 2, 3], num_jobs=0)
    

def test_negative_jobs():
    with pytest.raises(ValueError):
        map(lambda x: x + 3, [1, 2, 3], num_jobs=-3)
