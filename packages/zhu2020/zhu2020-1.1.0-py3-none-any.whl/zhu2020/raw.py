from math import log


def eq2(t_mean, t_min, t_max, t_opt):
    """Thermal time

    Args:
        t_mean (float): [°C] average daily temperature
        t_min (float): [°C] min daily temperature
        t_max (float): [°C] max daily temperature
        t_opt (float): [°C] optimal temperature for growth

    Returns:
        (float)
    """
    if not t_min < t_mean < t_max:
        return 0.

    alpha = log(2) / log((t_max - t_min) / (t_opt - t_min))
    dt_a_min = (t_mean - t_min) ** alpha
    dt_opt_min = (t_opt - t_min) ** alpha
    return (2 * dt_a_min * dt_opt_min - dt_a_min ** 2) / dt_opt_min ** 2


