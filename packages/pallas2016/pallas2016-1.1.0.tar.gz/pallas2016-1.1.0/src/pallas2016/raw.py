"""
Raw formalisms as expressed in the article
"""
import math


def eq1(lrb, ltb, p1, p2):
    """Maximal rate of photosynthesis.

    Args:
        lrb (float): [g DM]
        ltb (float): [g DM]
        p1 (float): [µmol CO2.m-2.s-1]
        p2 (float): [µmol CO2.m-2.s-1]

    Returns:
        p_max (float)
    """
    return p1 + p2 * lrb / ltb


def eq2(par, p_max, rd, l_i, p4):
    """Amount of photosynthesis for given shoot.

    Args:
        par (float): [µmol photon]
        p_max (float): [µmol CO2.m-2.s-1] maximal rate of photosynthesis
        rd (float): [µmol CO2.m-2.s-1] leaf respiration
        l_i (float): [m2] leaf area for leafy shoot
        p4 (float): [µmol CO2.µmol photon-1]

    Returns:
        p_i (float): [g C.h-1]
    """
    k = 12e-6 * 3600  # 0.0432
    return l_i * (p_max + rd) * (1 - math.exp(-p4 * par / (p_max + rd))) * k
