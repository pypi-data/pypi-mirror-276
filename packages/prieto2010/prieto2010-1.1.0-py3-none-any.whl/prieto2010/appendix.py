"""
Equation from Appendix 1
"""
import math

gas_constant = 8.3144598
"""[J.K-1.mol-1] Universal gas constant

References: scipy.constants.gas_constant
"""


def eq1(vc, ci, gamma_star, rd):
    """Net CO2 assimilation.

    Args:
        vc (float): [µmol CO2.m-2.s-1] rate of carboxylation
        ci (float): [Pa] partial pressure of CO2 in the intercellular space
        gamma_star (float): [Pa] Compensation point for CO2 in the absence of dark
                            respiration
        rd (float): [Pa] rate of CO2 evolution in the light resulting from processes
                    other than photorespiration

    Returns:
        (float): A [µmol CO2.m-2.s-1]
    """
    return vc * (1 - gamma_star / ci) - rd


def eq2(ac, aj, ap):
    """Rate of carboxylation.

    Args:
        ac (float): [µmol CO2.m-2.s-1] rate of carboxylation limited solely by
                    the amount, activation state and kinetic properties of Rubisco
        aj (float): [µmol CO2.m-2.s-1] rate of carboxylation limited solely by
                    the rate of RuBP regeneration in the Calvin cycle
        ap (float): [µmol CO2.m-2.s-1] rate of carboxylation limited solely by
                    inorganic phosphate

    Returns:
        (float): Vc [µmol CO2.m-2.s-1]
    """
    return min(ac, aj, ap)


def eq3(vc_max, ci, o, kc, ko):
    """Rubisco-limited carboxylation rate.

    Args:
        vc_max (float): [µmol CO2.m-2.s-1] maximum rate of carboxylation
        ci (float): [Pa] partial pressure of CO2 in the intercellular space
        o (float): [kPa] partial pressure of O2 in the intercellular space
        kc (float): [Pa CO2] Michaelis constant for carboxylation
        ko (float): [kPa O2] Michaelis constant for oxygenation

    Returns:
        (float): Ac [µmol CO2.m-2.s-1]
    """
    return vc_max * ci / (ci + kc * (1 + o / ko))


def eq4(j, ci, gamma_star):
    """RuBP regeneration-limited carboxylation rate.

    Args:
        j (float): [µmol e-.m-2.s-1] rate of electron transport
        ci (float): [Pa] partial pressure of CO2 in the intercellular space
        gamma_star (float): [Pa] Compensation point for CO2 in the absence of dark
                            respiration

    Returns:
        (float): Aj [µmol CO2.m-2.s-1] because factor 4 in equation below
    """
    return j * ci / (4 * ci + 8 * gamma_star)


def eq5(tpu, ci, gamma_star):
    """TPU-limited carboxylation rate.

    Args:
        tpu (float): [µmol CO2.m-2.s-1] rate of phosphate release in triose phosphate utilization
        ci (float): [Pa] partial pressure of CO2 in the intercellular space
        gamma_star (float): [Pa] Compensation point for CO2 in the absence of dark
                            respiration

    Returns:
        (float): Ap [µmol CO2.m-2.s-1]
    """
    return 3 * tpu / (1 - gamma_star / ci)


def eq6(ppfd, alpha, j_max):
    """Electron transport rate.

    Args:
        ppfd (float): [µmol photon.m-2.s-1] Photosynthetic photon flux density
        alpha (float): [µmol CO2.µmol photon-1] photochemical efficiency
        j_max (float): [µmol e-.m-2.s-1] Maximum electron transport rate

    Returns:
        j (float): [µmol e-.m-2.s-1] Electron transport rate
    """
    return alpha * ppfd / math.sqrt(1 + alpha ** 2 * ppfd ** 2 / j_max ** 2)


def eq7(t_leaf, c, delta_ha):
    """Temperature dependence for Kc, Ko, gamma* and Rd.

    Args:
        t_leaf (float): [°C] leaf temperature
        c (float): [-] scaling constant
        delta_ha (float): [kJ.mol-1] Enthalpie of activation

    Returns:
        (float): [-]
    """
    tk = t_leaf + 273.15
    rtk = gas_constant * 1e-3 * tk  # [J.mol-1] to [kJ.mol-1]
    return math.exp(c - delta_ha / rtk)


def eq8(t_leaf, c, delta_ha, delta_hd, delta_s):
    """Temperature dependence for Vcmax, Jmax and TPU.

    Args:
        t_leaf (float): [°C] leaf temperature
        c (float): [-] scaling constant
        delta_ha (float): [kJ.mol-1] Enthalpie of activation
        delta_hd (float): [kJ.mol-1] Enthalpie of deactivation
        delta_s (float): [kJ.K-1.mol-1] Entropy term

    Returns:
        (float): [-]
    """
    tk = t_leaf + 273.15
    rtk = gas_constant * 1e-3 * tk  # [J.mol-1] to [kJ.mol-1]
    num = math.exp(c - delta_ha / rtk)
    denom = 1 + math.exp((delta_s * tk - delta_hd) / rtk)  # bug correction from paper (see harley1992)

    return num / denom


def eq9(na, sna, b):
    """Nitrogen dependence function for Vcmax, Jmax, TPU and Rd at 25 °C

    Warnings: corrected for error in sign

    Args:
        na (float): [g.m-2] Leaf nitrogen content per area
        sna (float): [µmol.g-1.s-1] Slope of the relationship between Na and
                     Vcmax, Jmax, TPU or Rd
        b (float): [?] Intercept of the relationship between Na and Vcmax, Jmax,
                   TPU or Rd

    Returns:
        (float)
    """
    return sna * na + b  # bug correction by comparison with figure7


def eq10(a, vpd, cs, gamma, g0, a1, d0):
    """Stomatal conductance.

    Args:
        a (float): [µmol CO2.m-2.s-1] Net photosynthetic rate
        vpd (float): [kPa] Water vapour pressure deficit
        cs (float): [Pa] CO2 partial pressure at the leaf surface
        gamma (float): [Pa] gamma_star???
        g0 (float): [mmol H2O.m-2.s-1] Residual stomatal conductance when A -> 0
        a1 (float): [?] Empirical stomatal conductance factor
        d0 (float): [?] Empirical factor assessing stomata sensitivity to VPD

    Returns:
        (float): gs [mmol H2O.m-2.s-1]
    """
    return g0 + a1 * a / (1 + vpd / d0) / (cs - gamma)


def eq11(a, ca, gb):
    """CO2 partial pressure at the leaf surface.

    Args:
        a (float): [µmol CO2.m-2.s-1] Net photosynthetic rate
        ca (float): [Pa] CO2 partial pressure at the leaf surface
        gb (float): [mol.m-2.s-1] Boundary layer conductance

    Returns:
        (float): Cs [Pa]
    """
    return ca - a * 1.37 / gb


def eq12(a, ca, gb, gs):
    """CO2 partial pressure in intercellular space.

    Args:
        a (float): [µmol CO2.m-2.s-1] Net photosynthetic rate
        ca (float): [Pa] CO2 partial pressure at the leaf surface
        gb (float): [mol.m-2.s-1] Boundary layer conductance
        gs (float): [mmol H2O.m-2.s-1] Stomatal conductance

    Returns:
        (float): Ci [Pa]
    """
    return ca - a * 1.6 / gs * 1.37 / gb
