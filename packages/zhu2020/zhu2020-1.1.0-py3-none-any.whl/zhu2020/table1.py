"""
Formalisms from table1
"""


def bunch_nb(t_max_ini, rad_ini, cane_nb=2):
    if cane_nb == 2:
        return 34.48 + 2.87 * t_max_ini + 0.58 * rad_ini
    elif cane_nb == 4:
        return 43.43 + 4.6 * t_max_ini + 0.42 * rad_ini
    else:
        raise NotImplementedError(f"cane nb {cane_nb:d} not implemented, only 2 and 4")


def berry_nb(t_mean_flow, rain_tot_flow, t_max_ini):
    return -44.3 + 3.18 * t_mean_flow + 0.83 * rain_tot_flow + 2.58 * t_max_ini + 0.047 * t_mean_flow * rain_tot_flow


def berry_mass(t_mean_flow, rain_tot_flow, rad_flow, rain_tot_ver):
    return (1.4 - 1.65e-2 * t_mean_flow - 1.67e-2 * rain_tot_flow + 3.8e-2 * rad_flow + 2.33e-2 * rain_tot_ver
            + 9.87e-4 * t_mean_flow * rain_tot_flow - 8.98e-4 * rad_flow * rain_tot_ver)


def bunch_mass(t_mean_flow, rain_tot_flow, eto_rain_tot_ver):
    return (47.23 + 6.42 * t_mean_flow - 2.88 * rain_tot_flow - 0.09 * eto_rain_tot_ver
            + 0.17 * t_mean_flow * rain_tot_flow)


def harvest_yield(t_max_ini, rad_ini, t_max_flow, eto_rain_tot_ver, cane_nb=2):
    if cane_nb == 2:
        return -13.55 + 0.2 * t_max_ini + 0.34 * rad_ini + 0.33 * t_max_flow - 9.6e-3 * eto_rain_tot_ver
    elif cane_nb == 4:
        return -28.24 + 0.37 * t_max_ini + 0.3 * rad_ini + 0.92 * t_max_flow + 4.6e-3 * eto_rain_tot_ver
    else:
        raise NotImplementedError(f"cane nb {cane_nb:d} not implemented, only 2 and 4")
