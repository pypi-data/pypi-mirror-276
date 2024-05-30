import pytest

from zhu2020 import raw


def test_eq2():
    t_min = 4
    t_opt = 28
    t_max = 40

    assert 1 / raw.eq2(25, t_min, t_max, t_opt) == pytest.approx(1.04, abs=1e-2)
    assert 1 / raw.eq2(18, t_min, t_max, t_opt) == pytest.approx(1.56, abs=1e-2)
