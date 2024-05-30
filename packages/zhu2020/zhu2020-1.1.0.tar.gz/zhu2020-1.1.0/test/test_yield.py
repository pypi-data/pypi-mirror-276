import pytest

from zhu2020.table1 import harvest_yield


def test_harvest_yield_model():  # from p227 second paragraph
    t_max_ini = 21  # [°C] mean from fig3
    rad_ini = 24  # [MJ.day-1] mean from fig3
    t_max_flow = 16  # [°C] mean from fig5
    eto_rain_tot_ver = 0  # [mm] no information available

    yield_ref = harvest_yield(t_max_ini, rad_ini, t_max_flow, eto_rain_tot_ver, cane_nb=2)
    yield_inc = harvest_yield(t_max_ini + 1, rad_ini, t_max_flow + 1, eto_rain_tot_ver, cane_nb=2)
    assert yield_inc - yield_ref == pytest.approx(0.53, abs=1e-8)

    yield_ref = harvest_yield(t_max_ini, rad_ini, t_max_flow, eto_rain_tot_ver, cane_nb=4)
    yield_inc = harvest_yield(t_max_ini + 1, rad_ini, t_max_flow + 1, eto_rain_tot_ver, cane_nb=4)
    assert yield_inc - yield_ref == pytest.approx(1.29, abs=1e-8)
